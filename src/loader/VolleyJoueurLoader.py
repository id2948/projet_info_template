import pandas as pd
from src.Model.Joueur import Joueur
from src.loader.JoueurLoader import JoueurLoader


class VolleyJoueurLoader:
    """Charge les joueurs de volleyball masculin et féminin depuis les CSV des JO 2024."""

    DATA_MEN     = "data/volley/player_men.csv"
    DATA_WOMEN   = "data/volley/player_women.csv"
    DATA_COUNTRIES = "data/volley/country.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        """Charge et retourne tous les joueurs de volleyball (hommes + femmes).

        Le genre est conservé dans le champ ``equipe`` ("Hommes" / "Femmes")
        pour permettre le filtrage et les statistiques comparées.

        Returns
        -------
        list[Joueur]
            Liste des joueurs avec pays, taille, genre et surnom.
        """
        df_men   = pd.read_csv(self.DATA_MEN)
        df_women = pd.read_csv(self.DATA_WOMEN)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)

        countries = dict(zip(df_countries["code"], df_countries["country"]))

        df_men["genre"]   = "Hommes"
        df_women["genre"] = "Femmes"
        df = pd.concat([df_men, df_women], ignore_index=True)

        joueurs = []
        for _, row in df.iterrows():
            code = str(row["country_code"]) if pd.notna(row["country_code"]) else None
            joueurs.append(Joueur(
                nom=str(row["name"]),
                sport="volley",
                equipe=str(row["genre"]),
                pays=countries.get(code, code) if code else None,
                date_naissance=str(row["birth_date"]) if pd.notna(row["birth_date"]) else None,
                taille=float(row["height"]) if pd.notna(row["height"]) else None,
                pseudo=str(row["nickname"]) if pd.notna(row["nickname"]) and str(row["nickname"]) != "" else None,
            ))
        return joueurs


JoueurLoader.register("volley", VolleyJoueurLoader)
