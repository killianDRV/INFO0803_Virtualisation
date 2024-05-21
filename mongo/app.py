from pymongo import MongoClient

def initialize_db():
    # Connect to MongoDB
    client = MongoClient('mongodb://root:example@mongo:27017/')
    db = client.ma_base_de_donnees

    # Sample data to insert
    sample_data = [
        {'nom': "kiki", 'prenom': "kiki", 'email': "kiki@gmail.com", 'propriete': {'employeur': "univ", 'poste': "univ", 'responsable': "univ"}}
    ]

    # Insert sample data into a collection
    db.contacts.insert_many(sample_data)
    print("Database initialized with sample data")

if __name__ == "__main__":
    initialize_db()
