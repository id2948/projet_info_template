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


def _stats_groupe(groupe: list, label: str) -> None:
    """Affiche les statistiques d'un groupe de joueurs (taille, âge, pays).

    Parameters
    ----------
    groupe : list
        Sous-liste de Joueur.
    label : str
        Nom du groupe à afficher (ex : "Hommes").
    """
    tailles = [j.taille for j in groupe if j.taille is not None]
    ages_data = [(_age(j.date_naissance), j) for j in groupe if j.date_naissance]
    ages = [(a, j) for a, j in ages_data if a is not None]

    print(f"\n  ── {label} ({len(groupe)} joueurs) " + "─" * (30 - len(label)))

    if tailles:
        grand = max(groupe, key=lambda j: j.taille or 0)
        petit = min(groupe, key=lambda j: j.taille or float("inf"))
        print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
        print(f"  Plus grand(e)   : {grand.nom} — {grand.taille:.0f} cm")
        print(f"  Plus petit(e)   : {petit.nom} — {petit.taille:.0f} cm")

    if ages:
        vals = [a for a, _ in ages]
        jeune = min(ages, key=lambda x: x[0])
        vieux = max(ages, key=lambda x: x[0])
        print(f"  Âge moyen       : {sum(vals)/len(vals):.1f} ans")
        print(f"  Plus jeune      : {jeune[1].nom} — {jeune[0]} ans")
        print(f"  Plus vieux      : {vieux[1].nom} — {vieux[0]} ans")

    pays: dict[str, int] = {}
    for j in groupe:
        if j.pays:
            pays[j.pays] = pays.get(j.pays, 0) + 1
    if pays:
        top = sorted(pays.items(), key=lambda x: -x[1])[:5]
        print(f"  Top 5 pays      : " + "  |  ".join(f"{p} ({n})" for p, n in top))


class VolleyJoueurStats:
    """Statistiques des joueurs de volleyball, comparées par genre (Hommes / Femmes)."""

    def run(self, joueurs: list) -> None:
        """Affiche les statistiques volleyball comparées par genre.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur volleyball (Hommes + Femmes mélangés).
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        hommes = [j for j in joueurs if j.equipe == "Hommes"]
        femmes = [j for j in joueurs if j.equipe == "Femmes"]

        print(f"\n=== Statistiques volleyball — {len(joueurs)} joueurs au total ===")
        print(f"  Hommes : {len(hommes)}  |  Femmes : {len(femmes)}\n")

        # ── Comparaison synthétique ───────────────────────────
        tailles_h = [j.taille for j in hommes if j.taille]
        tailles_f = [j.taille for j in femmes if j.taille]
        if tailles_h and tailles_f:
            print(f"  {'':20} {'Hommes':>10}  {'Femmes':>10}")
            print("  " + "─" * 44)
            print(f"  {'Taille moyenne':<20} {sum(tailles_h)/len(tailles_h):>9.1f}  {sum(tailles_f)/len(tailles_f):>9.1f} cm")

            ages_h = [_age(j.date_naissance) for j in hommes if j.date_naissance]
            ages_h = [a for a in ages_h if a]
            ages_f = [_age(j.date_naissance) for j in femmes if j.date_naissance]
            ages_f = [a for a in ages_f if a]
            if ages_h and ages_f:
                print(f"  {'Âge moyen':<20} {sum(ages_h)/len(ages_h):>9.1f}  {sum(ages_f)/len(ages_f):>9.1f} ans")

        # ── Détail par genre ──────────────────────────────────
        if hommes:
            _stats_groupe(hommes, "Hommes")
        if femmes:
            _stats_groupe(femmes, "Femmes")


JoueurStatsLoader.register("volley", VolleyJoueurStats)
