from src.sport import Sport
from src.Model.Match import Match
from src.Model.Joueur import Joueur
from src.Model.Equipe import Equipe
from src.Model.Competition import Competition

import src.loader.MatchLoader       # noqa: F401
import src.loader.JoueurLoader      # noqa: F401
import src.loader.EquipeLoader      # noqa: F401
import src.loader.CompetitionLoader  # noqa: F401

SPORTS_DISPONIBLES = ["basketball", "football", "LOL", "tennis", "volley"]

CATEGORIES = {
    "match":       "Résultats et statistiques de matchs",
    "joueur":      "Recherche et statistiques des joueurs",
    "equipe":      "Statistiques d'une équipe",
    "competition": "Classements de la compétition",
    "graphiques":  "Graphiques et classements visuels (PNG)",
    "ajouter":     "Enregistrer le résultat d'un match",
    "historique":  "Consulter les résultats enregistrés",
}

_SEP2 = "═" * 56


def _entete() -> None:
    """Affiche l'en-tête de l'application."""
    print("\n" + _SEP2)
    print("   Base de données sportive — Résultats & Statistiques")
    print(_SEP2)


def _menu_sport() -> None:
    """Affiche la liste des sports disponibles."""
    print(f"\n  Sports : {' | '.join(SPORTS_DISPONIBLES)}")
    print("  (q pour quitter)\n")


def _menu_categorie(sport: str) -> None:
    """Affiche le menu des catégories pour le sport choisi.

    Parameters
    ----------
    sport : str
        Nom du sport sélectionné.
    """
    print(f"\n  ── {sport.upper()} " + "─" * (50 - len(sport)))
    for cat, desc in CATEGORIES.items():
        print(f"    {cat:<12}  {desc}")
    print("\n  (retour = changer de sport | q = quitter)\n")


def _ajouter_resultat(sport: str) -> None:
    """Saisie guidée d'un nouveau résultat et sauvegarde dans le fichier CSV.

    Le résultat est automatiquement pris en compte dans toutes les statistiques.

    Parameters
    ----------
    sport : str
        Nom du sport pour lequel enregistrer le résultat.
    """
    from src.loader.GestionResultats import GestionResultats
    print(f"\n  ── Enregistrer un résultat — {sport.upper()} ──\n")
    try:
        date = input("  Date       (AAAA-MM-JJ) : ").strip()
        equipe_1 = input("  Équipe 1               : ").strip()
        equipe_2 = input("  Équipe 2               : ").strip()
        score_1 = float(input(f"  Score  {equipe_1[:18]:<18}: ").strip())
        score_2 = float(input(f"  Score  {equipe_2[:18]:<18}: ").strip())
    except ValueError:
        print("\n  Saisie invalide — résultat non enregistré.")
        return
    if not date or not equipe_1 or not equipe_2:
        print("\n  Tous les champs sont requis.")
        return

    GestionResultats.sauvegarder(sport, date, equipe_1, equipe_2, score_1, score_2)
    if score_1 > score_2:
        vainqueur = equipe_1
    elif score_2 > score_1:
        vainqueur = equipe_2
    else:
        vainqueur = "Match nul"
    print(f"\n  {equipe_1} {score_1:.0f} — {score_2:.0f} {equipe_2}  ({date})")
    print(f"  Vainqueur : {vainqueur}")
    print("  Les stats et classements sont mis à jour automatiquement.")


def _afficher_historique(sport: str) -> None:
    """Affiche tous les résultats enregistrés pour un sport.

    Parameters
    ----------
    sport : str
        Nom du sport dont on veut voir l'historique.
    """
    from src.loader.GestionResultats import GestionResultats
    resultats = GestionResultats.lister(sport)
    print(f"\n  ── Résultats enregistrés — {sport.upper()} ({len(resultats)}) ──\n")
    if not resultats:
        print("  Aucun résultat enregistré pour ce sport.")
        return
    for m in resultats:
        if m.score_1 > m.score_2:
            flag = ">"
        elif m.score_2 > m.score_1:
            flag = "<"
        else:
            flag = "="
        print(f"  {m.date}  {m.equipe_1:<25} {m.score_1:.0f} {flag} {m.score_2:.0f}  {m.equipe_2}")


def _executer_categorie(categorie: str, sport: Sport, sport_saisi: str) -> None:
    """Lance l'action correspondant à la catégorie choisie.

    Parameters
    ----------
    categorie : str
        Catégorie saisie par l'utilisateur.
    sport : Sport
        Sport sélectionné.
    sport_saisi : str
        Nom brut du sport (pour GestionResultats).
    """
    if categorie == "match":
        Match.run_menu(sport)
    elif categorie == "joueur":
        Joueur.run_menu(sport)
    elif categorie == "equipe":
        Equipe.run_menu(sport)
    elif categorie == "competition":
        Competition.run_menu(sport)
    elif categorie == "graphiques":
        from src.visualizer.GraphiquesSport import run_menu as graph_menu
        graph_menu(sport_saisi)
    elif categorie == "ajouter":
        _ajouter_resultat(sport_saisi)
    elif categorie == "historique":
        _afficher_historique(sport_saisi)


def _boucle_categorie(sport: Sport, sport_saisi: str) -> bool:
    """Boucle sur le menu des catégories pour un sport donné.

    Parameters
    ----------
    sport : Sport
        Sport sélectionné.
    sport_saisi : str
        Nom brut du sport.

    Returns
    -------
    bool
        True si l'utilisateur veut quitter l'application, False pour revenir.
    """
    while True:
        _menu_categorie(sport_saisi)
        categorie = input("  Quelle catégorie ? ").strip().lower()

        if categorie in ("q", "quitter"):
            print("\n  Au revoir \n")
            return True
        if categorie in ("retour", "r"):
            return False
        if categorie not in CATEGORIES:
            print(f"\n  Catégorie « {categorie} » non reconnue.\n")
            continue

        print()
        _executer_categorie(categorie, sport, sport_saisi)


def main() -> None:
    """Point d'entrée de l'application — boucle interactive principale."""
    _entete()

    while True:
        _menu_sport()
        sport_saisi = input("  Quel sport ? ").strip()

        if sport_saisi.lower() in ("q", "quitter"):
            print("\n  Au revoir !\n")
            break

        if sport_saisi not in SPORTS_DISPONIBLES:
            print(f"\n  Sport « {sport_saisi} » non reconnu.\n")
            continue

        sport = Sport(sport_saisi)
        if _boucle_categorie(sport, sport_saisi):
            return


if __name__ == "__main__":
    main()
