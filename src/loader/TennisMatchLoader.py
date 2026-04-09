import pandas as pd
from src.sport import Sport
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader

class TennisMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df_atp = pd.read_csv("data/tennis/atp_matches_2024.csv")
        df_wta = pd.read_csv("data/tennis/wta_matches_2024.csv")
        df = pd.concat([df_atp, df_wta], ignore_index=True)
        df = pd.DataFrame({
            "date":         df["tourney_date"].astype(str),
            "equipe_1":     df["winner_id"].astype(str),
            "equipe_2":     df["loser_id"].astype(str),
            "score_1":      1,
            "score_2":      0,
            "sport":        Sport.TENNIS.value,
            "tourney_name": df["tourney_name"],
            "surface":      df["surface"],
            "round":        df["round"],
        })
        return [Match(**r) for r in df.to_dict("records")]

MatchLoader.register(Sport.TENNIS, TennisMatchLoader)