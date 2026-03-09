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