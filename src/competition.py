class Competition:
    """Représente une compétition sportive.

    Parameters
    ----------
    nom : str
        nom de la compétition
    """

    def __init__(self, nom: str) -> None:
        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")

        self.nom = nom

    def __repr__(self) -> str:
        return f"Competition(nom='{self.nom}')"