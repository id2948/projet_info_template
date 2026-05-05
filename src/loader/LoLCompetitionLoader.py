import pandas as pd
from src.Model.Competition import Competition
from src.Model.Equipe import Equipe
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader


class LoLCompetitionLoader:
    """Affiche les classements de la compétition LoL EMEA 2025."""

    DATA_MATCHES = "data/LOL/match.csv"
    DATA_TEAMS   = "data/LOL/team.csv"

    def run(self) -> None:
        """Charge les données et affiche le menu de classement LoL."""
        df      = pd.read_csv(self.DATA_MATCHES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams_info = dict(zip(df_team["team_abbreviation"], df_team["team"]))

        comp = Competition("LoL EMEA 2025", "LOL")
        for _, row in df.iterrows():
            for side, opp in [("blue", "red"), ("red", "blue")]:
                abrev = str(row[f"team_{side}"])
                nom   = teams_info.get(abrev, abrev)
                if abrev not in comp.equipes:
                    comp.ajouter_equipe(abrev, Equipe(nom, "LOL", abrev))
                e = comp.equipes[abrev]
                e.matchs_joues  += 1
                e.kills         += int(row[f"kills_team_{side}"] or 0)
                e.dragons       += int(row[f"dragons_team_{side}"] or 0)
                e.barons        += int(row[f"barons_team_{side}"] or 0)
                e.gold          += float(row[f"gold_team_{side}"] or 0)
                e.score_pour    += int(row[f"kills_team_{side}"] or 0)
                e.score_contre  += int(row[f"kills_team_{opp}"] or 0)
                if str(row["winner"]) == abrev:
                    e.victoires += 1
                    e.points    += 1
                else:
                    e.defaites  += 1

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_competition(comp, nul_possible=False)
        if nb:
            print(f"  (+ {nb} nouveau(x) résultat(s) inclus dans le classement)")

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires / winrate)")
        print("2 - Classement kills")
        print("3 - Classement dragons & barons")
        print("4 - Classement gold")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
            print("-" * 52)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}"
                      f"{e.defaites:>4}{e.winrate:>6.1f}%")
        elif choix == "2":
            cl = comp.classement_par("kills")
            print(f"\n=== Classement kills — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Kills':>7}{'Moy/match':>10}")
            print("-" * 54)
            for i, e in enumerate(cl, 1):
                moy = e.kills / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.kills:>7}{moy:>10.1f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: -(e.dragons + e.barons))
            print(f"\n=== Classement objectifs — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Dragons':>8}{'Barons':>8}{'Total':>7}")
            print("-" * 60)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.dragons:>8}{e.barons:>8}{e.dragons+e.barons:>7}")
        elif choix == "4":
            cl = comp.classement_par("gold")
            print(f"\n=== Classement gold — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Gold total':>12}{'Moy/match':>12}")
            print("-" * 61)
            for i, e in enumerate(cl, 1):
                moy = e.gold / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.gold:>12.0f}{moy:>12.0f}")


CompetitionMenuLoader.register("LOL", LoLCompetitionLoader)
