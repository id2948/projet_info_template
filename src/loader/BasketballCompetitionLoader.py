import pandas as pd
from src.Model.Competition import Competition
from src.Model.Equipe import Equipe
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader


class BasketballCompetitionLoader:
    """Affiche les classements NBA pour un type de saison donné."""

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def run(self) -> None:
        """Charge les données et affiche le menu de classement NBA."""
        df_game = pd.read_csv(self.DATA_GAMES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams   = dict(zip(df_team["id"], df_team["full_name"]))
        abbrevs = dict(zip(df_team["id"], df_team["abbreviation"]))

        print("\nType de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        comp = Competition(f"NBA — {season_type}", "basketball")
        for _, row in df.iterrows():
            hid, aid   = int(row["team_id_home"]), int(row["team_id_away"])
            hpts, apts = int(row["pts_home"]),     int(row["pts_away"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(str(tid), Equipe(teams.get(tid, str(tid)), "basketball", abbrevs.get(tid)))
            eh = comp.equipes[str(hid)]
            ea = comp.equipes[str(aid)]
            eh.ajouter_match(hpts, apts, nul_possible=False)
            ea.ajouter_match(apts, hpts, nul_possible=False)
            eh.rebonds       += float(row["reb_home"] or 0)
            eh.passes        += float(row["ast_home"] or 0)
            eh.interceptions += float(row["stl_home"] or 0)
            eh.contres       += float(row["blk_home"] or 0)
            ea.rebonds       += float(row["reb_away"] or 0)
            ea.passes        += float(row["ast_away"] or 0)
            ea.interceptions += float(row["stl_away"] or 0)
            ea.contres       += float(row["blk_away"] or 0)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_competition(comp, nul_possible=False)
        if nb:
            print(f"  (+ {nb} nouveau(x) résultat(s) inclus dans le classement)")

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires)")
        print("2 - Meilleures attaques")
        print("3 - Meilleures défenses")
        print("4 - Classement rebonds")
        print("5 - Classement passes décisives")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Pts+':>6}{'Pts-':>6}{'Diff':>7}")
            print("-" * 65)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>6.0f}{e.score_contre:>6.0f}{e.difference_score:>+7.0f}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Meilleures attaques — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Pts total':>10}{'Moy/match':>10}")
            print("-" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_pour:>10.0f}{moy:>10.1f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: e.score_contre)
            print(f"\n=== Meilleures défenses — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Pts enc.':>10}{'Moy/match':>10}")
            print("-" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_contre / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_contre:>10.0f}{moy:>10.1f}")
        elif choix == "4":
            cl = comp.classement_par("rebonds")
            print(f"\n=== Classement rebonds — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Rebonds':>8}{'Moy/match':>10}")
            print("-" * 55)
            for i, e in enumerate(cl, 1):
                moy = e.rebonds / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.rebonds:>8.0f}{moy:>10.1f}")
        elif choix == "5":
            cl = comp.classement_par("passes")
            print(f"\n=== Classement passes — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Passes':>8}{'Moy/match':>10}")
            print("-" * 55)
            for i, e in enumerate(cl, 1):
                moy = e.passes / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.passes:>8.0f}{moy:>10.1f}")


CompetitionMenuLoader.register("basketball", BasketballCompetitionLoader)
