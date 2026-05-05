import pandas as pd
from email_validator import EmailNotValidError, validate_email


def clean_data(df):
    df = remove_spaces(df)
    df = manage_none_nan(df)
    df = format_emails(df)
    for col in ["first_name", "last_name", "city"]:
        df[col] = df[col].apply(capitalize_value)
    df = df.drop_duplicates(keep="first")
    return df


def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def add_valid_mail_column(df):
    _l = []
    for email in df["email"]:
        try:
            _l.append(is_valid_email(email))
        except TypeError:
            _l.append(False)

    df.insert(3, "is_email_valid", _l)
    df_unvalid_emails = df.loc[~df["is_email_valid"]]
    return df_unvalid_emails


def remove_spaces(df):
    def clean_strings(x):
        if isinstance(x, str):
            return x.strip()
        return x

    df = df.map(clean_strings)
    return df


def manage_none_nan(df):
    df = df.replace({"": None})
    df = df.where(pd.notnull(df), None)
    return df


def format_emails(df):
    df["email"] = df["email"].apply(lambda x: x.lower() if x else x)
    return df


def capitalize_value(x):
    return x.capitalize() if x else x
