import pandas as pd
from sport import Sport
from match import Match

class BasketballMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv("data/basketball/game.csv")
        df = pd.DataFrame({
            "date":        df["game_date"],
            "equipe_1":    df["team_id_home"].astype(str),
            "equipe_2":    df["team_id_away"].astype(str),
            "score_1":     df["pts_home"],
            "score_2":     df["pts_away"],
            "sport":       Sport.BASKETBALL.value,
            "season":      df["season"],
            "season_type": df["season_type"],
        })

        return [Match(**r) for r in df.to_dict("records")]