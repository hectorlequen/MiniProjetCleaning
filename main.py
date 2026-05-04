import pandas as pd
from utils.cleaning import add_valid_mail_column

    
df = pd.read_csv("data/input.csv")

df.drop_duplicates(keep="first")
add_valid_mail_column(df)

print(df)

