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
        self.nom    = nom
        self.sport  = sport
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

    def classement_par(self, *criteres) -> list[Equipe]:
        """Trie les équipes selon les critères donnés (attributs de Equipe).

        Parameters
        ----------
        *criteres : str
            Noms d'attributs de Equipe, triés de manière décroissante.

        Returns
        -------
        list[Equipe]
            Équipes triées du meilleur au moins bon.
        """
        return sorted(
            self.equipes.values(),
            key=lambda e: tuple(-getattr(e, c) for c in criteres)
        )

    def __repr__(self):
        return f"Competition(nom={self.nom}, sport={self.sport}, equipes={len(self.equipes)})"

    @staticmethod
    def run_menu(sport: Sport) -> None:
        """Affiche le menu de classement pour un sport donné.

        Délègue au loader enregistré pour ce sport via CompetitionMenuLoader.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        from src.loader.CompetitionMenuLoader import CompetitionMenuLoader
        CompetitionMenuLoader().run(sport)
