import pandas as pd
from src.Model.Joueur import Joueur
from src.loader.JoueurLoader import JoueurLoader


class LoLJoueurLoader:
    DATA_PLAYERS = "data/LOL/player.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df = pd.read_csv(self.DATA_PLAYERS)

        joueurs = []
        for _, row in df.iterrows():
            joueurs.append(Joueur(
                nom=str(row["name"]),
                sport="LOL",
                pseudo=str(row["pseudo"]) if pd.notna(row["pseudo"]) else None,
                equipe=str(row["team"]) if pd.notna(row["team"]) else None,
                position=str(row["role"]) if pd.notna(row["role"]) else None,
                date_naissance=str(row["birthdate"]) if pd.notna(row["birthdate"]) else None,
                pays=str(row["country_of_birth"]) if pd.notna(row["country_of_birth"]) else None,
            ))
        return joueurs


JoueurLoader.register("LOL", LoLJoueurLoader)