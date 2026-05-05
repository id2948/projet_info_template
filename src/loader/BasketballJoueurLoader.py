import pandas as pd
from src.Model.Joueur import Joueur
from src.loader.JoueurLoader import JoueurLoader


class BasketballJoueurLoader:
    """Charge les joueurs NBA depuis les fichiers CSV de basketball."""

    DATA_PLAYERS = "data/basketball/player.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        """Charge et retourne tous les joueurs NBA.

        Résout les noms d'équipes à partir de leurs identifiants et convertit
        les tailles du format pieds-pouces en centimètres.

        Returns
        -------
        list[Joueur]
            Liste des joueurs NBA enrichie des noms d'équipes.
        """
        df_players = pd.read_csv(self.DATA_PLAYERS)
        df_teams = pd.read_csv(self.DATA_TEAMS)

        teams = dict(zip(df_teams["id"].astype(str), df_teams["full_name"]))

        joueurs = []
        for _, row in df_players.iterrows():
            joueurs.append(Joueur(
                nom=str(row["last_name"]),
                prenom=str(row["first_name"]),
                sport="basketball",
                equipe=teams.get(str(row["team_id"]), str(row["team_id"])),
                position=str(row["position"]) if pd.notna(row["position"]) else None,
                date_naissance=str(row["birthdate"]) if pd.notna(row["birthdate"]) else None,
                taille=self._pieds_vers_cm(str(row["height"])),
                poids=float(row["weight"]) * 0.453592 if pd.notna(row["weight"]) else None,
            ))
        return joueurs

    def _pieds_vers_cm(self, valeur: str) -> float | None:
        """Convertit une taille au format pieds-pouces en centimètres.

        Parameters
        ----------
        valeur : str
            Taille au format "pieds-pouces" (ex : "6-8").

        Returns
        -------
        float | None
            Taille en centimètres, ou None si la conversion échoue.
        """
        try:
            pieds, pouces = valeur.split("-")
            return round((int(pieds) * 12 + int(pouces)) * 2.54, 1)
        except Exception:
            return None


JoueurLoader.register("basketball", BasketballJoueurLoader)
