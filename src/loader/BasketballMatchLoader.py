import pandas as pd
from src.sport import Sport
from src.Match import Match


class BasketballMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv("data/basketball/game.csv")
<<<<<<< HEAD
        df = pd.DataFrame({
            "date":        df["game_date"],
            "equipe_1":    df["team_id_home"].astype(str),
            "equipe_2":    df["team_id_away"].astype(str),
            "score_1":     df["pts_home"],
            "score_2":     df["pts_away"],
            "sport":       "basketball",
            "season":      df["season"],
            "season_type": df["season_type"],
        })
        return [Match(**r) for r in df.to_dict("records")]

MatchLoader.register("basketball", BasketballMatchLoader)
=======

        df = pd.DataFrame({
            "equipe_1": df["team_id_home"].astype(str),
            "equipe_2": df["team_id_away"].astype(str),
            "score_1": df["pts_home"],
            "score_2": df["pts_away"],
            "date": df["game_date"],              # optionnel
            "competition": df["season_type"],     # optionnel
        })

        return [Match(**r) for r in df.to_dict("records")]
>>>>>>> c58353b99a41b2fec2e0af0d498193d9a207d15d
