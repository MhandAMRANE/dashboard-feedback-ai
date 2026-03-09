# Dashboard Feedback AI (Sessions 1 & 2)

Ce projet est un tableau de bord analytique conçu pour importer, visualiser et bientôt analyser des feedbacks clients via une intelligence artificielle.

##  État Actuel (Sessions 1 & 2)

Actuellement, les fondations du projet et l'ingestion de données sont terminées :

- **Squelette Flask** : Structure complète de l'application avec routage et navigation professionnelle.
- **Design System** : Interface moderne "Slate & Indigo" utilisant la police Inter, des cartes d'information et un système de badges.
- **Importation CSV (Pandas)** : 
  - Système de dépôt de fichier `.csv`.
  - Aperçu instantané des 5 premières lignes via Pandas.
  - Statistiques rapides sur le contenu du fichier (nom, nombre de lignes/colonnes).

##  Installation & Lancement

1. **Prérequis** : Assurez-vous d'avoir Python 3.9+ d'installé.
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurer l'environnement** :
   - Copiez le fichier d'exemple : `cp .env.example .env` (ou renommez-le manuellement).
   - Pour les Sessions 1 & 2, les valeurs par défaut suffisent.
4. **Lancer le serveur** :
   ```bash
   python app.py
   ```
5. **Accès** : Ouvrez votre navigateur sur `http://127.0.0.1:5000`.

##  Utilisation

- Rendez-vous dans la section **"Importer"**.
- Sélectionnez le fichier d'exemple `data/sample_feedbacks.csv`.
- Cliquez sur **"Lancer l'importation"** pour voir l'aperçu dynamique de vos données.

---
*Note : Les fonctionnalités de stockage SQLite et d'analyse IA (DeepSeek) font partie des sessions suivantes.( session 3,4,5,6)*
