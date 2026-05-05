import pandas as pd
from src.Model.Match import Match
from src.loader.MatchLoader import MatchLoader


class VolleyMatchLoader:
    """Charge les matchs de volleyball masculin et féminin."""

    DATA_MEN_MATCHES = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES = "data/volley/country.csv"

    def load_all_matches(self) -> list[Match]:
        """Charge et retourne tous les matchs de volleyball (hommes + femmes).

        Résout les codes pays en noms complets.

        Returns
        -------
        list[Match]
            Liste des matchs avec noms de pays, sets et phase.
        """
        df_men = pd.read_csv(self.DATA_MEN_MATCHES)
        df_women = pd.read_csv(self.DATA_WOMEN_MATCHES)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)

        countries = dict(zip(df_countries["code"], df_countries["country"]))

        df_men = df_men.rename(columns={"country_code_1": "code_1", "country_code_2": "code_2"})
        df_women = df_women.rename(columns={"country_1":      "code_1", "country_2":      "code_2"})

        df = pd.concat([df_men, df_women], ignore_index=True)

        df_out = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["code_1"].map(countries).fillna(df["code_1"]),
            "equipe_2": df["code_2"].map(countries).fillna(df["code_2"]),
            "score_1":  df["set_country_1"],
            "score_2":  df["set_country_2"],
            "sport":    "volley",
            "stage":    df["stage"],
        })

        return [Match(**r) for r in df_out.to_dict("records")]


MatchLoader.register("volley", VolleyMatchLoader)
