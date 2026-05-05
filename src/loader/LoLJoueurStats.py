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


class LoLJoueurStats:
    """Statistiques détaillées des joueurs LoL : rôle, équipe, nationalité, âge."""

    def run(self, joueurs: list) -> None:
        """Affiche les statistiques LoL par rôle, équipe et pays.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur LoL déjà chargés.
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        print(f"\n=== Statistiques des joueurs — League of Legends ({len(joueurs)} joueurs) ===\n")

        # ── Par rôle ──────────────────────────────────────────
        roles: dict[str, int] = {}
        for j in joueurs:
            if j.position:
                roles[j.position] = roles.get(j.position, 0) + 1
        if roles:
            print("  Répartition par rôle :")
            for role, nb in sorted(roles.items(), key=lambda x: -x[1]):
                print(f"    {role:<12} : {nb} joueurs")

        # ── Par équipe ────────────────────────────────────────
        equipes: dict[str, int] = {}
        for j in joueurs:
            if j.equipe:
                equipes[j.equipe] = equipes.get(j.equipe, 0) + 1
        if equipes:
            print(f"\n  Répartition par équipe :")
            for eq, nb in sorted(equipes.items(), key=lambda x: -x[1]):
                print(f"    {eq:<25} : {nb} joueurs")

        # ── Par nationalité ───────────────────────────────────
        pays: dict[str, int] = {}
        for j in joueurs:
            if j.pays:
                pays[j.pays] = pays.get(j.pays, 0) + 1
        if pays:
            top = sorted(pays.items(), key=lambda x: -x[1])[:10]
            print(f"\n  Top nationalités :")
            for p, nb in top:
                print(f"    {p:<25} : {nb} joueurs")

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
            print(f"  Plus jeune      : {plus_jeune[1].pseudo or plus_jeune[1].nom} — {plus_jeune[0]} ans")
            print(f"  Plus vieux      : {plus_vieux[1].pseudo or plus_vieux[1].nom} — {plus_vieux[0]} ans")


JoueurStatsLoader.register("LOL", LoLJoueurStats)
