from src.sport import Sport


class Equipe:
    """Représente une équipe avec ses statistiques, tous sports confondus.

    Parameters
    ----------
    nom : str
        Nom de l'équipe.
    sport : str
        Sport pratiqué.
    abreviation : str, optional
        Abréviation de l'équipe.
    """

    def __init__(self, nom: str, sport: str, abreviation: str | None = None):
        self.nom = nom
        self.sport = sport
        self.abreviation = abreviation

        # Stats communes
        self.matchs_joues = 0
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.points = 0
        self.score_pour = 0.0
        self.score_contre = 0.0

        # Stats basketball
        self.rebonds = 0.0
        self.passes = 0.0
        self.interceptions = 0.0
        self.contres = 0.0

        # Stats LoL
        self.kills = 0
        self.dragons = 0
        self.barons = 0
        self.gold = 0.0

    @property
    def difference_score(self) -> float:
        """Différence entre le score marqué et le score encaissé."""
        return self.score_pour - self.score_contre

    @property
    def winrate(self) -> float:
        """Pourcentage de victoires sur les matchs joués."""
        return self.victoires / self.matchs_joues * 100 if self.matchs_joues else 0.0

    def ajouter_match(
        self,
        score_pour: float,
        score_contre: float,
        nul_possible: bool = True
    ) -> None:
        """Enregistre le résultat d'un match et met à jour les statistiques.

        Parameters
        ----------
        score_pour : float
            Score réalisé par cette équipe.
        score_contre : float
            Score encaissé par cette équipe.
        nul_possible : bool, optional
            Indique si le sport autorise les matchs nuls (par défaut True).
        """
        self.matchs_joues += 1
        self.score_pour += score_pour
        self.score_contre += score_contre

        if score_pour > score_contre:
            self.victoires += 1
            self.points += 3 if nul_possible else 1
        elif nul_possible and score_pour == score_contre:
            self.nuls += 1
            self.points += 1
        else:
            self.defaites += 1

    @staticmethod
    def run_menu(sport: Sport) -> None:
        """Affiche le menu de statistiques d'équipe pour un sport donné.

        Délègue au loader enregistré pour ce sport via EquipeLoader.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        from src.loader.EquipeLoader import EquipeLoader
        EquipeLoader().run(sport)
