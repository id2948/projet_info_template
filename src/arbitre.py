from individu import Individu


class Arbitre(Individu):
    """Modélise les arbitres parmi les individus dans la compétition."""

    def __init__(self, id: str, nom: str, prenom: str) -> None:
        Individu.__init__(self, id, nom, prenom)
