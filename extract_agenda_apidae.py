import requests
import json
from datetime import datetime, timedelta

# Identifiants Apidae
API_KEY = "HCL87NKU"
PROJET_ID = 8844

# Période souhaitée
date_debut = datetime.today().strftime("%Y-%m-%d")
date_fin = (datetime.today() + timedelta(days=180)).strftime("%Y-%m-%d")

# URL correcte de l’API Apidae
url = "https://api.apidae-tourisme.com/api/v002/objets-touristiques/list"

# Corps de la requête POST
payload = {
    "rechercheTab": {
        "criteres": [
            {
                "critereType": "TYPE_OBJET",
                "valeurs": [2898]  # ID Apidae pour FETE_ET_MANIFESTATION
            }
        ],
        "dateDebut": date_debut,
        "dateFin": date_fin
    },
    "projetId": PROJET_ID,
    "apiKey": API_KEY,
    "champs": [
        "id", "nom", "presentation", "localisation.commune", "informations.dateDebut",
        "informations.dateFin", "illustrations", "multiMotsCles"
    ],
    "traductionFichiers": True,
    "size": 100
}

headers = {
    "Content-Type": "application/json"
}

# Appel API POST
response = requests.post(url, headers=headers, json=payload)

try:
    objets = response.json().get("objetsTouristiques", [])
    resultats = []

    for obj in objets:
        evenement = {
            "id": obj.get("id"),
            "nom": obj.get("nom", {}).get("libelleFr", "Nom inconnu"),
            "date_debut": obj.get("informations", {}).get("dateDebut", ""),
            "date_fin": obj.get("informations", {}).get("dateFin", ""),
            "lieu": obj.get("localisation", {}).get("commune", {}).get("libelleFr", ""),
            "description": obj.get("presentation", {}).get("descriptifCourt", {}).get("libelleFr", ""),
            "themes": [mc.get("libelleFr", "") for mc in obj.get("multiMotsCles", [])],
            "image": obj.get("illustrations", [{}])[0]
                .get("traductionFichiers", {}).get("fr", {}).get("url", "")
        }


    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(resultats)} événements enregistrés dans agenda.json")

except Exception as e:
    print("❌ Erreur :", e)
    print("🔍 Réponse brute :", response.text[:1000])
