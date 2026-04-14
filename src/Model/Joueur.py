from dataclasses import dataclass
from typing import Optional


@dataclass
class Joueur:
    # Communs
    nom:            str
    sport:          str

    # Optionnels selon le sport
    prenom:         Optional[str] = None
    pseudo:         Optional[str] = None   # LoL
    equipe:         Optional[str] = None   # basketball, LoL
    position:       Optional[str] = None   # basketball, LoL
    date_naissance: Optional[str] = None
    taille:         Optional[float] = None   # en cm
    poids:          Optional[float] = None   # en kg (basketball)
    pays:           Optional[str] = None   # LoL, tennis, volley
    main:           Optional[str] = None   # tennis (R/L)

    def __str__(self):
        parts = []
        if self.prenom:
            parts.append(f"{self.prenom} {self.nom}")
        elif self.pseudo:
            parts.append(f"{self.pseudo} ({self.nom})")
        else:
            parts.append(self.nom)

        if self.equipe:
            parts.append(f"| {self.equipe}")
        if self.pays:
            parts.append(f"| {self.pays}")
        if self.position:
            parts.append(f"| {self.position}")
        if self.taille:
            parts.append(f"| {self.taille} cm")
        if self.date_naissance:
            parts.append(f"| né(e) le {self.date_naissance}")

        return f"[{self.sport}] " + " ".join(parts)