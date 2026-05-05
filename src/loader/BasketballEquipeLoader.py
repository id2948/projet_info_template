import pandas as pd
from src.Model.Equipe import Equipe
from src.loader.EquipeMenuLoader import EquipeMenuLoader


class BasketballEquipeLoader:
    """Affiche les statistiques d'une équipe NBA pour un type de saison donné."""

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def run(self) -> None:
        """Charge les données et affiche les stats pour une équipe NBA."""
        df_game = pd.read_csv(self.DATA_GAMES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams   = dict(zip(df_team["id"], df_team["full_name"]))

        print("\nType de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        nom = input("Nom de l'équipe : ").strip()
        team_matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not team_matches:
            print("Aucune équipe trouvée.")
            return
        team_id = list(team_matches.keys())[0]

        df = df[(df["team_id_home"] == team_id) | (df["team_id_away"] == team_id)]
        e = Equipe(teams.get(team_id, str(team_id)), "basketball")
        for _, row in df.iterrows():
            if int(row["team_id_home"]) == team_id:
                e.ajouter_match(int(row["pts_home"]), int(row["pts_away"]), nul_possible=False)
                e.rebonds       += float(row["reb_home"] or 0)
                e.passes        += float(row["ast_home"] or 0)
                e.interceptions += float(row["stl_home"] or 0)
                e.contres       += float(row["blk_home"] or 0)
            else:
                e.ajouter_match(int(row["pts_away"]), int(row["pts_home"]), nul_possible=False)
                e.rebonds       += float(row["reb_away"] or 0)
                e.passes        += float(row["ast_away"] or 0)
                e.interceptions += float(row["stl_away"] or 0)
                e.contres       += float(row["blk_away"] or 0)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        mj = e.matchs_joues
        print(f"\n=== {e.nom} — {season_type} ===\n")
        print(f"  Matchs joués     : {mj}")
        print(f"  Victoires        : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Points marqués   : {e.score_pour:.0f}  (moy: {e.score_pour/mj:.1f}/match)")
        print(f"  Points encaissés : {e.score_contre:.0f}  (moy: {e.score_contre/mj:.1f}/match)")
        print(f"  Rebonds          : {e.rebonds:.0f}  (moy: {e.rebonds/mj:.1f}/match)")
        print(f"  Passes décisives : {e.passes:.0f}  (moy: {e.passes/mj:.1f}/match)")
        print(f"  Interceptions    : {e.interceptions:.0f}  (moy: {e.interceptions/mj:.1f}/match)")
        print(f"  Contres          : {e.contres:.0f}  (moy: {e.contres/mj:.1f}/match)")


EquipeMenuLoader.register("basketball", BasketballEquipeLoader)
