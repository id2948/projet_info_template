import pandas as pd
from src.Model.Equipe import Equipe
from src.loader.EquipeMenuLoader import EquipeMenuLoader


class TennisEquipeLoader:
    """Affiche le bilan victoires/défaites d'un joueur de tennis sur le circuit 2024."""

    DATA_ATP_MATCHES = "data/tennis/atp_matches_2024.csv"
    DATA_WTA_MATCHES = "data/tennis/wta_matches_2024.csv"
    DATA_ATP_PLAYERS = "data/tennis/atp_players_2024.csv"
    DATA_WTA_PLAYERS = "data/tennis/wta_players_2024.csv"

    def run(self) -> None:
        """Charge les données et affiche le bilan d'un joueur de tennis."""
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

        nom = input("Nom du joueur : ").strip()
        pid_trouve = None
        for pid, pname in players.items():
            if nom.lower() in pname.lower():
                pid_trouve = pid
                break
        if not pid_trouve:
            print("Joueur non trouvé.")
            return

        e = Equipe(players[pid_trouve], "tennis")
        for _, row in df_m.iterrows():
            wid = str(int(row["winner_id"]))
            lid = str(int(row["loser_id"]))
            if wid == pid_trouve:
                e.ajouter_match(1, 0, nul_possible=False)
            elif lid == pid_trouve:
                e.ajouter_match(0, 1, nul_possible=False)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — {circuit} 2024 ===\n")
        print(f"  Matchs joués : {e.matchs_joues}")
        print(f"  Victoires    : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")


EquipeMenuLoader.register("tennis", TennisEquipeLoader)
