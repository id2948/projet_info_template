import pandas as pd

df = pd.read_csv("data/basketball/player_men.csv")
print(df.columns.tolist())  # affiche toutes les colonnes
print(df.head())             # affiche les 5 premières lignes

