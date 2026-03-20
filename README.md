# 🚀 Feedback AI - Dashboard Analytique Intelligent

**Feedback AI** est une application web moderne conçue pour transformer les retours clients bruts (CSV) en insights actionnables grâce à l'intelligence artificielle. 

L'outil permet d'importer des feedbacks, de les stocker de manière persistante, de les analyser (sentiment, thématiques) via des LLM, et d'exporter des rapports professionnels.

---

## ✨ Fonctionnalités Clés

- **📥 Import Intelligent** : Dépôt de fichiers CSV avec aperçu dynamique via Pandas.
- **🗄️ Stockage Persistant** : Base de données SQLite locale pour conserver l'historique des analyses.
- **🤖 Analyse IA (LLM)** : Détection automatique des sentiments (Positif, Neutre, Négatif) et des thématiques clés (Service, Prix, UX, Bug, etc.) via OpenRouter.
- **📊 Dashboard Interactif** : 
    - Cartes de scores en temps réel.
    - Graphiques de répartition (Chart.js).
    - Filtres multicritères (Sentiment, Thème, Date).
- **📄 Exportation Multi-format** : 
    - Exportation des données brutes en **CSV**.
    - Génération de rapports d'analyse professionnels en **PDF** (ReportLab).

---

## 🛠️ Stack Technique

- **Backend** : Python 3.9+ / Flask
- **Data** : Pandas (Traitement CSV) / SQLite (Base de données locale)
- **IA** : OpenRouter (Accès unifié aux modèles comme Gemini, GPT-4, Llama)
- **Frontend** : HTML5 / CSS3 (Vanilla) / Chart.js (Visualisation)
- **Reporting** : ReportLab (Génération PDF)

---

## 🚀 Installation et Lancement

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/MhandAMRANE/dashboard-feedback-ai.git
   cd dashboard-feedback-ai
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement** :
   - Créez un fichier `.env` à la racine :
     ```text
     OPENROUTER_API_KEY=votre_clé_ici
     OPENROUTER_MODEL=deepseek/deepseek-chat
     DATABASE_URL=sqlite:///database/feedbacks.db
     ```

4. **Lancer l'application** :
   ```bash
   python app.py
   ```
   Accédez à l'interface sur : `http://127.0.0.1:5000`

---

## 📂 Structure du Projet

```text
dashboard-feedback-ai/
├── app.py              # Point d'entrée Flask et routes
├── src/                # Logique métier
│   ├── llm.py          # Appels API OpenRouter
│   ├── storage.py      # Gestion SQLite
│   ├── analytics.py    # Calculs et statistiques
│   └── utils.py        # Fonctions utilitaires
├── templates/          # Pages HTML (Jinja2)
├── static/             # Styles CSS et Scripts JS
├── data/               # Dossier de stockage des CSV importés
└── database/           # Fichier feedbacks.db (SQLite)
```

---

## 📝 Journal de Développement
Pour plus de détails sur les choix de conception, les pivots techniques (comme l'abandon du système d'alertes) et l'évolution du projet, consultez le fichier [JOURNAL.md](./JOURNAL.md).

---
*Projet réalisé dans le cadre du module [Nom du module] - 2026*
