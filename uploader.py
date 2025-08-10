import json
import firebase_admin
from firebase_admin import credentials, firestore

def upload_stats_to_firestore(json_file_path, service_account_key_path):
    """
    Lit un fichier JSON de statistiques de joueurs et les envoie à la collection
    'lec-players' dans Firestore.
    """
    # --- Étape 1: Initialisation de Firebase Admin ---
    try:
        cred = credentials.Certificate(service_account_key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Connexion à Firebase réussie.")
    except Exception as e:
        print(f"Erreur d'initialisation de Firebase : {e}")
        print("Vérifiez que le fichier 'serviceAccountKey.json' est correct et au bon endroit.")
        return

    # --- Étape 2: Lecture du fichier JSON local ---
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            players_data = json.load(f)
        print(f"Lecture de {len(players_data)} joueurs depuis '{json_file_path}'.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{json_file_path}' n'a pas été trouvé.")
        print("Assurez-vous d'avoir d'abord exécuté le script de scraping.")
        return
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier '{json_file_path}' est mal formaté ou vide.")
        return

    # --- Étape 3: Envoi des données vers Firestore ---
    # On utilise un "batch" pour envoyer toutes les données en une seule fois, c'est plus efficace.
    batch = db.batch()
    players_collection_ref = db.collection('lec-players')
    
    print("Préparation de l'envoi des données vers Firestore...")
    for player in players_data:
        # L'ID du document dans Firestore sera le nom du joueur (son 'id')
        player_id = player.get('id')
        if not player_id:
            print(f"Avertissement : Joueur sans ID trouvé, ignoré : {player}")
            continue
        
        # Crée une référence au document du joueur
        doc_ref = players_collection_ref.document(player_id)
        # Ajoute l'opération d'écriture au batch
        batch.set(doc_ref, player)

    # --- Étape 4: Exécution du batch ---
    try:
        batch.commit()
        print(f"\nOpération terminée !")
        print(f"{len(players_data)} profils de joueurs ont été envoyés avec succès à la collection 'lec-players'.")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données à Firestore : {e}")


if __name__ == "__main__":
    # Chemin vers les fichiers. Assurez-vous qu'ils sont dans le même dossier.
    JSON_FILE = 'player_stats.json'
    SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json'
    
    upload_stats_to_firestore(JSON_FILE, SERVICE_ACCOUNT_KEY)
