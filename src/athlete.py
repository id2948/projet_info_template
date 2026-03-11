from individu import Individu


class Athlete(Individu):
    """Modélise les athlètes parmi les individu de la compétition.

    Parameters
    ----------
    id: str
        identifiant dans la compétition de l'athlète

    nom: str
        nom de l'athlète

    prenom: str
        prénom de l'athlète

    date_de_naissance: date
        date de naissance de l'athlète

    poids: float
        poids de l'athlète

    taille: float
        taille de l'athlète
    """

    def __init__(
        self,
        id: str,
        nom: str,
        prenom: str,
        date_de_naissance: date,
        poids: float,
        taille: float,
    ) -> None:
        Individu.__init__(self, id, nom, prenom)
        if not isinstance(date_de_naissance, date):
            raise TypeError("'date_de_naissance' doit être une instance de date")
        if not isinstance(poids, float):
            raise TypeError("'poids' doit être une instance de float")
        if not isinstance(taille, float):
            raise TypeError("'taille' doit être une instance de float")

        self.date_de_naissance = date_de_naissance
        self.poids = poids
        self.taille = taille
