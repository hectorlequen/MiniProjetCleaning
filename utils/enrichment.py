import requests


def enrich_city(city):
    r = requests.get(f"https://nominatim.openstreetmap.org/search?q={city}&format=json")
    return r.json()
