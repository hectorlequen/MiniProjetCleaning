import pandas as pd

from utils.cleaning import add_valid_mail_column, clean_data
from utils.data_enrichment import correct_city_names

df = pd.read_csv("data/input.csv")


df = clean_data(df)
df = correct_city_names(df)
df_unvalid_emails = add_valid_mail_column(df)

df.to_csv("output/cleaned_data.csv", index=False)
df_unvalid_emails.to_csv("output/unvalid_emails.csv", index=False)
