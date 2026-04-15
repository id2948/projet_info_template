from src.sport import Sport
from src.Model.Match import Match


class MatchLoader:
    _loaders = {}

    @classmethod
    def register(cls, sport_nom: str, loader):
        cls._loaders[sport_nom] = loader

    def load_all_matches(self, selected_sport: Sport) -> list[Match]:
        loader = self._loaders.get(selected_sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader enregistré pour {selected_sport.nom}")
        return loader().load_all_matches()
