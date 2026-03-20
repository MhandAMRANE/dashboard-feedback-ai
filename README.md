#  Feedback AI – Analyse Intelligente de Retours Clients



##  Fonctionnalités Clés

- ** Import CSV Dynamique** : Importez facilement vos fichiers de retours clients avec un aperçu instantané et une validation automatique des données.
- ** Analyse IA (LLM)** : Utilise des modèles de pointe (DeepSeek, GPT-4, etc.) pour qualifier chaque feedback :
  - **Sentiment** : Positif, Neutre ou Négatif.
  - **Thématiques** : Identification automatique parmi 9 catégories (Support, Qualité, Prix, UX, etc.).
- **Dashboard Interactif** : Visualisez les tendances globales via des graphiques dynamiques (Chart.js) et filtrez les données par sentiment, thème ou date.
- **Rapports & Exports** : Exportez vos analyses au format **CSV** pour un traitement externe ou générez un rapport **PDF** professionnel.
- **Stockage Local Sécurisé** : Vos données sont conservées localement dans une base de données SQLite performante.

---

## Stack Technique

- **Backend** : Python 3.13+, Flask (Web Framework)
- **Analyse de Données** : Pandas
- **Intelligence Artificielle** : OpenRouter API (Accessibilité à plusieurs LLMs)
- **Base de Données** : SQLite
- **Frontend** : HTML5, CSS3 Moderne, Chart.js (Visualisation)
- **Reporting** : ReportLab (Génération PDF)

---

## Installation & Lancement

### 1. Cloner le projet
```bash
git clone https://github.com/MhandAMRANE/dashboard-feedback-ai.git
cd dashboard-feedback-ai
```

### 2. Configurer l'environnement virtuel (Recommandé)
```bash
python -m venv .venv
# Sur Windows :
.\.venv\Scripts\activate
# Sur macOS/Linux :
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement
Créez un fichier `.env` à la racine (ou copiez `.env.example`) :
```env
OPENROUTER_API_KEY=votre_cle_api_ici
OPENROUTER_MODEL=deepseek/deepseek-chat
DATABASE_URL=sqlite:///database/feedbacks.db
SECRET_KEY=votre_cle_secrete_flask
```

### 5. Lancer l'application
```bash
python app.py
```
Accédez à l'interface sur : **[http://127.0.0.1:5000]**

---

## Aperçu du Dashboard

---

##  Lancement avec Docker

Si vous préférez utiliser Docker, une configuration `docker-compose` est disponible :

```bash
docker-compose up --build
```
L’application sera accessible sur [http://localhost:5000].

---

## Format de données attendu (CSV)
Le fichier CSV importé doit contenir au minimum les colonnes suivantes :
- `text` : Le contenu du feedback (obligatoire).
- `date` : La date du feedback (optionnel, format AAAA-MM-JJ).


