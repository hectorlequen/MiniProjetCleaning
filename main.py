import pandas as pd

from utils.cleaning import (
    clean_data,
)

df = pd.read_csv("data/input.csv")

print(df)


df = clean_data(df)


print(df)
