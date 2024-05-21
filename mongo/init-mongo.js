// Connect to mongoDB
conn = new Mongo();
db = conn.getDB("contact_db");

// data to insert
var sample_data = [
    {
        nom: "kiki",
        prenom: "kiki",
        email: "kiki@gmail.com",
        propriete: {
            employeur: "univ",
            poste: "univ",
            responsable: "univ"
        }
    }
];

// Insert data into collection
db.contacts.insertMany(sample_data);
print("Database initialized with sample data");