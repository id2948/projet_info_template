from src.sport import Sport
from src.loader.MatchLoader import MatchLoader
from src.loader.JoueurLoader import JoueurLoader

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

from src.menu.match_menu import run_match_menu
from src.menu.joueur_menu import run_joueur_menu

SPORTS_DISPONIBLES = ["basketball", "football", "LOL", "tennis", "volley"]
CATEGORIES_DISPONIBLES = ["match", "joueur"]  # à étendre : club, coach...

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
    run_match_menu(Sport(sport_choisi))
elif categorie == "joueur":
    run_joueur_menu(Sport(sport_choisi))
else:
    print(f"Catégorie '{categorie}' non reconnue.")
