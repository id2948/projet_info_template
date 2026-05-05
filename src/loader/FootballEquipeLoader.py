import pandas as pd
from src.Model.Equipe import Equipe
from src.loader.EquipeMenuLoader import EquipeMenuLoader


class FootballEquipeLoader:
    """Affiche les statistiques d'une équipe de football pour une saison donnée."""

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS   = "data/football/team.csv"

    def run(self) -> None:
        """Charge les données et affiche les stats pour une équipe de football."""
        df_match = pd.read_csv(self.DATA_MATCHES)
        df_team  = pd.read_csv(self.DATA_TEAMS)
        teams    = dict(zip(df_team["team_api_id"], df_team["team_long_name"]))

        nom = input("Nom de l'équipe : ").strip()
        matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not matches:
            print("Aucune équipe trouvée.")
            return
        if len(matches) > 1:
            for tid, tname in matches.items():
                print(f"  {tid} - {tname}")
            try:
                team_id = int(input("ID : ").strip())
            except ValueError:
                return
        else:
            team_id = list(matches.keys())[0]

        saisons = sorted(df_match["season"].unique())
        print("\nSaisons :", ", ".join(saisons))
        saison = input("Saison (ex: 2014/2015) : ").strip()
        if saison not in saisons:
            print("Saison non trouvée.")
            return

        df = df_match[
            ((df_match["home_team_api_id"] == team_id) | (df_match["away_team_api_id"] == team_id)) &
            (df_match["season"] == saison)
        ]
        e = Equipe(teams.get(team_id, str(team_id)), "football")
        for _, row in df.iterrows():
            if int(row["home_team_api_id"]) == team_id:
                e.ajouter_match(int(row["home_team_goal"]), int(row["away_team_goal"]))
            else:
                e.ajouter_match(int(row["away_team_goal"]), int(row["home_team_goal"]))

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_equipe(e, e.nom)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — {saison} ===\n")
        print(f"  Matchs joués   : {e.matchs_joues}")
        print(f"  Victoires      : {e.victoires}  Nuls : {e.nuls}  Défaites : {e.defaites}")
        print(f"  Buts marqués   : {e.score_pour:.0f}  (moy: {e.score_pour/e.matchs_joues:.2f}/match)")
        print(f"  Buts encaissés : {e.score_contre:.0f}  (moy: {e.score_contre/e.matchs_joues:.2f}/match)")
        print(f"  Différence     : {e.difference_score:+.0f}")
        print(f"  Points         : {e.points}")
        print(f"  Winrate        : {e.winrate:.1f}%")


EquipeMenuLoader.register("football", FootballEquipeLoader)
