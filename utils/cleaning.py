from typing import Any

import pandas as pd
from email_validator import EmailNotValidError, validate_email

CITIES: list[str] = [
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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the standard cleaning pipeline and remove duplicate rows."""
    df = remove_spaces(df)
    df = manage_none_nan(df)
    df = format_emails(df)
    for col in ["first_name", "last_name", "city"]:
        df[col] = df[col].apply(capitalize_value)
    df = correct_city_names(df)
    df = df.drop_duplicates(keep="first")
    return df


def is_valid_email(email: Any) -> bool:
    """
    Return True if the email address is valid, otherwise False.
    """
    try:
        validate_email(email)
        return True
    except (EmailNotValidError, TypeError):
        return False


def add_valid_mail_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a boolean column indicating whether each email is valid.
    """
    df = df.copy()
    df["is_email_valid"] = df["email"].apply(is_valid_email)
    return df


def get_invalid_emails(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return rows where the email address is invalid.
    """
    return df.loc[~df["is_email_valid"]].copy()


def correct_city_names(
    df: pd.DataFrame,
    city_column: str = "city",
    min_similarity: float = 0.8,
) -> pd.DataFrame:
    """Correct typos in the city column using the known CITIES list."""
    from difflib import get_close_matches

    valid_cities: dict[str, str] = {city.lower(): city for city in CITIES}

    def correct_city(city: Any) -> Any:
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


def remove_spaces(df: pd.DataFrame) -> pd.DataFrame:
    def clean_strings(x: Any) -> Any:
        if isinstance(x, str):
            return x.strip()
        return x

    df = df.map(clean_strings)
    return df


def manage_none_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Convert empty strings and pandas missing values to Python None."""
    df = df.replace({"": None})
    df = df.where(pd.notnull(df), None)
    return df


def format_emails(df: pd.DataFrame) -> pd.DataFrame:
    df["email"] = df["email"].apply(lambda x: x.lower() if x else x)
    return df


def capitalize_value(x: Any) -> Any:
    return x.capitalize() if x else x
