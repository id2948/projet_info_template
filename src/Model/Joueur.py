from typing import Optional
from src.sport import Sport


class Joueur:

    def __init__(
        self,
        nom:            str,
        sport:          str,
        prenom:         Optional[str] = None,
        pseudo:         Optional[str] = None,
        equipe:         Optional[str] = None,
        position:       Optional[str] = None,
        date_naissance: Optional[str] = None,
        taille:         Optional[float] = None,
        poids:          Optional[float] = None,
        pays:           Optional[str] = None,
        main:           Optional[str] = None,
    ):
        self.nom = nom
        self.sport = sport
        self.prenom = prenom
        self.pseudo = pseudo
        self.equipe = equipe
        self.position = position
        self.date_naissance = date_naissance
        self.taille = taille
        self.poids = poids
        self.pays = pays
        self.main = main

    def __str__(self):
        parts = []
        if self.prenom:
            parts.append(f"{self.prenom} {self.nom}")
        elif self.pseudo:
            parts.append(f"{self.pseudo} ({self.nom})")
        else:
            parts.append(self.nom)

        if self.equipe:
            parts.append(f"| {self.equipe}")
        if self.pays:
            parts.append(f"| {self.pays}")
        if self.position:
            parts.append(f"| {self.position}")
        if self.taille:
            parts.append(f"| {self.taille} cm")
        if self.date_naissance:
            parts.append(f"| né(e) le {self.date_naissance}")

        return f"[{self.sport}] " + " ".join(parts)

    @staticmethod
    def run_menu(sport: Sport) -> None:
        from src.loader.JoueurLoader import JoueurLoader
        loader = JoueurLoader()
        joueurs = loader.load_all_joueurs(sport)
        print(f"\n{len(joueurs)} joueurs chargés pour {sport.nom}\n")

        print("Que voulez-vous faire ?")
        print("1 - Chercher un joueur par nom")
        if sport.nom in ["basketball", "LOL"]:
            print("2 - Chercher les joueurs d'une équipe")
            print("3 - Chercher les joueurs par position")
        elif sport.nom in ["tennis", "volley", "football"]:
            print("2 - Chercher les joueurs par pays")
        print("4 - Statistiques des joueurs")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            Joueur._chercher_par_nom(joueurs)
        elif choix == "2":
            if sport.nom in ["basketball", "LOL"]:
                Joueur._chercher_par_equipe(joueurs)
            else:
                Joueur._chercher_par_pays(joueurs)
        elif choix == "3":
            if sport.nom in ["basketball", "LOL"]:
                Joueur._chercher_par_position(joueurs)
            else:
                print("Option non disponible pour ce sport.")
        elif choix == "4":
            Joueur._stats(joueurs, sport)
        else:
            print("Choix invalide.")

    @staticmethod
    def _chercher_par_nom(joueurs: list) -> None:
        nom = input("Nom du joueur : ").strip()
        resultats = [j for j in joueurs if nom.lower() in j.nom.lower()
                     or (j.prenom and nom.lower() in j.prenom.lower())
                     or (j.pseudo and nom.lower() in j.pseudo.lower())]
        Joueur._afficher(resultats)

    @staticmethod
    def _chercher_par_equipe(joueurs: list) -> None:
        equipe = input("Nom de l'équipe : ").strip()
        resultats = [j for j in joueurs if j.equipe and equipe.lower() in j.equipe.lower()]
        Joueur._afficher(resultats)

    @staticmethod
    def _chercher_par_position(joueurs: list) -> None:
        position = input("Position (ex: Forward, Center, top, jungle...) : ").strip()
        resultats = [j for j in joueurs if j.position and position.lower() in j.position.lower()]
        Joueur._afficher(resultats)

    @staticmethod
    def _chercher_par_pays(joueurs: list) -> None:
        pays = input("Pays : ").strip()
        resultats = [j for j in joueurs if j.pays and pays.lower() in j.pays.lower()]
        Joueur._afficher(resultats)

    @staticmethod
    def _stats(joueurs: list, sport: Sport) -> None:
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        print(f"\n=== Statistiques des joueurs — {sport.nom} ===\n")
        print(f"  Nombre total de joueurs : {len(joueurs)}")

        tailles = [j.taille for j in joueurs if j.taille is not None]
        if tailles:
            print(f"  Taille moyenne          : {sum(tailles) / len(tailles):.1f} cm")
            plus_grand = max(joueurs, key=lambda j: j.taille if j.taille else 0)
            plus_petit = min(joueurs, key=lambda j: j.taille if j.taille else float('inf'))
            print(
                f"Joueur le plus grand: {plus_grand.prenom or ''} {plus_grand.nom} ({plus_grand.taille} cm)")
            print(
                f"Joueur le plus petit: {plus_petit.prenom or ''} {plus_petit.nom} ({plus_petit.taille} cm)")

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

    @staticmethod
    def _afficher(resultats: list, limite: int = 20) -> None:
        print(f"\n{len(resultats)} résultat(s) trouvé(s) :\n")
        for j in resultats[:limite]:
            print(j)
        if len(resultats) > limite:
            print(f"... ({len(resultats) - limite} résultats supplémentaires non affichés)")