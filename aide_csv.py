import pandas as pd

df = pd.read_csv("data/basketball/player.csv")

# 1. FILTRES SIMPLES

# Égalité
df[df["position"] == "Forward"]

# Différent
df[df["position"] != "Forward"]

# Supérieur / Inférieur
df[df["weight"] > 250]
df[df["weight"] <= 200]

# 2. FILTRES MULTIPLES

# ET (les deux conditions vraies)
df[(df["position"] == "Forward") & (df["weight"] > 220)]

# OU (au moins une condition vraie)
df[(df["position"] == "Forward") | (df["position"] == "Center")]

# 3. RECHERCHE DANS UNE LISTE

# La valeur est dans cette liste ?
df[df["position"].isin(["Forward", "Center", "Guard"])]

# N'est PAS dans la liste
df[~df["position"].isin(["Forward"])]

# 4. RECHERCHE TEXTE (contient, commence par...)

# Contient un mot (insensible à la casse)
df[df["last_name"].str.contains("ad", case=False)]

# Commence par
df[df["first_name"].str.startswith("S")]

# 5. VALEURS MANQUANTES

# Lignes où une colonne est vide, donne ces collones là
df[df["nickname"].isna()]

# Lignes où la colonne est remplie
df[df["nickname"].notna()]

# 6. TRIER

# Tri croissant
df.sort_values("weight")

# Tri décroissant
df.sort_values("weight", ascending=False)

# Tri sur plusieurs colonnes
df.sort_values(["position", "weight"], ascending=[True, False])

# 7. SÉLECTIONNER DES COLONNES

# Une seule colonne
df["first_name"]

# Plusieurs colonnes
df[["first_name", "last_name", "position"]]

# 8. STATISTIQUES

# Moyenne, min, max, total
df["weight"].mean()
df["weight"].min()
df["weight"].max()
df["weight"].sum()

# Résumé complet
df.describe()

# Compter les valeurs uniques (ex: combien de joueurs par position)
df["position"].value_counts()

# 9. GROUPER (GROUP BY)

# Poids moyen par position
df.groupby("position")["weight"].mean()

# Plusieurs stats à la fois
df.groupby("position")["weight"].agg(["mean", "min", "max", "count"])

# 10. JOINTURE — relier deux fichiers

players = pd.read_csv("data/basketball/player.csv")
teams = pd.read_csv("data/basketball/team.csv")

# Relier les joueurs à leur équipe
resultat = players.merge(teams, left_on="team_id", right_on="id")
print(resultat[["first_name", "last_name", "full_name", "position"]])

# 11. AFFICHAGE

# Nombre de résultats
print(len(df))

# Les 10 premiers
print(df.head(10))

# Les 5 derniers
print(df.tail(5))

# Afficher sans limite de colonnes
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)
