import pandas as pd
from utils.cleaning import clean_data, remove_spaces, manage_none_nan, format_emails, add_valid_mail_column, capitalize_value

    
df = pd.read_csv("data/input.csv")

print(df)

df = clean_data(df)


print(df)


