from src.sport import Sport 



class Competition:
    def __init__(self, nom: str, sport : Sport) -> None:
        if not isinstance(nom, str):
            raise TypeError("'nom' doit être une instance de str")


        self.nom = nom

    def __repr__(self) -> str:
        return f"Competition(nom='{self.nom}')"