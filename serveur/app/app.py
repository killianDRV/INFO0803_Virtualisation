from flask import Flask, jsonify, redirect, render_template, request, url_for
import requests

import logging
logger = logging.getLogger('gunicorn.error')

app = Flask(__name__)

list_contacts = []


# Route pour la page d'accueil
@app.route('/')
@app.route('/index')
def index():
    global list_contacts

    try:
        # Récupère la liste des contacts depuis l'API via une requête GET
        response = requests.get('http://api:5001/contacts')
        if response.status_code == 200:
            list_contacts = response.json()
        else:
            # Réinitialise la liste en cas d'échec
            list_contacts = []
            app.logger.error(f"Erreur lors du fetch (code={response.status_code})")
    except requests.exceptions.RequestException as e:
        list_contacts = []
        app.logger.error(f"Error fetching contacts: {e}")

    # Renvoie vers le template 'index.html' avec la liste de contacts récupérée
    return render_template('index.html', list_contacts=list_contacts)


# Route pour ajouter un nouveau contact via une requête POST
@app.route('/contacts', methods=['POST'])
def add_contact():
    app.logger.debug("Received POST request to /contacts")
    api_url = 'http://api:5001/contacts'

    # Récupère les données du formulaire POST pour créer un nouveau contact
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    employeur = request.form.get('employeur')
    poste = request.form.get('poste')
    responsable = request.form.get('responsable')

    # Structure les données à envoyer à l'API
    data = {
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'propriete': {
            'employeur': employeur,
            'poste': poste,
            'responsable': responsable
        }
    }

    # Envoie une requête POST à l'API pour ajouter le nouveau contact    
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        app.logger.debug("Contact added successfully")
    else:
        app.logger.error("Failed to add contact")
    return redirect(url_for('index'))


# Route pour supprimer un contact
@app.route('/delete_contact/<string:contact_id>', methods=['POST', 'DELETE'])
def delete_contact(contact_id):
    try:
        if request.method in ['POST', 'DELETE']:
            api_url = f'http://api:5001/contacts/{contact_id}'

            # Envoie une requête DELETE à l'API pour supprimer le contact spécifié
            response = requests.delete(api_url)
            if response.status_code == 200:
                # Redirige vers la page d'accueil après la suppression
                return redirect(url_for('index'))
            else:
                return jsonify({'error': 'Failed to delete contact'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error deleting contact: {e}'}), 500


# Route pour filtrer les contacts
@app.route('/filter_contacts', methods=['POST'])
def filter_contacts():
    critere = request.form.get('critere')
    valeur = request.form.get('valeur')

    try:
        # Envoie une requête GET à l'API pour filtrer les contacts selon le critère et la valeur spécifiés
        response = requests.get(f'http://api:5001/search/{critere}/{valeur}')
        if response.status_code == 200:
            search_contacts = response.json()
        else:
            search_contacts = []
            app.logger.error(f"Failed to filter contacts. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        search_contacts = []
        app.logger.error(f"Error filtering contacts: {e}")

    # Renvoie le template 'index.html' avec les contacts filtrés et les valeurs actuelles du critère pour mettre a jour les tableaux
    return render_template('index.html', search_contacts=search_contacts, current_critere=critere, current_valeur=valeur)


if __name__ == '__main__':
    # Démarre l'application Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
