from src.sport import Sport


class EquipeMenuLoader:
    """Dispatcher qui délègue les stats d'équipe au loader du sport concerné.

    Les loaders spécifiques s'enregistrent via `register` au moment de leur import.
    """

    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader) -> None:
        """Enregistre un loader de stats d'équipe pour un sport donné.

        Parameters
        ----------
        sport_nom : str
            Nom du sport (ex : "football", "basketball").
        loader : type
            Classe loader à instancier.
        """
        cls._loaders[sport_nom] = loader

    def run(self, sport: Sport) -> None:
        """Lance le menu de stats d'équipe pour le sport sélectionné.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        loader = self._loaders.get(sport.nom)
        if loader is None:
            print(f"Pas de stats d'équipe disponibles pour {sport.nom}.")
            return
        loader().run()
