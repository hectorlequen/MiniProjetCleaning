import pandas as pd

from utils.cleaning import (
    add_valid_mail_column,
    clean_data,
    get_invalid_emails,
)

df = pd.read_csv("data/input.csv")


df = clean_data(df)
df = add_valid_mail_column(df)
df_unvalid_emails = get_invalid_emails(df)

df.to_csv("output/cleaned_data.csv", index=False)
df_unvalid_emails.to_csv("output/invalid_emails.csv", index=False)
