from datetime import date
from src.loader.JoueurStatsLoader import JoueurStatsLoader


def _age(dob_str: str) -> int | None:
    """Calcule l'âge à partir d'une chaîne de date ISO."""
    try:
        dob = date.fromisoformat(dob_str[:10])
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except Exception:
        return None


class FootballJoueurStats:
    """Statistiques détaillées des joueurs de football : morphologie et âge."""

    def run(self, joueurs: list) -> None:
        """Affiche les statistiques football (taille, poids, âge).

        Parameters
        ----------
        joueurs : list
            Liste de Joueur football déjà chargés.
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        print(f"\n=== Statistiques des joueurs — Football ({len(joueurs)} joueurs) ===\n")

        # ── Morphologie ───────────────────────────────────────
        tailles = [j.taille for j in joueurs if j.taille is not None]
        poids_l = [j.poids  for j in joueurs if j.poids  is not None]

        if tailles:
            grand = max(joueurs, key=lambda j: j.taille or 0)
            petit = min(joueurs, key=lambda j: j.taille or float("inf"))
            print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
            print(f"  Plus grand      : {grand.nom} — {grand.taille} cm")
            print(f"  Plus petit      : {petit.nom} — {petit.taille} cm")
        if poids_l:
            lourd = max(joueurs, key=lambda j: j.poids or 0)
            leger = min(joueurs, key=lambda j: j.poids or float("inf"))
            print(f"  Poids moyen     : {sum(poids_l)/len(poids_l):.1f} kg")
            print(f"  Plus lourd      : {lourd.nom} — {lourd.poids:.1f} kg")
            print(f"  Plus léger      : {leger.nom} — {leger.poids:.1f} kg")

        # ── Âge ──────────────────────────────────────────────
        ages_avec_joueur = [
            (_age(j.date_naissance), j) for j in joueurs if j.date_naissance
        ]
        ages_valides = [(a, j) for a, j in ages_avec_joueur if a is not None]

        if ages_valides:
            ages = [a for a, _ in ages_valides]
            plus_jeune = min(ages_valides, key=lambda x: x[0])
            plus_vieux = max(ages_valides, key=lambda x: x[0])
            print(f"\n  Âge moyen       : {sum(ages)/len(ages):.1f} ans")
            print(f"  Plus jeune      : {plus_jeune[1].nom} — {plus_jeune[0]} ans")
            print(f"  Plus vieux      : {plus_vieux[1].nom} — {plus_vieux[0]} ans")

            # Distribution par tranche d'âge
            tranches = {"< 20 ans": 0, "20-25 ans": 0, "26-30 ans": 0, "31-35 ans": 0, "> 35 ans": 0}
            for a, _ in ages_valides:
                if a < 20:
                    tranches["< 20 ans"] += 1
                elif a <= 25:
                    tranches["20-25 ans"] += 1
                elif a <= 30:
                    tranches["26-30 ans"] += 1
                elif a <= 35:
                    tranches["31-35 ans"] += 1
                else:
                    tranches["> 35 ans"] += 1
            print(f"\n  Distribution par tranche d'âge :")
            for tranche, nb in tranches.items():
                print(f"    {tranche:<12} : {nb} joueurs")


JoueurStatsLoader.register("football", FootballJoueurStats)
