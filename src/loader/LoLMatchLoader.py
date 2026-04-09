import pandas as pd
from src.sport import Sport
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader

class LOLMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv("data/LOL/match.csv")
        df = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["team_blue"],
            "equipe_2": df["team_red"],
            "score_1":  df["kills_team_blue"],
            "score_2":  df["kills_team_red"],
            "sport":    Sport.LOL.value,
            "patch":    df["patch"],
            "week":     df["week"],
            "winner":   df["winner"],
        })
        return [Match(**r) for r in df.to_dict("records")]

MatchLoader.register(Sport.LOL, LOLMatchLoader)