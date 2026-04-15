from competition import Competition
from Parsers.parse_csv import parse_csv 


class CompetitionLoader:
    """Charge les compétitions depuis season_type."""

    def __init__(self, filepath: str) -> None:
        if not isinstance(filepath, str):
            raise TypeError("'filepath' doit être un str")

        self.filepath = filepath

    def charger_competitions(self) -> dict[str, Competition]:
        data = parse_csv(self.filepath, sep=",")

        competitions: dict[str, Competition] = {}

        for ligne in data:
            season_type = ligne["season_type"].strip()

            if season_type not in competitions:
                competitions[season_type] = Competition(season_type)

        return competitions