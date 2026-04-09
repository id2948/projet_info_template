import pandas as pd
from src.sport import Sport
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader

class VolleyMatchLoader:
    def load_all_matches(self) -> list[Match]:
        df_men   = pd.read_csv("data/volley/match_men.csv")
        df_women = pd.read_csv("data/volley/match_women.csv")
        df_men   = df_men.rename(columns={"country_code_1": "equipe_1", "country_code_2": "equipe_2"})
        df_women = df_women.rename(columns={"country_1": "equipe_1", "country_2": "equipe_2"})
        df = pd.concat([df_men, df_women], ignore_index=True)
        df = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["equipe_1"],
            "equipe_2": df["equipe_2"],
            "score_1":  df["set_country_1"],
            "score_2":  df["set_country_2"],
            "sport":    "volley",
            "stage":    df["stage"],
        })
        return [Match(**r) for r in df.to_dict("records")]

MatchLoader.register("volley", VolleyMatchLoader)
