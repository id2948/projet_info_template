import pandas as pd
from src.sport import Sport
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader

class FootballMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv("data/football/match.csv")
        df = pd.DataFrame({
            "date":      df["date"],
            "equipe_1":  df["home_team_api_id"].astype(str),
            "equipe_2":  df["away_team_api_id"].astype(str),
            "score_1":   df["home_team_goal"],
            "score_2":   df["away_team_goal"],
            "sport":     Sport.FOOTBALL.value,
            "league_id": df["league_id"],
            "stage":     df["stage"],
        })
        return [Match(**r) for r in df.to_dict("records")]

MatchLoader.register(Sport.FOOTBALL, FootballMatchLoader)