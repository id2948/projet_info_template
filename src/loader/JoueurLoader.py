from src.sport import Sport
from src.Model.Joueur import Joueur


class JoueurLoader:
    """Dispatcher qui délègue le chargement des joueurs au loader du sport concerné.

    Les loaders spécifiques s'enregistrent via `register` au moment de leur import.
    """

    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader) -> None:
        """Enregistre un loader de joueurs pour un sport donné.

        Parameters
        ----------
        sport_nom : str
            Nom du sport (ex : "basketball", "tennis").
        loader : type
            Classe loader à instancier pour charger les joueurs.
        """
        cls._loaders[sport_nom] = loader

    def load_all_joueurs(self, selected_sport: Sport) -> list[Joueur]:
        """Charge tous les joueurs du sport sélectionné.

        Parameters
        ----------
        selected_sport : Sport
            Sport dont on veut charger les joueurs.

        Returns
        -------
        list[Joueur]
            Liste de tous les joueurs disponibles pour ce sport.

        Raises
        ------
        Exception
            Si aucun loader n'est enregistré pour le sport demandé.
        """
        loader = self._loaders.get(selected_sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader de joueurs enregistré pour '{selected_sport.nom}'")
        return loader().load_all_joueurs()
