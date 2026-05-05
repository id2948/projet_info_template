from src.sport import Sport


class CompetitionMenuLoader:
    """Dispatcher qui délègue les classements au loader du sport concerné.

    Les loaders spécifiques s'enregistrent via `register` au moment de leur import.
    """

    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader) -> None:
        """Enregistre un loader de classement pour un sport donné.

        Parameters
        ----------
        sport_nom : str
            Nom du sport (ex : "football", "LOL").
        loader : type
            Classe loader à instancier.
        """
        cls._loaders[sport_nom] = loader

    def run(self, sport: Sport) -> None:
        """Lance le menu de classement pour le sport sélectionné.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        loader = self._loaders.get(sport.nom)
        if loader is None:
            print(f"Pas de classement disponible pour {sport.nom}.")
            return
        loader().run()
