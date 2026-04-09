from src.sport import Sport
from src.loader.MatchLoader import MatchLoader

import src.loader.BasketballMatchLoader
import src.loader.FootballMatchLoader
import src.loader.LoLMatchLoader
import src.loader.TennisMatchLoader
import src.loader.VolleyMatchLoader

loader = MatchLoader()

print("=== Bienvenue dans la base de données sportive ===\n")

# Choix du sport
print("Sports disponibles : basketball, football, LOL, tennis, volley")
sport_choisi = input("Quel sport ? ").strip()

# Chargement des matchs
matchs = loader.load_all_matches(Sport(sport_choisi))
print(f"\n{len(matchs)} matchs chargés pour {sport_choisi}\n")

# Choix de la recherche
print("Que voulez-vous chercher ?")
print("1 - Tous les matchs d'une équipe")
print("2 - Matchs entre deux équipes")
print("3 - Matchs à une date précise")
print("4 - Matchs où le score dépasse un certain seuil")
choix = input("\nVotre choix : ").strip()

if choix == "1":
    equipe = input("Nom de l'équipe : ").strip()
    resultats = [m for m in matchs if equipe in m.equipe_1 or equipe in m.equipe_2]

elif choix == "2":
    equipe1 = input("Équipe 1 : ").strip()
    equipe2 = input("Équipe 2 : ").strip()
    resultats = [m for m in matchs if
                (equipe1 in m.equipe_1 and equipe2 in m.equipe_2) or
                (equipe2 in m.equipe_1 and equipe1 in m.equipe_2)]

elif choix == "3":
    date = input("Date (ex: 2022-10-18) : ").strip()
    resultats = [m for m in matchs if date in m.date]

elif choix == "4":
    seuil = float(input("Score minimum : ").strip())
    resultats = [m for m in matchs if m.score_1 >= seuil or m.score_2 >= seuil]

else:
    print("Choix invalide")
    resultats = []

# Affichage des résultats
print(f"\n{len(resultats)} résultat(s) trouvé(s) :\n")
for m in resultats[:20]:
    print(m)
