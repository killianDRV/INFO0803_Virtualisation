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




# # Utilisation de l'image Python officielle en tant que base
# FROM python:3.9-slim

# # Installer git pour cloner le dépôt
# RUN apt-get update && apt-get install -y git

# # Définition du répertoire de travail dans le conteneur
# WORKDIR /app

# # Cloner le dépôt GitHub pour l'API
# RUN git clone https://github.com/killianDRV/INFO0803_Virtualisation/tree/main/api.git .

# # Installation des dépendances Python
# RUN pip install --no-cache-dir -r requirements.txt

# # Commande par défaut pour démarrer l'application
# CMD ["python", "app.py"]
