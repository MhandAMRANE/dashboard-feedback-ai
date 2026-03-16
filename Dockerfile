# Utilise une image Python officielle comme image de base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste du code de l'application
COPY . .

# Définit la variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose le port utilisé par l'application Flask
EXPOSE 5000

# Commande pour lancer l'application
CMD ["flask", "run"]
