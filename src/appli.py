from src.sport import Sport

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