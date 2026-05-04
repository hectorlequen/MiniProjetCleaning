import pandas as pd

        
    
input_file = pd.read_csv("data/input.csv")

input_file.drop_duplicates(keep="first")

print(input_file)

