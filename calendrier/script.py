import requests
from ics import Calendar, Event
from datetime import timedelta
import os

# Décalage horaire
DECALAGE = timedelta(hours=-2)

# Dossier du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def generer_calendrier(url, nom_fichier):
    print(f"Génération de {nom_fichier}...")

    response = requests.get(url)
    response.raise_for_status()

    calendar = Calendar(response.text)
    filtered_calendar = Calendar()

    for event in calendar.events:
        if "Repos hebdomadaire" not in event.name:
            new_event = Event()
            new_event.name = event.name
            new_event.begin = event.begin + DECALAGE
            new_event.end = event.end + DECALAGE
            new_event.description = event.description
            new_event.location = event.location
            new_event.uid = event.uid

            filtered_calendar.events.add(new_event)

    output_path = os.path.join(SCRIPT_DIR, nom_fichier)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(filtered_calendar.serialize_iter())

    print(f"{nom_fichier} généré.")


# =====================
# Calendriers à générer
# =====================

CALENDRIERS = [
    (
        "https://api.skello.io/users/1625132/feeds/ics/919588_47744_924010597.ics",
        "skello_filtré.ics",
    ),
    (
        "https://api.skello.io/users/919155/feeds/ics/235677309781_1485589239_6.ics",
        "skello_filtré_manon.ics",
    ),
]

for url, fichier in CALENDRIERS:
    generer_calendrier(url, fichier)

print("Tous les calendriers ont été générés.")