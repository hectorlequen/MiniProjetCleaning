CITIES = [
    "Paris",
    "Lyon",
    "Marseille",
    "Toulouse",
    "Nice",
    "Nantes",
    "Strasbourg",
    "Montpellier",
    "Bordeaux",
    "Lille",
]


def correct_city_names(df, city_column="city", min_similarity=0.8):
    """Correct typos in the city column using the known CITIES list."""
    from difflib import get_close_matches

    valid_cities = {city.lower(): city for city in CITIES}

    def correct_city(city):
        if not city:
            return city

        normalized_city = str(city).strip().lower()
        if normalized_city in valid_cities:
            return valid_cities[normalized_city]

        matches = get_close_matches(
            normalized_city,
            valid_cities.keys(),
            n=1,
            cutoff=min_similarity,
        )
        if matches:
            return valid_cities[matches[0]]

        return city

    df[city_column] = df[city_column].apply(correct_city)
    return df
