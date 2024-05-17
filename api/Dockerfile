# Dockerfile pour backend

# Utilisation de l'image Python officielle en tant que base
FROM python:3.9-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers nécessaires dans le conteneur
COPY . /app

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour démarrer l'application
CMD ["python", "app.py"]
