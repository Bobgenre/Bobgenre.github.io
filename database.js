// NOUVEAU : Définition de la structure du programme d'entraînement.
// C'est ici que vous définissez vos exercices et leur temps de repos.
const program = {
    "tirage": [
        { "name": "Tractions Normales", "sets": "5", "reps": "3-6", "rest_time": "2 min" },
        { "name": "Rowing à la machine", "sets": "4", "reps": "8-12", "rest_time": "1 min 30" },
        { "name": "Tirage Vertical Prise Large", "sets": "4", "reps": "8-12", "rest_time": "1 min 30" },
        { "name": "Curl Biceps à la barre EZ", "sets": "3", "reps": "10-12", "rest_time": "1 min" }
    ],
    "poussee": [
        { "name": "Dips au poids du corps", "sets": "4", "reps": "Jusqu'à l'échec", "rest_time": "2 min" },
        { "name": "Développé Couché (Haltères)", "sets": "4", "reps": "8-12", "rest_time": "1 min 30" },
        { "name": "Développé Militaire", "sets": "3", "reps": "8-10", "rest_time": "1 min 30" },
        { "name": "Pompes", "sets": "3", "reps": "Jusqu'à l'échec", "rest_time": "1 min" }
    ],
    "jambes": [
        { "name": "Squat à la barre", "sets": "4", "reps": "8-10", "rest_time": "2 min 30" },
        { "name": "Soulevé de Terre Roumain", "sets": "4", "reps": "10-12", "rest_time": "2 min" },
        { "name": "Fentes Marchées", "sets": "3", "reps": "12-15 par jambe", "rest_time": "1 min 30" },
        { "name": "Relevés de jambes suspendu", "sets": "4", "reps": "10-15", "rest_time": "1 min" },
        { "name": "Gainage", "sets": "3", "reps": "Temps maximum", "rest_time": "1 min" }
    ]
};


// Ce fichier agit comme votre base de données locale.
// Vous pouvez ajouter de nouvelles entrées au tableau "workout_log" pour enregistrer de nouvelles séances.
const mockData = {
    "workout_log": [
        {
            "date": "2025-06-30",
            "type": "Tirage",
            "exercises": [
                { "name": "Tractions Normales", "sets": 5, "reps": [3, 3, 3, 3, 3], "weight": 0 },
                { "name": "Rowing à la machine", "sets": 4, "reps": [8, 8, 8, 8], "weight": 45 },
                { "name": "Tirage Vertical Prise Large", "sets": 4, "reps": [8, 8, 8, 8], "weight": 45 },
                { "name": "Curl Biceps à la barre EZ", "sets": 3, "reps": [8, 8, 8], "weight": 20 }
            ]
        }
    ]
};
