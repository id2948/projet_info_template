import pandas as pd
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader


class FootballMatchLoader:
    """Charge les matchs de football et résout les noms d'équipes."""

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS = "data/football/team.csv"

    def load_all_matches(self) -> list[Match]:
        df_matches = pd.read_csv(self.DATA_MATCHES)
        df_teams = pd.read_csv(self.DATA_TEAMS)

        teams = dict(zip(df_teams["team_api_id"].astype(str), df_teams["team_long_name"]))

        df = pd.DataFrame({
            "date":      df_matches["date"],
            "equipe_1":  df_matches["home_team_api_id"].astype(str).map(teams).fillna(
                df_matches["home_team_api_id"].astype(str)),
            "equipe_2":  df_matches["away_team_api_id"].astype(str).map(teams).fillna(
                df_matches["away_team_api_id"].astype(str)),
            "score_1":   df_matches["home_team_goal"],
            "score_2":   df_matches["away_team_goal"],
            "sport":     "football",
            "league_id": df_matches["league_id"],
            "stage":     df_matches["stage"],
        })

        return [Match(**r) for r in df.to_dict("records")]


MatchLoader.register("football", FootballMatchLoader)
