// Connect to mongoDB
conn = new Mongo();
db = conn.getDB("contact_db");

// data to insert
var sample_data = [
    {
        nom: "Darville",
        prenom: "Killian",
        email: "killian.darville@etudiant.univ-reims.fr",
        propriete: {
            employeur: "Université de Reims",
            poste: "Étudiant",
            responsable: "Mr. Fouchal"
        }
    },
    {
        nom: "Goat",
        prenom: "Madippe",
        email: "madippe.goat@RI.com",
        propriete: {
            employeur: "Université de Laon",
            poste: "Étudiant",
            responsable: "Mr. Rabat"
        }
    },
    {
        nom: "Bee",
        prenom: "Alarig",
        email: "alarig@gmail.com",
        propriete: {
            employeur: "Académie de Reims",
            poste: "Intérimaire",
            responsable: "Mr. Pessi"
        }
    }
];

// Insert data into collection
db.contacts.insertMany(sample_data);
print("Database initialized with sample data");