class Sport :

    def __init__(self, nom: str) -> None:

        if not isinstance(nom, str):
            raise TypeError("'prenom' doit être une instance de str")
        self.nom = nom

    def __str__(self):
        return self.nom