# Journal de Développement - Dashboard d’analyse de feedback client

## Parcours utilisateur & fonctionnalités principales


Lorsque vous accédez à l’application, commencez par la page « Importer ». Sélectionnez un fichier à importer : si vous vous trompez, vous pouvez supprimer ce fichier individuellement. Lors de l’importation, un aperçu des 5 premières lignes et le nombre total de feedbacks s’affichent pour vérification. Après validation, les données sont accessibles sur le dashboard.

Sur le dashboard, vous pouvez lancer l’analyse IA (« Lancer l’analyse IA ») puis déclencher un audit qualité (« Audit Qualité (LLM Judge) »). Vous accédez alors à l’historique détaillé de tous les feedbacks analysés. Il est possible de rechercher un feedback par sentiment, par thème principal ou par date précise grâce à la barre de recherche avancée. Enfin, vous pouvez exporter les résultats au format CSV ou PDF pour exploitation externe.


Ce projet a pour but de créer un dashboard intelligent pour analyser les retours clients (feedbacks) en utilisant l'intelligence artificielle.


> **Note pour le test :**
> Pour tester rapidement l’application, vous pouvez utiliser directement les fichiers CSV d’exemple déjà présents dans le dossier `data/`. Il suffit de les importer via l’interface d’importation pour alimenter le dashboard sans avoir à créer vos propres fichiers.
---

## Session 1 — Fondations et Structure
### Ce que je voulais faire
e voulais poser les bases techniques du projet, mais je ne savais pas trop par où commencer. J’ai choisi Flask parce que c’est un framework que je voulais mieux comprendre, et j’ai décidé de créer trois pages de base (Accueil, Import, Dashboard) pour visualiser le flux de travail


### Ce qui a bloqué ou changé

Au début, je voulais mettre tout mon HTML dans un seul fichier, mais l'IA m'a suggéré d'utiliser l'héritage de templates avec `base.html`.

---

## Session 2 — Gestion des Importations CSV
### Ce que je voulais faire
Je voulais que l'utilisateur puisse envoyer ses propres données. L'idée était d'importer un CSV et d'en afficher un aperçu immédiat pour rassurer l'utilisateur sur le fait que son fichier a bien été lu.


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

### Focus sur la gestion des doublons et la mise à jour de la base

L’ajout de la carte « MISE À JOUR BASE » sur le dashboard m’a permis de rendre visible le résultat de chaque importation de feedbacks. On voit immédiatement combien de nouveaux feedbacks ont été ajoutés et combien de doublons ont été ignorés. Cette transparence est essentielle pour l’utilisateur : il sait que la base ne sera jamais polluée par des répétitions, et il peut suivre l’évolution de ses données en temps réel. C’est aussi une validation concrète de l’utilité du hash unique pour chaque feedback.

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

Voir la "Répartition des Sentiments" sous forme de donut chart permet d’avoir, en un coup d’œil, une idée claire de la tonalité générale des retours clients. C’est visuel, impactant, et cela rend l’analyse beaucoup plus accessible, même pour un non-expert.

Le "Top 10 Thèmes Détectés" apporte une dimension supplémentaire : il ne s’agit plus seulement de savoir si les clients sont contents ou non, mais de comprendre précisément ce qui revient le plus souvent dans leurs feedbacks (ex : UX, performance, delivery…). Ce classement dynamique, généré automatiquement à partir des données, m’a permis d’identifier rapidement les axes d’amélioration prioritaires.

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



## Session 8 — L'Audit Qualité : "LLM as Judge"
### Ce que je voulais faire
Pour aller encore plus loin dans la professionnalisation, je voulais introduire un système de contrôle qualité automatisé. L'idée est d'utiliser un second modèle d'IA (un "Juge") pour auditer les analyses du premier modèle (DeepSeek).

### Comment j’ai travaillé avec l’IA
J'ai conçu un workflow où un modèle plus puissant (Gemini 2.0 Flash) ré-analyse un échantillon de feedbacks et compare son verdict à l'original. J'ai ajouté un bouton "Audit Qualité" sur le dashboard qui déclenche ce processus.

### Ce qui a bloqué ou changé
Le principal défi était technique : modifier la structure de la base de données SQLite pour stocker les avis du juge sans perdre les données existantes. J'ai aussi dû gérer les cas de "désaccord" entre les deux IA pour les afficher clairement dans l'interface.

### Ce que j’en retiens
C'est une avancée majeure. Cela montre qu'on ne fait pas aveuglément confiance à l'IA, mais qu'on met en place des garde-fous. Le badge "Confirmé" ou "Désaccord" sur le dashboard apporte une transparence totale sur la fiabilité des données.

### Focus sur l’explication d’audit (Explication Audit)

Un point particulièrement intéressant dans ce système d’audit qualité est l’ajout d’un champ « Explication Audit ». Pour chaque feedback audité, le LLM « juge » ne se contente pas de dire s’il est d’accord ou non avec l’analyse initiale : il fournit aussi un commentaire détaillé expliquant sa décision. 

Cela apporte une vraie valeur ajoutée : en cas de désaccord, on comprend immédiatement pourquoi (ex : « Le thème détecté initialement ne correspond pas au contenu du message », ou « Le sentiment est trop sévère au vu du texte »). Même en cas d’accord, l’explication permet de valider la pertinence de l’analyse et de rassurer sur la qualité du process.
---


## Session 9 — La Maîtrise des Données : Gestion des imports
### Ce que je voulais faire
Pour rendre l'outil vraiment utilisable, il fallait pouvoir "faire le ménage". Si un utilisateur importe le mauvais fichier, il doit pouvoir le supprimer sans tout effacer.

