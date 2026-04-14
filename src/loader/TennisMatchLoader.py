import pandas as pd
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader


class TennisMatchLoader:
    """Charge les matchs ATP et WTA 2024 avec les noms des joueurs résolus."""

    DATA_ATP_MATCHES = "data/tennis/atp_matches_2024.csv"
    DATA_WTA_MATCHES = "data/tennis/wta_matches_2024.csv"
    DATA_ATP_PLAYERS = "data/tennis/atp_players_2024.csv"
    DATA_WTA_PLAYERS = "data/tennis/wta_players_2024.csv"

    def load_all_matches(self) -> list[Match]:
        df_atp_m = pd.read_csv(self.DATA_ATP_MATCHES)
        df_wta_m = pd.read_csv(self.DATA_WTA_MATCHES)
        df_atp_p = pd.read_csv(self.DATA_ATP_PLAYERS)
        df_wta_p = pd.read_csv(self.DATA_WTA_PLAYERS)

        # Dictionnaire player_id -> nom complet
        def build_players(df_p: pd.DataFrame) -> dict:
            return dict(
                zip(
                    df_p["player_id"].astype(str),
                    df_p["name_first"] + " " + df_p["name_last"],
                )
            )

        atp_players = build_players(df_atp_p)
        wta_players = build_players(df_wta_p)

        def process(df: pd.DataFrame, players: dict) -> pd.DataFrame:
            return pd.DataFrame({
                "date":         df["tourney_date"].astype(str),
                "equipe_1":     df["winner_id"].astype(str).map(players).fillna(
                    df["winner_id"].astype(str)),
                "equipe_2":     df["loser_id"].astype(str).map(players).fillna(
                    df["loser_id"].astype(str)),
                "score_1":      1.0,
                "score_2":      0.0,
                "sport":        "tennis",
                "tourney_name": df["tourney_name"],
                "surface":      df["surface"],
                "round":        df["round"],
            })

        df_atp_out = process(df_atp_m, atp_players)
        df_wta_out = process(df_wta_m, wta_players)

        df_all = pd.concat([df_atp_out, df_wta_out], ignore_index=True)

        return [Match(**r) for r in df_all.to_dict("records")]


MatchLoader.register("tennis", TennisMatchLoader)
