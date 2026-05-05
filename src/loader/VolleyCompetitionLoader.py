import pandas as pd
from src.Model.Competition import Competition
from src.Model.Equipe import Equipe
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader


class VolleyCompetitionLoader:
    """Affiche les classements de volleyball des JO 2024."""

    DATA_MEN_MATCHES   = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES     = "data/volley/country.csv"

    def run(self) -> None:
        """Charge les données et affiche le menu de classement volleyball."""
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

        comp = Competition(f"Volley {genre} — JO 2024", "volley")
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            for code in [c1, c2]:
                if code not in comp.equipes:
                    comp.ajouter_equipe(code, Equipe(countries.get(code, code), "volley", code))
            comp.equipes[c1].ajouter_match(s1, s2, nul_possible=False)
            comp.equipes[c2].ajouter_match(s2, s1, nul_possible=False)

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_competition(comp, nul_possible=False)
        if nb:
            print(f"  (+ {nb} nouveau(x) résultat(s) inclus dans le classement)")

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires)")
        print("2 - Classement sets gagnés")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Pays':<25}{'MJ':>4}{'V':>4}{'D':>4}{'Sets+':>7}{'Sets-':>7}{'Diff':>7}")
            print("-" * 62)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<25}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>7.0f}{e.score_contre:>7.0f}{e.difference_score:>+7.0f}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Sets gagnés — {comp.nom} ===\n")
            print(f"{'#':<4}{'Pays':<25}{'Sets gagnés':>12}{'Moy/match':>10}")
            print("-" * 54)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<25}{e.score_pour:>12.0f}{moy:>10.2f}")


CompetitionMenuLoader.register("volley", VolleyCompetitionLoader)
