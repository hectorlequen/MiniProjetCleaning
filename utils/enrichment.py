import logging

import requests

logger = logging.getLogger(__name__)
HEADERS = {"User-Agent": "MiniProjetCleaning/1.0"}


def request_api(city):
    if not city:
        logger.warning("City is empty, skipping enrichment.")
        return None
    r = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={city}&format=json&addressdetails=1",
        headers=HEADERS,
        timeout=5,
    )
    try:
        r.raise_for_status()
    except requests.Timeout:
        logger.error(f"API request timed out for city '{city}'.")
        return None
    except requests.HTTPError as e:
        logger.error(f"API request failed for city '{city}': {e}")
        return None
    except requests.RequestException as e:
        logger.error(f"API request error for city '{city}': {e}")
        return None
    return r.json()


def get_country_from_city(city):
    if not city:
        logger.warning("Failed to enrich city data.")
        return None
    city_data = request_api(city)
    if city_data is None:
        return None
    return city_data[0]["address"]["country"]


def add_country_column(df):
    df = df.copy()
    df["country"] = df["city"].apply(get_country_from_city)
    return df
