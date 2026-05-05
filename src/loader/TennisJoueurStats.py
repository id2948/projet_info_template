from datetime import date
from src.loader.JoueurStatsLoader import JoueurStatsLoader

_MAIN_LABELS = {"R": "Droitier(ère)", "L": "Gaucher(ère)", "U": "Ambidextre"}


def _age(dob_str: str) -> int | None:
    """Calcule l'âge à partir d'une chaîne de date ISO."""
    try:
        dob = date.fromisoformat(dob_str[:10])
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except Exception:
        return None


def _stats_circuit(groupe: list, label: str) -> None:
    """Affiche les statistiques détaillées pour un circuit (ATP ou WTA).

    Parameters
    ----------
    groupe : list
        Joueurs du circuit.
    label : str
        Nom du circuit ("ATP" ou "WTA").
    """
    tailles = [j.taille for j in groupe if j.taille]
    ages_data = [_age(j.date_naissance) for j in groupe if j.date_naissance]
    ages = [a for a in ages_data if a]

    mains: dict[str, int] = {}
    for j in groupe:
        if j.main:
            mains[j.main] = mains.get(j.main, 0) + 1

    pays: dict[str, int] = {}
    for j in groupe:
        if j.pays:
            pays[j.pays] = pays.get(j.pays, 0) + 1

    print(f"\n  ── {label} ({len(groupe)} joueurs) " + "─" * (35 - len(label)))

    if tailles:
        grand = max(groupe, key=lambda j: j.taille or 0)
        print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
        print(f"  Plus grand(e)   : {grand.prenom or ''} {grand.nom} — {grand.taille:.0f} cm")
    if ages:
        jeune = min(ages)
        vieux = max(ages)
        print(f"  Âge moyen       : {sum(ages)/len(ages):.1f} ans  (min {jeune} — max {vieux})")

    if mains:
        total = sum(mains.values())
        parts = [f"{_MAIN_LABELS.get(m, m)} {n} ({n/total*100:.0f}%)"
                 for m, n in sorted(mains.items(), key=lambda x: -x[1])]
        print(f"  Main dominante  : " + "  |  ".join(parts))

    if pays:
        top = sorted(pays.items(), key=lambda x: -x[1])[:8]
        print(f"  Top 8 pays      : " + "  |  ".join(f"{p} ({n})" for p, n in top))


class TennisJoueurStats:
    """Statistiques des joueurs de tennis, comparées par circuit (ATP / WTA)."""

    def run(self, joueurs: list) -> None:
        """Affiche les statistiques tennis par circuit avec comparaison ATP / WTA.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur tennis (ATP + WTA mélangés).
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        atp = [j for j in joueurs if j.equipe == "ATP"]
        wta = [j for j in joueurs if j.equipe == "WTA"]

        print(f"\n=== Statistiques tennis — {len(joueurs)} joueurs au total ===")
        print(f"  ATP (hommes) : {len(atp)}  |  WTA (femmes) : {len(wta)}\n")

        # ── Tableau comparatif synthétique ────────────────────
        tailles_a = [j.taille for j in atp if j.taille]
        tailles_w = [j.taille for j in wta if j.taille]
        ages_a = [a for a in (_age(j.date_naissance) for j in atp if j.date_naissance) if a]
        ages_w = [a for a in (_age(j.date_naissance) for j in wta if j.date_naissance) if a]

        # Main dominante
        def _pct(groupe, main):
            total = sum(1 for j in groupe if j.main)
            nb = sum(1 for j in groupe if j.main == main)
            return f"{nb/total*100:.0f}%" if total else "—"

        if tailles_a and tailles_w:
            print(f"  {'':22} {'ATP':>10}  {'WTA':>10}")
            print("  " + "─" * 46)
            print(f"  {'Taille moyenne':<22} {sum(tailles_a)/len(tailles_a):>9.1f}  {sum(tailles_w)/len(tailles_w):>9.1f} cm")
            if ages_a and ages_w:
                print(f"  {'Âge moyen':<22} {sum(ages_a)/len(ages_a):>9.1f}  {sum(ages_w)/len(ages_w):>9.1f} ans")
            print(f"  {'Droitiers/ères':<22} {_pct(atp, 'R'):>10}  {_pct(wta, 'R'):>10}")
            print(f"  {'Gauchers/ères':<22} {_pct(atp, 'L'):>10}  {_pct(wta, 'L'):>10}")

        # ── Détail par circuit ────────────────────────────────
        if atp:
            _stats_circuit(atp, "ATP — Hommes")
        if wta:
            _stats_circuit(wta, "WTA — Femmes")


JoueurStatsLoader.register("tennis", TennisJoueurStats)
