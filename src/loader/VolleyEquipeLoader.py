import pandas as pd
from src.Model.Equipe import Equipe
from src.loader.EquipeMenuLoader import EquipeMenuLoader


class VolleyEquipeLoader:
    """Affiche les statistiques d'une équipe nationale de volleyball (JO 2024)."""

    DATA_MEN_MATCHES   = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES     = "data/volley/country.csv"

    def run(self) -> None:
        """Charge les données et affiche les stats pour une équipe de volleyball."""
        df_men   = pd.read_csv(self.DATA_MEN_MATCHES)
        df_women = pd.read_csv(self.DATA_WOMEN_MATCHES)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)
        countries = dict(zip(df_countries["code"], df_countries["country"]))

        df_men["code_1"]   = df_men["country_code_1"]
        df_men["code_2"]   = df_men["country_code_2"]
        df_women["code_1"] = df_women["country_1"]
        df_women["code_2"] = df_women["country_2"]

        cat = input("\nCatégorie (Hommes / Femmes) : ").strip().lower()
        df  = df_men if cat in ["hommes", "h", "men"] else df_women
        genre = "Hommes" if cat in ["hommes", "h", "men"] else "Femmes"

        nom = input("Nom du pays : ").strip()
        code_trouve = None
        for code, pays in countries.items():
            if nom.lower() in pays.lower():
                code_trouve = code
                break
        if not code_trouve:
            print("Pays non trouvé.")
            return

        e = Equipe(countries[code_trouve], "volley", code_trouve)
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            if c1 == code_trouve:
                e.ajouter_match(s1, s2, nul_possible=False)
            elif c2 == code_trouve:
                e.ajouter_match(s2, s1, nul_possible=False)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — Volley {genre} JO 2024 ===\n")
        print(f"  Matchs joués : {e.matchs_joues}")
        print(f"  Victoires    : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Sets gagnés  : {e.score_pour:.0f}")
        print(f"  Sets perdus  : {e.score_contre:.0f}")
        print(f"  Différence   : {e.difference_score:+.0f}")


EquipeMenuLoader.register("volley", VolleyEquipeLoader)
