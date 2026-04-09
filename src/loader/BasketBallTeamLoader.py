from src.Parsers.parse_csv import parse_csv
from team import Equipe


class BasketballTeamLoader:
    """Permet de charger les équipes de basketball depuis un fichier CSV."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load_all_teams(self) -> dict[str, Equipe]:
        data = parse_csv(self.filepath, sep=",")

        equipes = {}
        for row in data:
            equipe = self._create_equipe(row)
            equipes[equipe.id] = equipe  # 👈 clé = team_id

        return equipes

    def _create_equipe(self, row: dict) -> Equipe:
        return Equipe(
            id=row["id"],
            nom=row["full_name"],
            location=row["city"]
        )