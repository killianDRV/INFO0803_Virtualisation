// Connect to mongoDB
conn = new Mongo();
db = conn.getDB("contact_db");

// data to insert
var sample_data = [
    {
        nom: "Killian",
        prenom: "Darville",
        email: "killian.darville@etudiant.univ-reims.fr",
        propriete: {
            employeur: "Université de Reims",
            poste: "Étudiant",
            responsable: "Mr. Fouchal"
        }
    },
    {
        nom: "Madippe",
        prenom: "Goat",
        email: "madippe.goat@RI.com",
        propriete: {
            employeur: "Université de Laon",
            poste: "Étudiant",
            responsable: "Mr. Rabat"
        }
    },
    {
        nom: "Alarig",
        prenom: "bee",
        email: "alarig@gmail.com",
        propriete: {
            employeur: "Académie de Reims",
            poste: "Intérimaire",
            responsable: "Mr. Stanek"
        }
    }
];

// Insert data into collection
db.contacts.insertMany(sample_data);
print("Database initialized with sample data");