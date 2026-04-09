class Equipe:
    def __init__(self, team_id: int, nom: str | None = None, location: str | None = None) -> None:
        if not isinstance(team_id, int):
            raise TypeError("'team_id' doit être un int")

        if nom is not None and not isinstance(nom, str):
            raise TypeError("'nom' doit être un str")

        if location is not None and not isinstance(location, str):
            raise TypeError("'location' doit être un str")

        self.team_id = team_id
        self.nom = nom
        self.location = location

    def __repr__(self) -> str:
        return f"Equipe(team_id={self.team_id}, nom={self.nom}, location={self.location})"