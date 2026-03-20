# Journal de Développement - Dashboard d’analyse de feedback client

Ce projet a pour but de créer un dashboard intelligent pour analyser les retours clients (feedbacks) en utilisant l'intelligence artificielle.

---

## Session 1 — Fondations et Structure
### Ce que je voulais faire
L'objectif était de poser les bases techniques. Je ne savais pas trop par où commencer, alors j'ai décidé de partir sur une structure Flask classique. Je voulais simplement avoir une application qui "tourne" avec trois pages de base (Accueil, Import, Dashboard) pour visualiser le flux de travail futur.

### Comment j’ai travaillé avec l’IA
J'ai demandé à l'IA : « Aide-moi à créer la structure d'une application Flask avec un dossier templates et un dossier static. Je veux trois routes de base. » 
L'IA m'a généré un squelette propre. J'ai dû corriger le fait que l'IA avait oublié de me dire comment lier le fichier CSS dans `base.html` au début. J'ai compris l'importance de `url_for('static', filename='...')`.

### Ce qui a bloqué ou changé
Au début, je voulais mettre tout mon HTML dans un seul fichier, mais l'IA m'a suggéré d'utiliser l'héritage de templates avec `base.html`. J'ai hésité car ça paraissait plus complexe, mais j'ai fini par accepter car j'ai compris que ça m'éviterait de copier-coller le menu sur chaque page.

### Ce que j’en retiens
J'ai appris la structure standard d'un projet web en Python. Ce n'est pas juste du code, c'est une organisation.

---

## Session 2 — Gestion des Importations CSV
### Ce que je voulais faire
Je voulais que l'utilisateur puisse envoyer ses propres données. L'idée était d'importer un CSV et d'en afficher un aperçu immédiat pour rassurer l'utilisateur sur le fait que son fichier a bien été lu.

### Comment j’ai travaillé avec l’IA
J'ai utilisé le prompt : « Comment gérer l'upload d'un fichier CSV en Flask et l'afficher dans un tableau HTML avec Pandas ? »
L'IA m'a proposé d'utiliser `request.files`. Ce qui était génial, c'est qu'elle m'a montré comment transformer un DataFrame Pandas en dictionnaire pour que Jinja2 puisse boucler dessus facilement.

### Ce qui a bloqué ou changé
Le plus gros problème a été les fichiers mal formés. J'ai essayé d'importer un fichier qui n'était pas un CSV et le serveur a planté lamentablement. J'ai dû ajouter des vérifications sur l'extension du fichier (`ALLOWED_EXTENSIONS`).

### Ce que j’en retiens
On ne peut jamais faire confiance à ce que l'utilisateur envoie. La validation des données est 50% du travail.

---

## Session 3 — Persistance avec SQLite
### Ce que je voulais faire
L'aperçu c'est bien, mais si on ferme le navigateur, on perd tout. Je devais passer à une base de données. J'ai choisi SQLite car c'est léger et ça ne demande pas d'installation de serveur lourd (comme PostgreSQL).

### Comment j’ai travaillé avec l’IA
Prompt : « Je veux stocker mes feedbacks dans une table SQLite. Comment éviter d'insérer deux fois le même message si l'utilisateur ré-importe le même fichier ? »
L'IA m'a suggéré de créer un `text_hash` (un identifiant unique basé sur le contenu du texte). C'était une révélation pour moi.

### Ce qui a bloqué ou changé
J'ai eu des soucis avec les formats de date qui variaient d'un CSV à l'autre. J'ai essayé de coder un parseur complexe, mais l'IA m'a aidé à simplifier ça avec une fonction de normalisation dans `utils.py`.

### Ce que j’en retiens
L'importance des identifiants uniques. Sans le hash, ma base de données se remplissait de doublons à chaque test.

---

## Session 4 — Le saut dans l'IA (OpenRouter)
### Ce que je voulais faire
C'est le cœur du projet : transformer du texte brut en données structurées (sentiment, thèmes). Je voulais automatiser l'analyse que je ferais normalement à la main.

