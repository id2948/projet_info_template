import pandas as pd
from src.Model.Competition import Competition
from src.Model.Equipe import Equipe
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader


class TennisCompetitionLoader:
    """Affiche les classements du circuit tennis ATP/WTA 2024."""

    DATA_ATP_MATCHES = "data/tennis/atp_matches_2024.csv"
    DATA_WTA_MATCHES = "data/tennis/wta_matches_2024.csv"
    DATA_ATP_PLAYERS = "data/tennis/atp_players_2024.csv"
    DATA_WTA_PLAYERS = "data/tennis/wta_players_2024.csv"

    def run(self) -> None:
        """Charge les données et affiche le menu de classement tennis."""
        df_atp_p = pd.read_csv(self.DATA_ATP_PLAYERS)
        df_wta_p = pd.read_csv(self.DATA_WTA_PLAYERS)
        df_atp_m = pd.read_csv(self.DATA_ATP_MATCHES)
        df_wta_m = pd.read_csv(self.DATA_WTA_MATCHES)

        atp_players = dict(zip(df_atp_p["player_id"].astype(str),
                               df_atp_p["name_first"] + " " + df_atp_p["name_last"]))
        wta_players = dict(zip(df_wta_p["player_id"].astype(str),
                               df_wta_p["name_first"] + " " + df_wta_p["name_last"]))

        circuit = input("\nCircuit (ATP / WTA) : ").strip().upper()
        if circuit == "ATP":
            df_m, players = df_atp_m, atp_players
        elif circuit == "WTA":
            df_m, players = df_wta_m, wta_players
        else:
            print("Circuit invalide.")
            return

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général par victoires")
        print("2 - Classement par tournoi")
        choix = input("\nVotre choix : ").strip()

        if choix == "2":
            tournois = list(df_m["tourney_name"].unique())
            print("\nTournois disponibles :")
            for i, t in enumerate(tournois[:20], 1):
                print(f"  {i}. {t}")
            try:
                idx = int(input("Numéro du tournoi : ").strip()) - 1
                df_m = df_m[df_m["tourney_name"] == tournois[idx]]
                nom_comp = tournois[idx]
            except (ValueError, IndexError):
                print("Choix invalide.")
                return
        else:
            nom_comp = f"{circuit} 2024"

        comp = Competition(nom_comp, "tennis")
        for _, row in df_m.iterrows():
            wid = str(int(row["winner_id"]))
            lid = str(int(row["loser_id"]))
            for pid in [wid, lid]:
                if pid not in comp.equipes:
                    comp.ajouter_equipe(pid, Equipe(players.get(pid, pid), "tennis"))
            comp.equipes[wid].ajouter_match(1, 0, nul_possible=False)
            comp.equipes[lid].ajouter_match(0, 1, nul_possible=False)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_competition(comp, nul_possible=False)
        if nb:
            print(f"  (+ {nb} nouveau(x) résultat(s) inclus dans le classement)")

        cl = comp.classement_par("victoires")
        print(f"\n=== {comp.nom} ===\n")
        print(f"{'#':<4}{'Joueur':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
        print("-" * 52)
        for i, e in enumerate(cl[:20], 1):
            print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}"
                  f"{e.defaites:>4}{e.winrate:>6.1f}%")


CompetitionMenuLoader.register("tennis", TennisCompetitionLoader)
