from datetime import date


class Participant:
    """Permet de modéliser un participant dans la compétition.

    Parameters
    ----------
    id: str
        identifiant dans la compétition du participant

    nom: str
        nom et prénom du particpant dans le cas où une variable seulement donne les deux

    prénom: str | None
        prénom dans le cas où deux variables distinctes font nom et prénom

    """
    def __init__(
        self,
        id: str | None,
        nom: str,
        prénom: str | None,
        date_naissance: date | None,
        nationalite: str | None
    ) -> None:
        if id is not None and not isinstance(id, str):
            raise TypeError("'id' doit être une instance de int")
        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")
        if not isinstance(prénom, str):
            raise TypeError("'prénom' doit être une instance de str")
        if not isinstance(date_naissance, str):
            raise TypeError("'date_naissance' doit être une instance de date")
        if not isinstance(nationalite, str):
            raise TypeError("'nationalite' doit être une instance de nationalite")
        
        self.id = id
        self.nom = nom
        self.prénom = prénom
        self.date_naissance = date_naissance
        self.nationalite = nationalite
