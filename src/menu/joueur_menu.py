from src.sport import Sport
from src.loader.JoueurLoader import JoueurLoader
from src.Model.Joueur import Joueur


def run_joueur_menu(sport: Sport) -> None:
    """Menu principal pour tout ce qui concerne les joueurs."""

    loader = JoueurLoader()
    joueurs = loader.load_all_joueurs(sport)
    print(f"\n{len(joueurs)} joueurs chargés pour {sport.nom}\n")

    print("Que voulez-vous faire ?")
    print("1 - Chercher un joueur par nom")
    if sport.nom == "basketball":
        print("2 - Chercher les joueurs d'une équipe")
        print("3 - Chercher les joueurs par position")
    elif sport.nom == "LOL":
        print("2 - Chercher les joueurs d'une équipe")
        print("3 - Chercher les joueurs par rôle")
    elif sport.nom == "tennis":
        print("2 - Chercher les joueurs par pays")
    elif sport.nom == "volley":
        print("2 - Chercher les joueurs par pays")
    print("4 - Statistiques des joueurs")

    choix = input("\nVotre choix : ").strip()

    if choix == "1":
        _chercher_par_nom(joueurs)
    elif choix == "2":
        if sport.nom in ["basketball", "LOL"]:
            _chercher_par_equipe(joueurs)
        elif sport.nom in ["tennis", "volley", "football"]:
            _chercher_par_pays(joueurs)
        else:
            print("Option non disponible pour ce sport.")
    elif choix == "3":
        if sport.nom in ["basketball", "LOL"]:
            _chercher_par_position(joueurs)
        else:
            print("Option non disponible pour ce sport.")
    elif choix == "4":
        _stats_joueurs(joueurs, sport)
    else:
        print("Choix invalide.")


def _chercher_par_nom(joueurs: list[Joueur]) -> None:
    nom = input("Nom du joueur : ").strip()
    resultats = [j for j in joueurs if nom.lower() in j.nom.lower()
                 or (j.prenom and nom.lower() in j.prenom.lower())
                 or (j.pseudo and nom.lower() in j.pseudo.lower())]
    _afficher(resultats)


def _chercher_par_equipe(joueurs: list[Joueur]) -> None:
    equipe = input("Nom de l'équipe : ").strip()
    resultats = [j for j in joueurs if j.equipe and equipe.lower() in j.equipe.lower()]
    _afficher(resultats)


def _chercher_par_position(joueurs: list[Joueur]) -> None:
    position = input("Position (ex: Forward, Center, top, jungle...) : ").strip()
    resultats = [j for j in joueurs if j.position and position.lower() in j.position.lower()]
    _afficher(resultats)


def _chercher_par_pays(joueurs: list[Joueur]) -> None:
    pays = input("Pays : ").strip()
    resultats = [j for j in joueurs if j.pays and pays.lower() in j.pays.lower()]
    _afficher(resultats)


def _stats_joueurs(joueurs: list[Joueur], sport: Sport) -> None:
    if not joueurs:
        print("Aucun joueur disponible.")
        return

    print(f"\n=== Statistiques des joueurs — {sport.nom} ===\n")
    print(f"  Nombre total de joueurs : {len(joueurs)}")

    tailles = [j.taille for j in joueurs if j.taille is not None]
    if tailles:
        print(f"  Taille moyenne          : {sum(tailles) / len(tailles):.1f} cm")
        print(f"  Joueur le plus grand    : {_joueur_max(joueurs, 'taille')}")
        print(f"  Joueur le plus petit    : {_joueur_min(joueurs, 'taille')}")

    poids = [j.poids for j in joueurs if j.poids is not None]
    if poids:
        print(f"  Poids moyen             : {sum(poids) / len(poids):.1f} kg")

    positions = [j.position for j in joueurs if j.position]
    if positions:
        compteur: dict[str, int] = {}
        for p in positions:
            compteur[p] = compteur.get(p, 0) + 1
        print(f"\n  Répartition par position :")
        for pos, nb in sorted(compteur.items(), key=lambda x: -x[1]):
            print(f"    {pos:<15} : {nb} joueurs")

    pays_list = [j.pays for j in joueurs if j.pays]
    if pays_list:
        compteur_pays: dict[str, int] = {}
        for p in pays_list:
            compteur_pays[p] = compteur_pays.get(p, 0) + 1
        top_pays = sorted(compteur_pays.items(), key=lambda x: -x[1])[:5]
        print(f"\n  Top 5 pays représentés :")
        for pays, nb in top_pays:
            print(f"    {pays:<20} : {nb} joueurs")


def _joueur_max(joueurs: list[Joueur], attr: str) -> str:
    j = max((j for j in joueurs if getattr(j, attr) is not None), key=lambda j: getattr(j, attr))
    return f"{j.prenom or ''} {j.nom} ({getattr(j, attr)} cm)".strip()


def _joueur_min(joueurs: list[Joueur], attr: str) -> str:
    j = min((j for j in joueurs if getattr(j, attr) is not None), key=lambda j: getattr(j, attr))
    return f"{j.prenom or ''} {j.nom} ({getattr(j, attr)} cm)".strip()


def _afficher(resultats: list[Joueur], limite: int = 20) -> None:
    print(f"\n{len(resultats)} résultat(s) trouvé(s) :\n")
    for j in resultats[:limite]:
        print(j)
    if len(resultats) > limite:
        print(f"... ({len(resultats) - limite} résultats supplémentaires non affichés)")