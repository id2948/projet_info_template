class Competition:
    """Représente une compétition sportive.

    Parameters
    ----------
    nom : str
        nom de la compétition
    """

    def __init__(self, nom: str) -> None:
        # --- Vérification ---
        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")

        # --- Attribut ---
        self.nom = nom

    def __repr__(self) -> str:
        return f"Competition(nom='{self.nom}')"