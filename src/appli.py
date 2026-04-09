from src.sport import Sport
from src.competition import Competition

sport_selected = [
    Sport("football"),
    Sport("LOL"),
    Sport("tennis"),
    Sport("volley"),
    Sport("basketball")
]

sports_names = [s.nom for s in sport_selected]

choice = input(f"Choisissez un sport {sports_names} : ")

if choice not in sports_names:
    raise ValueError(f"'{choice}' n'est pas un sport valide. Choisissez parmi {sports_names}")

sport = next(s for s in sport_selected if s.nom == choice)

competitions = sport.competitions  # adapte selon ton attribut
competitions_names = tuple(c.nom for c in competitions)

choice_comp = input(f"Choisissez une compétition {competitions_names} : ")

if choice_comp not in competitions_names:
    raise ValueError(f"'{choice_comp}' n'est pas valide. Choisissez parmi {competitions_names}")

competition = next(c for c in competitions if c.nom == choice_comp)
