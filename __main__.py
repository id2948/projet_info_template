from src.sport import Sport
from src.Model.Match import Match
from src.Model.Joueur import Joueur
from src.Model.Equipe import Equipe
from src.Model.Competition import Competition

import src.loader.BasketballMatchLoader
import src.loader.FootballMatchLoader
import src.loader.LoLMatchLoader
import src.loader.TennisMatchLoader
import src.loader.VolleyMatchLoader

import src.loader.BasketballJoueurLoader
import src.loader.FootballJoueurLoader
import src.loader.LoLJoueurLoader
import src.loader.TennisJoueurLoader
import src.loader.VolleyJoueurLoader

SPORTS_DISPONIBLES = ["basketball", "football", "LOL", "tennis", "volley"]
CATEGORIES_DISPONIBLES = ["match", "joueur", "equipe", "competition"]

print("=== Bienvenue dans la base de données sportive ===\n")

# Choix du sport
print(f"Sports disponibles : {', '.join(SPORTS_DISPONIBLES)}")
sport_choisi = input("Quel sport ? ").strip()

if sport_choisi not in SPORTS_DISPONIBLES:
    print(f"Sport '{sport_choisi}' non reconnu.")
    exit()

# Choix de la catégorie
print(f"\nCatégories disponibles : {', '.join(CATEGORIES_DISPONIBLES)}")
categorie = input("Quelle catégorie ? ").strip().lower()

if categorie == "match":
    Match.run_menu(Sport(sport_choisi))
elif categorie == "joueur":
    Joueur.run_menu(Sport(sport_choisi))
elif categorie == "equipe":
    Equipe.run_menu(Sport(sport_choisi))
elif categorie == "competition":
    Competition.run_menu(Sport(sport_choisi))
else:
    print(f"Catégorie '{categorie}' non reconnue.")
