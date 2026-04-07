from datetime import datetime, date

from src.Parsers.parse_csv import parse_csv
from personne import Personne
from equipe import Equipe


class BasketballPlayerLoader:
    def __init__(self, filepath: str, equipes: dict[str, Equipe]) -> None:
        self.filepath = filepath
        self.equipes = equipes

    def load_all_players(self) -> list[Personne]:
        data = parse_csv(self.filepath, sep=",")

        joueurs = []
        for row in data:
            joueur = self._create_personne(row)
            joueurs.append(joueur)

        return joueurs

    def _create_personne(self, row: dict) -> Personne:
        team_id = row["team_id"]
        equipe = self.equipes.get(team_id)

        return Personne(
            id=row["person_id"] if row["person_id"] else None,
            nom=row["last_name"],
            prénom=row["first_name"],
            date_naissance=self._parse_date(row["birthdate"]),
            taille=self._parse_height_to_cm(row["height"]),
            equipe=equipe
        )

    def _parse_date(self, value: str) -> date | None:
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            parts = value.split("-")
            if len(parts) == 3:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                return date(year, month, day)

        return None

    def _parse_height_to_cm(self, value: str) -> float | None:
        if not value:
            return None

        try:
            feet, inches = value.split("-")
            feet = int(feet)
            inches = int(inches)

            total_inches = feet * 12 + inches
            total_cm = total_inches * 2.54

            return round(total_cm, 1)
        except (ValueError, AttributeError):
            return None