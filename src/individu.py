class Individu:
    """Permet de modéliser un individu dans la compétition.

    Parameters
    ----------
    id: str
        identifiant dans la compétition de l'individu

    nom: str
        nom de l'individu

    prenom: str
        prénom de l'individu
    """

    def __init__(self, id: str, nom: str, prenom: str) -> None:
        if not isinstance(id, str):
            raise TypeError("'id' doit être une instance de str")
        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")
        if not isinstance(prenom, str):
            raise TypeError("'prenom' doit être une instance de str")
 
        
        self.id = id
        self.nom = nom
        self.prenom = prenom
