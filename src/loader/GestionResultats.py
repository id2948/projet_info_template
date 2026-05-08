import csv
import os

from src.Model.Match import Match
from src.Model.Equipe import Equipe

FICHIER_RESULTATS = "data/resultats/nouveaux_matchs.csv"
COLONNES = ["sport", "date", "equipe_1", "equipe_2", "score_1", "score_2"]


class GestionResultats:
    """Gestion des nouveaux résultats ajoutés manuellement.

    Les résultats sont stockés dans un fichier CSV unique,
    et automatiquement inclus lors du chargement des données.
    """

    @staticmethod
    def sauvegarder(
        sport: str,
        date: str,
        equipe_1: str,
        equipe_2: str,
        score_1: float,
        score_2: float,
    ) -> None:
        """Sauvegarde un résultat de match dans le fichier de résultats.

        Parameters
        ----------
        sport : str
            Nom du sport (ex : "football", "LOL").
        date : str
            Date du match au format AAAA-MM-JJ.
        equipe_1 : str
            Nom de la première équipe.
        equipe_2 : str
            Nom de la deuxième équipe.
        score_1 : float
            Score de la première équipe.
        score_2 : float
            Score de la deuxième équipe.
        """
        os.makedirs(os.path.dirname(FICHIER_RESULTATS), exist_ok=True)
        deja_existe = (
            os.path.exists(FICHIER_RESULTATS) and os.path.getsize(FICHIER_RESULTATS) > 0
        )
        with open(FICHIER_RESULTATS, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLONNES)
            if not deja_existe:
                writer.writeheader()
            writer.writerow(
                {
                    "sport": sport,
                    "date": date,
                    "equipe_1": equipe_1,
                    "equipe_2": equipe_2,
                    "score_1": score_1,
                    "score_2": score_2,
                }
            )

    @staticmethod
    def charger(sport: str) -> list:
        """Charge les résultats sauvegardés pour un sport donné.

        Parameters
        ----------
        sport : str
            Nom du sport pour lequel charger les résultats.

        Returns
        -------
        list
            Liste des nouveaux matchs enregistrés pour ce sport.
        """
        if not os.path.exists(FICHIER_RESULTATS):
            return []
        resultats = []
        with open(FICHIER_RESULTATS, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("sport") == sport:
                    resultats.append(
                        Match(
                            date=row["date"],
                            equipe_1=row["equipe_1"],
                            equipe_2=row["equipe_2"],
                            score_1=float(row["score_1"]),
                            score_2=float(row["score_2"]),
                            sport=row["sport"],
                        )
                    )
        return resultats

    @staticmethod
    def _correspond(nom_a: str, nom_b: str) -> bool:
        """Vérifie si deux noms d'équipe se correspondent.

        Parameters
        ----------
        nom_a : str
            Premier nom à comparer.
        nom_b : str
            Second nom à comparer.

        Returns
        -------
        bool
            Vrai si l'un contient l'autre (insensible à la casse).
        """
        a, b = nom_a.lower(), nom_b.lower()
        return a in b or b in a

    @staticmethod
    def appliquer_a_equipe(
        equipe: Equipe, nom_filtre: str, nul_possible: bool = True
    ) -> int:
        """Applique les nouveaux résultats à un objet Equipe.

        Parameters
        ----------
        equipe : Equipe
            Objet Equipe à mettre à jour.
        nom_filtre : str
            Nom de l'équipe tel qu'il apparaît dans les données.
        nul_possible : bool, optional
            Indique si le sport autorise les matchs nuls (par défaut True).

        Returns
        -------
        int
            Nombre de nouveaux résultats appliqués.
        """
        nb = 0
        for m in GestionResultats.charger(equipe.sport):
            if GestionResultats._correspond(nom_filtre, m.equipe_1):
                equipe.ajouter_match(m.score_1, m.score_2, nul_possible)
                nb += 1
            elif GestionResultats._correspond(nom_filtre, m.equipe_2):
                equipe.ajouter_match(m.score_2, m.score_1, nul_possible)
                nb += 1
        return nb

    @staticmethod
    def appliquer_a_competition(comp, nul_possible: bool = True) -> int:
        """Applique les nouveaux résultats à toutes les équipes d'une Competition.

        Parameters
        ----------
        comp : Competition
            Compétition à mettre à jour.
        nul_possible : bool, optional
            Indique si le sport autorise les matchs nuls (par défaut True).

        Returns
        -------
        int
            Nombre de nouveaux matchs appliqués.
        """
        nb = 0
        for m in GestionResultats.charger(comp.sport):
            e1 = e2 = None
            for eq in comp.equipes.values():
                if GestionResultats._correspond(m.equipe_1, eq.nom):
                    e1 = eq
                if GestionResultats._correspond(m.equipe_2, eq.nom):
                    e2 = eq
            if e1 is None:
                e1 = Equipe(m.equipe_1, comp.sport)
                comp.ajouter_equipe(m.equipe_1, e1)
            if e2 is None:
                e2 = Equipe(m.equipe_2, comp.sport)
                comp.ajouter_equipe(m.equipe_2, e2)
            e1.ajouter_match(m.score_1, m.score_2, nul_possible)
            e2.ajouter_match(m.score_2, m.score_1, nul_possible)
            nb += 1
        return nb

    @staticmethod
    def lister(sport: str | None = None) -> list:
        """Retourne tous les résultats enregistrés, filtrés par sport si précisé.

        Parameters
        ----------
        sport : str | None, optional
            Sport à filtrer. Si None, retourne tous les sports.

        Returns
        -------
        list
            Liste des matchs enregistrés.
        """
        if not os.path.exists(FICHIER_RESULTATS):
            return []
        resultats = []
        with open(FICHIER_RESULTATS, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if sport is None or row.get("sport") == sport:
                    resultats.append(
                        Match(
                            date=row["date"],
                            equipe_1=row["equipe_1"],
                            equipe_2=row["equipe_2"],
                            score_1=float(row["score_1"]),
                            score_2=float(row["score_2"]),
                            sport=row["sport"],
                        )
                    )
        return resultats
