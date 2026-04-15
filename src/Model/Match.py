from typing import Optional
from src.sport import Sport


class Match:

    def __init__(
        self,
        date:         str,
        equipe_1:     str,
        equipe_2:     str,
        score_1:      float,
        score_2:      float,
        sport:        str,
        season:       Optional[str] = None,
        season_type:  Optional[str] = None,
        league_id:    Optional[float] = None,
        stage:        Optional[str] = None,
        patch:        Optional[str] = None,
        week:         Optional[int] = None,
        winner:       Optional[str] = None,
        tourney_name: Optional[str] = None,
        surface:      Optional[str] = None,
        round:        Optional[str] = None,
    ):
        self.date = date
        self.equipe_1 = equipe_1
        self.equipe_2 = equipe_2
        self.score_1 = score_1
        self.score_2 = score_2
        self.sport = sport
        self.season = season
        self.season_type = season_type
        self.league_id = league_id
        self.stage = stage
        self.patch = patch
        self.week = week
        self.winner = winner
        self.tourney_name = tourney_name
        self.surface = surface
        self.round = round

    def __str__(self):
        return (f"[{self.sport}] {self.date} | "
                f"{self.equipe_1} {self.score_1} - {self.score_2} {self.equipe_2}")

    @staticmethod
    def run_menu(sport: Sport) -> None:
        from src.loader.MatchLoader import MatchLoader
        loader = MatchLoader()
        matchs = loader.load_all_matches(sport)
        print(f"\n{len(matchs)} matchs chargés pour {sport.nom}\n")

        print("Que voulez-vous faire ?")
        print("1 - Chercher les matchs d'une équipe")
        print("2 - Chercher les matchs entre deux équipes")
        print("3 - Chercher les matchs à une date précise")
        print("4 - Chercher les matchs où le score dépasse un seuil")
        print("5 - Statistiques agrégées")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            Match._matchs_equipe(matchs)
        elif choix == "2":
            Match._matchs_entre_deux_equipes(matchs)
        elif choix == "3":
            Match._matchs_par_date(matchs)
        elif choix == "4":
            Match._matchs_par_score(matchs)
        elif choix == "5":
            Match._stats_agregeees(matchs, sport)
        else:
            print("Choix invalide.")

    @staticmethod
    def _matchs_equipe(matchs: list) -> None:
        equipe = input("Nom de l'équipe : ").strip()
        resultats = [m for m in matchs if equipe.lower() in m.equipe_1.lower()
                     or equipe.lower() in m.equipe_2.lower()]
        Match._afficher(resultats)

    @staticmethod
    def _matchs_entre_deux_equipes(matchs: list) -> None:
        equipe1 = input("Équipe 1 : ").strip()
        equipe2 = input("Équipe 2 : ").strip()
        resultats = [m for m in matchs if
                     (equipe1.lower() in m.equipe_1.lower() and
                      equipe2.lower() in m.equipe_2.lower()) or
                     (equipe2.lower() in m.equipe_1.lower() and
                      equipe1.lower() in m.equipe_2.lower())]
        Match._afficher(resultats)

    @staticmethod
    def _matchs_par_date(matchs: list) -> None:
        date = input("Date (ex: 2022-10-18) : ").strip()
        resultats = [m for m in matchs if date in str(m.date)]
        Match._afficher(resultats)

    @staticmethod
    def _matchs_par_score(matchs: list) -> None:
        try:
            seuil = float(input("Score minimum : ").strip())
        except ValueError:
            print("Score invalide.")
            return
        resultats = [m for m in matchs if m.score_1 >= seuil or m.score_2 >= seuil]
        Match._afficher(resultats)

    @staticmethod
    def _stats_agregeees(matchs: list, sport: Sport) -> None:
        if not matchs:
            print("Aucun match disponible.")
            return

        equipe_filtre = input("Filtrer sur une équipe ? (laissez vide pour tout) : ").strip()
        if equipe_filtre:
            matchs_filtres = [m for m in matchs if equipe_filtre.lower() in m.equipe_1.lower()
                              or equipe_filtre.lower() in m.equipe_2.lower()]
            if not matchs_filtres:
                print(f"Aucun match trouvé pour '{equipe_filtre}'.")
                return
            titre = f"{sport.nom} — {equipe_filtre}"
        else:
            matchs_filtres = matchs
            equipe_filtre = None
            titre = sport.nom

        match_record = max(matchs_filtres, key=lambda m: (m.score_1 or 0) + (m.score_2 or 0))

        print(f"\n=== Statistiques des matchs — {titre} ===\n")
        print(f"  Nombre total de matchs   : {len(matchs_filtres)}")
        print(f"  Match le plus prolifique : {match_record}")

        if equipe_filtre:
            victoires = 0
            defaites = 0
            nuls = 0
            points_marques = []
            points_encaisses = []

            matchs_tries = sorted(matchs_filtres, key=lambda m: str(m.date))
            serie_actuelle = 0
            serie_max = 0

            for m in matchs_tries:
                if equipe_filtre.lower() in m.equipe_1.lower():
                    marques = m.score_1 or 0
                    encaisses = m.score_2 or 0
                else:
                    marques = m.score_2 or 0
                    encaisses = m.score_1 or 0

                points_marques.append(marques)
                points_encaisses.append(encaisses)

                if marques > encaisses:
                    victoires += 1
                    serie_actuelle += 1
                    serie_max = max(serie_max, serie_actuelle)
                elif marques < encaisses:
                    defaites += 1
                    serie_actuelle = 0
                else:
                    nuls += 1
                    serie_actuelle = 0

            moy_marques = sum(points_marques) / len(points_marques) if points_marques else 0
            moy_encaisses = sum(points_encaisses) / len(points_encaisses) if points_encaisses else 0

            print(f"  Victoires                : {victoires}")
            print(f"  Défaites                 : {defaites}")
            if nuls > 0:
                print(f"  Nuls                     : {nuls}")
            print(f"  Moyenne points marqués   : {moy_marques:.1f}")
            print(f"  Moyenne points encaissés : {moy_encaisses:.1f}")
            print(f"  Série de victoires max   : {serie_max}")

    @staticmethod
    def _afficher(resultats: list, limite: int = 20) -> None:
        print(f"\n{len(resultats)} résultat(s) trouvé(s) :\n")
        for m in resultats[:limite]:
            print(m)
        if len(resultats) > limite:
            print(f"... ({len(resultats) - limite} résultats supplémentaires non affichés)")
