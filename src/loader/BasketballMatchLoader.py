import pandas as pd
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader


class BasketballMatchLoader:
    """Charge les matchs de basketball"""

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def load_all_matches(self) -> list[Match]:
        df_games = pd.read_csv(self.DATA_GAMES)
        df_teams = pd.read_csv(self.DATA_TEAMS)

        teams = dict(zip(df_teams["id"].astype(str), df_teams["full_name"]))

        df = pd.DataFrame({
            "date":        df_games["game_date"],
            "equipe_1":    df_games["team_id_home"].astype(str).map(teams).fillna(
                df_games["team_id_home"].astype(str)),
            "equipe_2":    df_games["team_id_away"].astype(str).map(teams).fillna(
                df_games["team_id_away"].astype(str)),
            "score_1":     df_games["pts_home"],
            "score_2":     df_games["pts_away"],
            "sport":       "basketball",
            "season":      df_games["season"],
            "season_type": df_games["season_type"],
        })

        return [Match(**r) for r in df.to_dict("records")]


MatchLoader.register("basketball", BasketballMatchLoader)
