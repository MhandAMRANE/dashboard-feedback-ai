import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")
JUDGE_MODEL = "google/gemini-2.0-flash-001"

ALLOWED_SENTIMENTS = {"positive", "neutral", "negative"}
ALLOWED_THEMES = {
    "delivery",
    "pricing",
    "quality",
    "support",
    "ux",
    "performance",
    "billing",
    "features",
    "other",
}


def build_prompt(feedback_text):
    return f"""
Analyse le feedback client suivant.

Feedback :
\"\"\"{feedback_text}\"\"\"

Retourne UNIQUEMENT un JSON valide avec cette structure exacte, sans aucun texte explicatif ni blocs de code markdown :
{{
  "sentiment": "positive | neutral | negative",
  "themes": ["theme1", "theme2"],
  "confidence": 0.0
}}

Règles :
- "sentiment" doit être exactement : positive, neutral ou negative
- "themes" doit contenir entre 1 et 3 thèmes maximum
- Les thèmes autorisés sont :
  delivery, pricing, quality, support, ux, performance, billing, features, other
- "confidence" doit être un nombre entre 0 et 1
- RÉPONSE RAW JSON UNIQUEMENT (Pas de ```json ... ```)
"""


def validate_analysis(data):
    if not isinstance(data, dict):
        raise ValueError("La réponse n'est pas un objet JSON.")

    sentiment = data.get("sentiment")
    themes = data.get("themes")
    confidence = data.get("confidence")

    if sentiment not in ALLOWED_SENTIMENTS:
        raise ValueError(f"Sentiment invalide : {sentiment}")

    if not isinstance(themes, list) or len(themes) == 0 or len(themes) > 3:
        raise ValueError("La liste des thèmes est invalide.")

    normalized_themes = []
    for theme in themes:
        if theme not in ALLOWED_THEMES:
            normalized_themes.append("other")
        else:
            normalized_themes.append(theme)

    if not isinstance(confidence, (int, float)):
        raise ValueError("Confidence doit être un nombre.")

    confidence = max(0.0, min(1.0, float(confidence)))

    return {
        "sentiment": sentiment,
        "themes": normalized_themes,
        "confidence": confidence,
    }


def analyze_feedback_with_llm(feedback_text):
    if not OPENROUTER_API_KEY:
        raise ValueError("Clé OPENROUTER_API_KEY absente du fichier .env")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": build_prompt(feedback_text)
            }
        ],
        "temperature": 0.1,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    content = result["choices"][0]["message"]["content"].strip()

    # Nettoyage des blocs de code Markdown (```json ... ``` ou ``` ... ```)
    if content.startswith("```"):
        # Enlever la ligne d'ouverture (ex: ```json)
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        # Enlever la ligne de fermeture (ex: ```)
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Réponse JSON invalide du modèle : {content}") from e

    return validate_analysis(parsed)


def analyze_feedback_with_judge(feedback_text, original_sentiment, original_themes):
    if not OPENROUTER_API_KEY:
        raise ValueError("Clé OPENROUTER_API_KEY absente du fichier .env")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"""
Tu es un Juge expert en analyse de feedback client. Ton rôle est d'évaluer une analyse déjà effectuée par une autre IA et de donner ton propre verdict.

Feedback original :
\"\"\"{feedback_text}\"\"\"

Analyse à évaluer :
- Sentiment : {original_sentiment}
- Thèmes : {original_themes}

Instructions :
1. Analyse le feedback de manière indépendante.
2. Compare ton analyse avec l'analyse fournie.
3. Retourne un JSON avec :
   - "judge_sentiment" : ton propre verdict (positive | neutral | negative)
   - "judge_themes" : liste de thèmes (delivery, pricing, quality, support, ux, performance, billing, features, other)
   - "judge_confidence" : ton niveau de confiance (0.0 à 1.0)
   - "judge_explanation" : une courte explication de ton choix, surtout si tu es en désaccord.

Réponds UNIQUEMENT par un JSON brut.
"""

    payload = {
        "model": JUDGE_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    content = result["choices"][0]["message"]["content"].strip()

    if content.startswith("```"):
        content = content.splitlines()[1:-1]
        content = "\n".join(content).strip()

    parsed = json.loads(content)
    
    # Normalisation basique
    if parsed["judge_sentiment"] not in ALLOWED_SENTIMENTS:
        parsed["judge_sentiment"] = "neutral"
        
    return parsed