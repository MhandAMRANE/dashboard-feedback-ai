## Session 1 — Mise en place du projet

## Objectif : créer la structure initiale du projet et lancer une première interface Flask.

## Travail réalisé :
•	création de l’environnement Python
•	installation de Flask, Pandas, Requests et python-dotenv
•	création de l’arborescence du projet
•	mise en place de trois pages HTML : accueil, upload, dashboard
•	ajout d’un style CSS simple

## Problèmes rencontrés :
•	gestion de la structure Flask
•	séparation entre templates et fichiers statiques
## Solution :
•	utiliser une structure Flask standard avec dossiers templates/ et static/
## Apprentissage :
•	comprendre comment Flask relie les routes Python aux pages HTML
•	comprendre la différence entre backend, templates et fichiers statiques

## Session 2 — Import CSV et aperçu des données

### Objectif
Permettre à l’utilisateur d’importer un fichier CSV de feedbacks et afficher un aperçu avant analyse.

### Travail réalisé
- Ajout d’un formulaire d’upload dans Flask
- Vérification du type de fichier
- Sauvegarde du CSV dans le dossier `data/`
- Lecture du fichier avec Pandas
- Affichage des colonnes et des 5 premières lignes dans l’interface

### Problèmes rencontrés
- Gérer les erreurs liées à l’absence de fichier
- Gérer les fichiers non CSV
- Afficher dynamiquement les données dans un tableau HTML

### Solutions
- Validation de l’extension du fichier
- Messages d’erreur clairs dans le template
- Conversion du DataFrame en dictionnaire pour l’affichage

### Apprentissage
- Comprendre le traitement d’un upload côté Flask
- Comprendre comment relier Pandas à une interface web
- Poser la base de l’ingestion des données du projet

## Session 3 — Ajout du stockage SQLite

### Objectif
Enregistrer les feedbacks importés dans une base SQLite pour assurer la persistance des données.

### Travail réalisé
- Création d’une base SQLite locale
- Création de la table `feedbacks`
- Ajout d’un système d’insertion des feedbacks
- Ajout d’un hash de texte pour éviter les doublons
- Affichage des feedbacks enregistrés dans le dashboard

### Problèmes rencontrés
- Éviter l’insertion multiple du même feedback
- Gérer les dates manquantes ou mal formatées

### Solutions
- Utilisation d’un `text_hash` unique
- Normalisation simple des dates avant insertion

### Apprentissage
- Comprendre le fonctionnement d’une base SQLite
- Comprendre l’intérêt de la persistance dans une application data
- Comprendre comment prévenir les doublons à l’ingestion

## Session 4 — Intégration de l’analyse IA avec OpenRouter

### Objectif
Enrichir les feedbacks stockés en base avec une analyse IA : sentiment, thèmes et score de confiance.

### Travail réalisé
- Création d’un module `llm.py` pour appeler OpenRouter
- Construction d’un prompt imposant une sortie JSON stricte
- Validation des réponses reçues
- Mise à jour des feedbacks analysés dans la base SQLite
- Ajout d’un bouton d’analyse dans le dashboard

### Problèmes rencontrés
- Les modèles peuvent renvoyer une réponse non strictement conforme
- Nécessité de vérifier les valeurs avant de les stocker

### Solutions
- Validation manuelle du JSON reçu
- Restriction à une liste fermée de sentiments et de thèmes
- Gestion des erreurs dans l’interface

### Apprentissage
- Comprendre comment intégrer une API LLM dans une application web
- Comprendre pourquoi il faut valider les sorties d’un modèle
- Séparer l’ingestion des données et leur enrichissement IA