### Comment j’ai travaillé avec l’IA
Ici, c'était crucial. Prompt : « Crée un prompt pour OpenAI/Gemini qui analyse un feedback et retourne UNIQUEMENT un JSON avec les champs 'sentiment', 'themes', et 'confidence'. »
J'ai dû me battre contre le fait que l'IA bavarde (elle mettait "Voici le JSON..." avant le code). J'ai corrigé en ajoutant des instructions de "output format" très strictes.

### Ce qui a bloqué ou changé
Parfois, l'API ne répondait pas ou renvoyait une erreur. J'ai failli abandonner la gestion d'erreur complexe pour faire du simple `try/except`, mais j'ai finalement gardé un système qui affiche l'erreur à l'utilisateur dans le dashboard.

### Ce que j’en retiens
Les LLM sont puissants mais imprévisibles. Il faut les "dresser" avec des prompts très fermés pour obtenir du JSON propre.

---

## Session 5 & 6 — Analytics et Visualisation
### Ce que je voulais faire
Passer de "j'ai des données" à "j'ai des informations". Je voulais un dashboard avec des cartes de scores et des filtres interactifs.

### Comment j’ai travaillé avec l’IA
J'ai demandé à l'IA : « Comment calculer les thèmes les plus fréquents si chaque feedback peut avoir plusieurs thèmes séparés par des virgules ? »
L'IA m'a aidé à faire un `split().strip()` efficace. Pour l'interface, j'ai utilisé Chart.js pour les graphiques, ce qui a rendu le dashboard beaucoup plus "pro".

### Ce qui a bloqué ou changé
Le filtrage par date a été un enfer car les dates en SQL et en Python ne se parlent pas toujours bien. J'ai passé deux heures à débugger pourquoi ma liste de feedbacks était vide alors qu'il y en avait en base. C'était juste un problème de format "YYYY-MM-DD" vs "DD/MM/YYYY".

### Ce que j’en retiens
La visualisation de données est valorisante, mais l'agrégation en amont (le nettoyage) est la partie la plus dure.

---

## Session 7 — Exports CSV/PDF et Professionnalisation
### Ce que je voulais faire
L'objectif était de permettre l'exportation des résultats. J'avais déjà une exportation CSV mais elle était cassée suite à une modification. Je voulais la réparer et ajouter l'exportation PDF pour un rendu plus pro.

### Comment j’ai travaillé avec l’IA
J'ai dû demander à l'IA de restaurer la route `/export` que j'avais écrasée par erreur : « Restaure la fonction d'export CSV d'origine car je l'ai perdue. » Puis j'ai demandé : « Ajoute maintenant l'export PDF avec reportlab. »
J'ai appris à peupler un document PDF dynamiquement à partir d'une liste de dictionnaires.

### Ce qui a bloqué ou changé
La mise en page du PDF a été délicate. Les colonnes étaient trop larges. J'ai dû apprendre à gérer les dimensions et les positions avec `reportlab`.

### Ce que j’en retiens
Restaurer du code perdu est frustrant, j'ai compris pourquoi Git est indispensable. GitHub m'a sauvé la mise pour synchroniser mes versions.

---

## Session 8 — Expérimentation et Pivot Final (Les Alertes)
### Ce que je voulais faire
Je voulais aller plus loin avec un système d'alerte automatique (notification si trop de feedbacks négatifs). 

### Comment j’ai travaillé avec l’IA
J'ai implémenté un système avec un seuil dans le fichier `.env`. C'était intéressant techniquement de découpler la configuration du code source.

### Ce qui a bloqué ou changé (Décision de retrait)
Finalement, j'ai décidé de **supprimer cette fonctionnalité**. Après réflexion, je trouvais que cela alourdissait l'application sans apporter de réelle valeur ajoutée immédiate pour l'utilisateur.
**Action radicale :** J'ai supprimé tout le code lié aux alertes (route, template, service Python).
Ce n'est pas un échec, c'est un choix conscient de garder un produit simple et efficace.

### Ce que j’en retiens
Savoir retirer une fonctionnalité est une preuve de maturité. J'ai appris à "nettoyer" mon repo Git pour qu'il soit propre et prêt à être rendu sans "code mort".


---

## Session 9 — L'Audit Qualité : "LLM as Judge"
### Ce que je voulais faire
Pour aller encore plus loin dans la professionnalisation, je voulais introduire un système de contrôle qualité automatisé. L'idée est d'utiliser un second modèle d'IA (un "Juge") pour auditer les analyses du premier modèle (DeepSeek).

