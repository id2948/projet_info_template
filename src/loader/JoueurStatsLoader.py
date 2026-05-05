from src.sport import Sport


class JoueurStatsLoader:
    """Dispatcher pour les statistiques détaillées de joueurs.

    Les loaders spécifiques s'enregistrent via `register`.
    Sans loader enregistré, des statistiques génériques sont affichées.
    """

    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader) -> None:
        """Enregistre un loader de stats pour un sport donné.

        Parameters
        ----------
        sport_nom : str
            Nom du sport.
        loader : type
            Classe loader à instancier.
        """
        cls._loaders[sport_nom] = loader

    def run(self, joueurs: list, sport: Sport) -> None:
        """Lance les statistiques pour les joueurs du sport sélectionné.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur déjà chargés.
        sport : Sport
            Sport concerné.
        """
        loader = self._loaders.get(sport.nom)
        if loader is not None:
            loader().run(joueurs)
        else:
            self._stats_generiques(joueurs, sport)

    @staticmethod
    def _stats_generiques(joueurs: list, sport: Sport) -> None:
        """Affiche des statistiques génériques quand aucun loader spécifique n'existe.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur.
        sport : Sport
            Sport concerné.
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return
        print(f"\n=== Statistiques des joueurs — {sport.nom} ===\n")
        print(f"  Nombre total : {len(joueurs)}")
        tailles = [j.taille for j in joueurs if j.taille is not None]
        if tailles:
            print(f"  Taille moyenne : {sum(tailles)/len(tailles):.1f} cm")
        poids = [j.poids for j in joueurs if j.poids is not None]
        if poids:
            print(f"  Poids moyen    : {sum(poids)/len(poids):.1f} kg")