### Comment j’ai travaillé avec l’IA
J'ai transformé la base de données pour qu'elle "se souvienne" de l'origine de chaque feedback (`source_file`). J'ai ensuite créé une interface simple sur la page d'importation qui liste les fichiers et permet la suppression en un clic (base de données + fichier physique).

### Ce qui a bloqué ou changé
Un petit oubli d'importation (`redirect`) a causé un bug passager lors des tests, mais il a été corrigé instantanément. La structure est maintenant robuste.

### Ce que j’en retiens
La gestion granulaire des données est ce qui transforme un prototype en un véritable logiciel. Pouvoir importer, auditer par IA, puis supprimer sélectivement donne un contrôle total à l'utilisateur.

---

## Session 10 — Visualisation temporelle des sentiments (Line Chart)

### Ce que je voulais faire
Je voulais aller au bout de la promesse de la data visualisation : permettre à l’utilisateur de voir comment l’opinion des clients évolue dans le temps. L’idée était d’ajouter un graphique en ligne (Chart.js) qui affiche, semaine par semaine, le nombre de feedbacks positifs, neutres et négatifs.

### Comment j’ai travaillé avec l’IA
J’ai demandé à l’IA : « Comment grouper mes feedbacks par semaine et compter les sentiments pour chaque période ? » L’IA m’a proposé une fonction Pandas qui transforme la liste de feedbacks en DataFrame, extrait la semaine, puis compte chaque type de sentiment. J’ai ensuite intégré ce calcul dans la route Flask du dashboard, et passé les résultats à Chart.js via Jinja2.

### Ce qui a bloqué ou changé
Le plus difficile a été d’harmoniser les labels de sentiment (parfois “positif”, parfois “positive”, etc.) et de gérer les dates manquantes ou mal formatées. J’ai dû ajouter des remplacements et des vérifications pour éviter les erreurs silencieuses. L’IA m’a aussi aidé à rendre le graphique responsive et lisible.

### Ce que j’en retiens
Ce genre de visualisation donne une vraie valeur ajoutée au dashboard. On ne regarde plus seulement des chiffres statiques : on comprend l’évolution, on détecte les tendances, on peut agir. J’ai aussi appris à mieux structurer le passage de données backend → frontend, et à anticiper les problèmes de cohérence de données.

---

## Session 11 — Alerte automatique sur pic négatif thématique

### Ce que je voulais faire
Je voulais aller plus loin dans l’aide à la décision : afficher une alerte automatique si un thème précis (ex : “livraison”) reçoit un nombre anormalement élevé de feedbacks négatifs sur une semaine. L’objectif : permettre à l’utilisateur de réagir immédiatement à une crise potentielle.

### Comment j’ai travaillé avec l’IA
J’ai demandé à l’IA comment détecter ce “pic” : elle m’a proposé une fonction qui agrège les feedbacks négatifs par semaine et par thème, puis compare le résultat à un seuil (ici : 5). J’ai intégré ce calcul dans le backend Flask, et l’IA m’a aidé à afficher une bannière d’alerte sur le dashboard si le cas se présente.

### Ce qui a bloqué ou changé
Le plus délicat a été de bien harmoniser les labels de sentiment et de thème pour éviter les faux positifs. J’ai aussi réfléchi à la meilleure façon d’afficher l’alerte pour qu’elle soit visible sans être anxiogène. Finalement, la bannière n’apparaît que si le seuil est dépassé, avec la ou les semaines concernées.

### Ce que j’en retiens
Ce genre d’alerte transforme le dashboard en véritable outil de pilotage : on ne se contente plus de constater, on peut anticiper et agir. L’IA m’a permis d’implémenter cette logique très rapidement, tout en gardant le code lisible et facilement paramétrable.

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
- **Comparaison de périodes** : Permettre à l'utilisateur de comparer l'évolution des sentiments ou des thèmes entre deux périodes (ex : avant/après une mise à jour produit).
- **Clustering automatique des thèmes émergents** : Détecter automatiquement les nouveaux thèmes qui apparaissent dans les feedbacks grâce à des techniques de clustering ou d'IA.
- **Détection d’anomalie** : Mettre en place une détection automatique des variations inhabituelles (ex : un thème qui double soudainement d'une semaine à l'autre).

---

## Conclusion : Un outil complet et fiable
L'application propose désormais un cycle de vie complet pour le feedback : Importation sécurisée, Analyse par DeepSeek, Audit Qualité par Gemini (LLM as Judge) et Gestion granulaire des fichiers. C'est une base solide pour n'importe quelle analyse de sentiment professionnelle.

Ce projet n'est qu'une première étape. La base est solide, et ces évolutions en feraient un outil d'aide à la décision extrêmement puissant pour n'importe quelle entreprise.

---

## Conclusion personnelle

Ce projet m’a permis de découvrir la réalité du développement : on avance rarement en ligne droite, il faut souvent revenir en arrière, corriger, et accepter de ne pas tout réussir du premier coup. J’ai compris que l’IA est un outil puissant, mais qu’il faut savoir l’utiliser avec esprit critique. Si c’était à refaire, je passerais plus de temps à anticiper les cas d’erreur et à tester chaque étape avant d’aller plus loin. Je me sens plus à l’aise avec Flask, la gestion de données, et surtout avec l’idée que l’apprentissage passe par l’erreur. Ce journal m’a aussi aidé à prendre du recul sur mes choix et à mieux comprendre ma propre progression.

---

## Annexe : Format de données attendu (CSV)
Le fichier CSV importé doit contenir au minimum les colonnes suivantes :
- `text` : Le contenu du feedback (obligatoire).
- `date` : La date du feedback (optionnel, format AAAA-MM-JJ).


