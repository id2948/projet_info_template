from src.sport import Sport
from src.Model.Joueur import Joueur


class JoueurLoader:
    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader):
        cls._loaders[sport_nom] = loader

    def load_all_joueurs(self, selected_sport: Sport) -> list[Joueur]:
        loader = self._loaders.get(selected_sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader de joueurs enregistré pour '{selected_sport.nom}'")
        return loader().load_all_joueurs()
