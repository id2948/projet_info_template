from dataclasses import dataclass
from typing import Optional

@dataclass
class Match:
    # Communs
    date:     str
    equipe_1: str
    equipe_2: str
    score_1:  float
    score_2:  float
    sport:    str

    # Basketball
    season:       Optional[str]   = None
    season_type:  Optional[str]   = None

    # Football
    league_id:    Optional[float] = None
    stage:        Optional[str]   = None  # aussi volley

    # LoL
    patch:        Optional[str]   = None
    week:         Optional[int]   = None
    winner:       Optional[str]   = None

    # Tennis
    tourney_name: Optional[str]   = None
    surface:      Optional[str]   = None
    round:        Optional[str]   = None

    def __str__(self):
        return (f"[{self.sport}] {self.date} | "
                f"{self.equipe_1} {self.score_1} - {self.score_2} {self.equipe_2}")