import pandas as pd
from src.Parsers.parse_csv import parse_csv
from src.Analysis.pandas.GoatFinder import find_the_goat_in_df
from src.Analysis.homemade.GoatFinder import find_the_goat
from src.sport import Sport
from src.loader.MatchLoader import MatchLoader

import src.loader.BasketballMatchLoader
import src.loader.FootballMatchLoader
import src.loader.LoLMatchLoader
import src.loader.TennisMatchLoader
import src.loader.VolleyMatchLoader

loader = MatchLoader()

# Test Basketball
print("=== BASKETBALL ===")
matchs = loader.load_all_matches(Sport.BASKETBALL)
for m in matchs[:3]:
    print(m)

# Test Football
print("\n=== FOOTBALL ===")
matchs = loader.load_all_matches(Sport.FOOTBALL)
for m in matchs[:3]:
    print(m)

# Test LoL
print("\n=== LOL ===")
matchs = loader.load_all_matches(Sport.LOL)
for m in matchs[:3]:
    print(m)

# Test Tennis
print("\n=== TENNIS ===")
matchs = loader.load_all_matches(Sport.TENNIS)
for m in matchs[:3]:
    print(m)

# Test Volley
print("\n=== VOLLEY ===")
matchs = loader.load_all_matches(Sport.VOLLEY)
for m in matchs[:3]:
    print(m)