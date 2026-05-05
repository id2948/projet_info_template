class Sport:
    """Représente un sport identifié par son nom.

    Parameters
    ----------
    nom : str
        Nom du sport (ex : "football", "LOL", "basketball").
    """

    def __init__(self, nom: str) -> None:

        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")
        self.nom = nom

    def __str__(self):
        return self.nom