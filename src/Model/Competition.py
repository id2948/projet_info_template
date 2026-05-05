from src.sport import Sport
from src.Model.Equipe import Equipe


class Competition:
    """Représente une compétition regroupant des équipes et leurs statistiques.

    Parameters
    ----------
    nom : str
        Nom de la compétition.
    sport : str
        Sport concerné.
    """

    def __init__(self, nom: str, sport: str):
        self.nom = nom
        self.sport = sport
        self.equipes: dict[str, Equipe] = {}

    def ajouter_equipe(self, cle: str, equipe: Equipe) -> None:
        """Ajoute ou remplace une équipe dans la compétition.

        Parameters
        ----------
        cle : str
            Clé d'indexation (ex : identifiant ou abréviation).
        equipe : Equipe
            Instance Equipe à enregistrer.
        """
        self.equipes[cle] = equipe

    def classement_par(self, critere: str) -> list:
        """Trie les équipes selon un attribut de Equipe, du plus grand au plus petit.

        Parameters
        ----------
        critere : str
            Nom d'un attribut de Equipe (ex : "points", "victoires").

        Returns
        -------
        list
            Équipes triées du meilleur au moins bon.
        """
        return sorted(
            self.equipes.values(),
            key=lambda e: getattr(e, critere),
            reverse=True,
        )

    def __repr__(self):
        return f"Competition(nom={self.nom}, sport={self.sport}, equipes={len(self.equipes)})"

    @staticmethod
    def run_menu(sport: Sport) -> None:
        """Affiche le menu de classement pour un sport donné.

        Délègue au loader enregistré pour ce sport via CompetitionLoader.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        from src.loader.CompetitionLoader import CompetitionLoader
        CompetitionLoader().run(sport)
