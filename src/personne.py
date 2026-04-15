from datetime import date
from typing import Optional

from equipe import Equipe


class Personne:
    """Permet de modéliser un participant dans la compétition.

    Parameters
    ----------
    id: str | None
        identifiant dans la compétition du participant

    nom: str
        nom complet ou nom de famille

    prénom: str | None
        prénom si disponible

    date_naissance: date | None
        date de naissance du participant

    taille: float | None
        taille en cm ou mètres selon ton choix

    equipe: Equipe | None
        équipe à laquelle appartient la personne
    """

    def __init__(
        self,
        id: str | None,
        nom: str,
        prénom: str | None,
        date_naissance: date | None = None,
        taille: float | None = None,
        equipe: Optional[Equipe] = None
    ) -> None:
        if id is not None and not isinstance(id, str):
            raise TypeError("'id' doit être une instance de str")

        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")

        if prénom is not None and not isinstance(prénom, str):
            raise TypeError("'prénom' doit être une instance de str")

        if date_naissance is not None and not isinstance(date_naissance, date):
            raise TypeError("'date_naissance' doit être une instance de datetime.date")

        if taille is not None and not isinstance(taille, (int, float)):
            raise TypeError("'taille' doit être un nombre (float ou int)")

        if equipe is not None and not isinstance(equipe, Equipe):
            raise TypeError("'equipe' doit être une instance de Equipe")

        self.id = id
        self.nom = nom
        self.prénom = prénom
        self.date_naissance = date_naissance
        self.taille = float(taille) if taille is not None else None
        self.equipe = equipe

    def __repr__(self) -> str:
        return (
            f"Personne(id={self.id}, nom='{self.nom}', prénom='{self.prénom}', "
            f"date_naissance={self.date_naissance}, taille={self.taille}, "
            f"equipe={self.equipe})"
        )