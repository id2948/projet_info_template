import pandas as pd
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader


class LOLMatchLoader:
    """Charge les matchs de League of Legends."""

    DATA_MATCHES = "data/LOL/match.csv"

    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv(self.DATA_MATCHES)

        df_out = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["team_blue"],
            "equipe_2": df["team_red"],
            "score_1":  df["kills_team_blue"],
            "score_2":  df["kills_team_red"],
            "sport":    "LOL",
            "patch":    df["patch"],
            "week":     df["week"],
            "winner":   df["winner"],
        })

        return [Match(**r) for r in df_out.to_dict("records")]


MatchLoader.register("LOL", LOLMatchLoader)
