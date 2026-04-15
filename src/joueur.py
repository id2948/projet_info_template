from datetime import date
from typing import Optional
from team import Equipe
from personne import Personne

class Joueur(Personne):
    """Représente un joueur dans une équipe."""

    def __init__(
        self,
        id: str | None,
        nom: str,
        prénom: str | None,
        date_naissance: date | None = None,
        taille: float | None = None,
        equipe: Optional[Equipe] = None
    ) -> None:
        super().__init__(id, nom, prénom, date_naissance, taille, equipe)

    def __repr__(self) -> str:
        return f"Joueur({super().__repr__()})"


class Coach(Personne):
    """Représente un coach d'équipe."""

    def __init__(
        self,
        id: str | None,
        nom: str,
        prénom: str | None,
        date_naissance: date | None = None,
        taille: float | None = None,
        equipe: Optional[Equipe] = None
    ) -> None:
        super().__init__(id, nom, prénom, date_naissance, taille, equipe)

    def __repr__(self) -> str:
        return f"Coach({super().__repr__()})"