### Comment j’ai travaillé avec l’IA
J'ai conçu un workflow où un modèle plus puissant (Gemini 2.0 Flash) ré-analyse un échantillon de feedbacks et compare son verdict à l'original. J'ai ajouté un bouton "Audit Qualité" sur le dashboard qui déclenche ce processus.

### Ce qui a bloqué ou changé
Le principal défi était technique : modifier la structure de la base de données SQLite pour stocker les avis du juge sans perdre les données existantes. J'ai aussi dû gérer les cas de "désaccord" entre les deux IA pour les afficher clairement dans l'interface.

### Ce que j’en retiens
C'est une avancée majeure. Cela montre qu'on ne fait pas aveuglément confiance à l'IA, mais qu'on met en place des garde-fous. Le badge "Confirmé" ou "Désaccord" sur le dashboard apporte une transparence totale sur la fiabilité des données.

---

## Focus sur les choix technologiques : SQLite et OpenRouter

Comme vous m'avez mentionné que vous n'aviez pas encore utilisé SQLite et OpenRouter, voici mon retour d'expérience sur leur utilisation et comment cela fonctionne concrètement dans ce projet :

- **SQLite** : Contrairement à MySQL ou PostgreSQL, SQLite ne nécessite pas d'installer un serveur de base de données. Toute la base est stockée dans un simple fichier (`feedbacks.db`). C'est extrêmement pratique pour le développement et pour vous permettre de tester le projet sans configuration complexe. C'est robuste, rapide et parfait pour une application de ce type.
- **OpenRouter** : C'est une plateforme qui "unifie" l'accès à de nombreux modèles d'IA (OpenAI, Gemini, Claude, Mistral). Au lieu de m'enfermer dans une seule API, OpenRouter me permet de switcher de modèle en changeant juste une ligne de code dans le `.env`. Pour ce projet, cela m'a permis de tester quel modèle était le plus performant pour l'analyse de sentiment.

---

## Perspectives et évolutions futures

Afin de rendre ce projet encore plus complet et professionnel, j'envisage plusieurs pistes d'amélioration pour la suite :

- **Authentification et Sécurité** : Ajouter un système de connexion (Login) pour que seul l'administrateur puisse accéder au dashboard et aux données sensibles.
- **Analyse multilingue** : Détecter automatiquement la langue des feedbacks (français, anglais, espagnol...) et adapter l'analyse de sentiment en conséquence.
- **Tagging manuel et correction** : Permettre à l'utilisateur de corriger manuellement un sentiment ou un thème si l'IA s'est trompée, afin d'améliorer la fiabilité des statistiques.
- **Alertes automatiques (Email)** : Réintégrer le système d'alertes mais avec un envoi d'email réel (via SMTP ou une API comme SendGrid) pour être prévenu immédiatement en cas de crise (pics de retours négatifs).
- **Visualisation temporelle** : Ajouter des graphiques en ligne (Time series) pour voir comment le sentiment des clients évolue de mois en mois.
- **Recherche avancée** : Intégrer une barre de recherche pour retrouver rapidement un feedback précis par mot-clé ou par date.
- **Suggestions d'actions IA** : Aller au-delà de l'analyse et demander à l'IA de proposer des solutions concrètes (ex: "Améliorer le processus de login" ou "Vérifier le bug sur la page de paiement") à partir des critiques récurrentes.

---

## Conclusion : LLM as Judge - Un gage de qualité
J'ai finalement implémenté cette fonctionnalité d'audit. Elle permet d'afficher pour chaque feedback si l'analyse est **confirmée** par un second regard expert (Gemini) ou s'il y a un **désaccord**. C'est un pas de plus vers une IA responsable et fiable.

Ce projet n'est qu'une première étape. La base est solide, et ces évolutions en feraient un outil d'aide à la décision extrêmement puissant pour n'importe quelle entreprise.

---

## Annexe : Format de données attendu (CSV)
Le fichier CSV importé doit contenir au minimum les colonnes suivantes :
- `text` : Le contenu du feedback (obligatoire).
- `date` : La date du feedback (optionnel, format AAAA-MM-JJ).
