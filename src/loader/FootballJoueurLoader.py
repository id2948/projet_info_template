import pandas as pd
from src.Model.Joueur import Joueur
from src.loader.JoueurLoader import JoueurLoader


class FootballJoueurLoader:
    DATA_PLAYERS = "data/football/player.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df = pd.read_csv(self.DATA_PLAYERS)

        joueurs = []
        for _, row in df.iterrows():
            joueurs.append(Joueur(
                nom=str(row["player_name"]),
                sport="football",
                date_naissance=str(row["birthday"]) if pd.notna(row["birthday"]) else None,
                taille=float(row["height (cm)"]) if pd.notna(row["height (cm)"]) else None,
                poids=float(row["weight (kg)"]) if pd.notna(row["weight (kg)"]) else None,
            ))
        return joueurs


JoueurLoader.register("football", FootballJoueurLoader)