from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import logging
logger = logging.getLogger('gunicorn.error')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:example@mongo:27017/contact_db?authSource=admin'
mongo = PyMongo(app)

@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        contacts = list(mongo.db.contacts.find())
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
        app.logger.debug(f"list_contacts > {contacts}")
        return jsonify(contacts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        result = mongo.db.contacts.insert_one(new_contact)
        app.logger.debug("Contact added successfully")
        return jsonify({'message': 'Contact added successfully', 'id': str(result.inserted_id)}), 200
    except Exception as e:
        app.logger.error(f"Failed to add contact: {e}")
        return jsonify({'error': 'Failed to add contact'}), 500


@app.route('/contacts/<string:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    result = mongo.db.contacts.delete_one({'_id': ObjectId(contact_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Contact not found'}), 404
    return jsonify({'message': 'Contact deleted successfully'}), 200


@app.route('/search/<string:critere>/<string:valeur>', methods=['GET'])
def filter_contacts(critere, valeur):
    app.logger.debug(f"critere ===== {critere}")
    app.logger.debug(f"valeur ===== {valeur}")

    if critere and valeur:
        # Filtrage basé sur le critère et la valeur avec regex pour recherche partielle
        query = {f'propriete.{critere}': {'$regex': valeur, '$options': 'i'}}
        contacts = list(mongo.db.contacts.find(query))
    else:
        # Récupération de tous les contacts si aucun critère n'est spécifié
        contacts = list(mongo.db.contacts.find())
    
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
    
    return jsonify(contacts), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)