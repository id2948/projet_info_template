from src.sport import Sport
from src.Model.Match import Match


class MatchLoader:
    """Dispatcher qui délègue le chargement des matchs au loader du sport concerné.

    Les loaders spécifiques s'enregistrent via `register` au moment de leur import.
    Les résultats nouvellement ajoutés via ResultatManager sont automatiquement inclus.
    """

    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader) -> None:
        """Enregistre un loader de matchs pour un sport donné.

        Parameters
        ----------
        sport_nom : str
            Nom du sport (ex : "football", "LOL").
        loader : type
            Classe loader à instancier pour charger les matchs.
        """
        cls._loaders[sport_nom] = loader

    def load_all_matches(self, selected_sport: Sport) -> list[Match]:
        """Charge tous les matchs du sport sélectionné, y compris les nouveaux résultats.

        Parameters
        ----------
        selected_sport : Sport
            Sport dont on veut charger les matchs.

        Returns
        -------
        list[Match]
            Liste de tous les matchs disponibles pour ce sport,
            incluant les résultats ajoutés manuellement.

        Raises
        ------
        Exception
            Si aucun loader n'est enregistré pour le sport demandé.
        """
        loader = self._loaders.get(selected_sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader enregistré pour {selected_sport.nom}")
        matchs = loader().load_all_matches()

        from src.loader.ResultatManager import ResultatManager
        nouveaux = ResultatManager.charger(selected_sport.nom)
        return matchs + nouveaux
