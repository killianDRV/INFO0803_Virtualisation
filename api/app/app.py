from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import logging
logger = logging.getLogger('gunicorn.error')

app = Flask(__name__)
# URL de la base de données MongoDB
app.config['MONGO_URI'] = 'mongodb://root:example@mongo:27017/contact_db?authSource=admin'
mongo = PyMongo(app)


# Endpoint pour récupérer tous les contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        # Récupère tous les contacts depuis la base de données
        contacts = list(mongo.db.contacts.find())

        for contact in contacts:
            contact['_id'] = str(contact['_id'])

        return jsonify(contacts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint pour ajouter un nouveau contact
@app.route('/contacts', methods=['POST'])
def add_contact():
    app.logger.debug("Received POST request to /contacts")

    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    propriete = data.get('propriete')

    new_contact = {
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'propriete': propriete
    }

    try:
        # Insere le nouveau contact dans la base de données
        result = mongo.db.contacts.insert_one(new_contact)

        return jsonify({'message': 'Contact added successfully', 'id': str(result.inserted_id)}), 200
    except Exception as e:
        app.logger.error(f"Failed to add contact: {e}")
        return jsonify({'error': 'Failed to add contact'}), 500


# Endpoint pour supprimer un contact par son ID
@app.route('/contacts/<string:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        # Supprime le contact de la base de données en utilisant son ObjectID
        result = mongo.db.contacts.delete_one({'_id': ObjectId(contact_id)})

        if result.deleted_count == 0:
            return jsonify({'error': 'Contact not found'}), 404
        
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        app.logger.error(f"Failed to delete contact: {e}")
        return jsonify({'error': 'Failed to delete contact'}), 500


# Endpoint pour filtrer les contacts par critère et valeur
@app.route('/search/<string:critere>/<string:valeur>', methods=['GET'])
def filter_contacts(critere, valeur):
    # app.logger.debug(f"critere ===== {critere}")
    # app.logger.debug(f"valeur ===== {valeur}")

    if critere and valeur:
        # Construit une requête mongo pour filtrer les contacts basés sur critere et valeur
        query = {f'propriete.{critere}': {'$regex': valeur, '$options': 'i'}}
        contacts = list(mongo.db.contacts.find(query))
    else:
        # Si aucun critère n'est spécifié, récupère tous les contacts de la base de données
        contacts = list(mongo.db.contacts.find())
    
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
    
    return jsonify(contacts), 200


if __name__ == '__main__':
    # Démarre l'application Flask
    app.run(host='0.0.0.0', port=5001, debug=True)