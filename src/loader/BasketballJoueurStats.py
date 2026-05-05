from src.loader.JoueurStatsLoader import JoueurStatsLoader


class BasketballJoueurStats:
    """Statistiques détaillées des joueurs NBA : générales et par position."""

    def run(self, joueurs: list) -> None:
        """Affiche les statistiques NBA, dont la répartition par position.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur basketball déjà chargés.
        """
        if not joueurs:
            print("Aucun joueur disponible.")
            return

        print(f"\n=== Statistiques des joueurs — Basketball ({len(joueurs)} joueurs) ===\n")

        # ── Générale ──────────────────────────────────────────
        tailles = [j.taille for j in joueurs if j.taille is not None]
        poids_l = [j.poids  for j in joueurs if j.poids  is not None]

        if tailles:
            grand = max(joueurs, key=lambda j: j.taille or 0)
            petit = min(joueurs, key=lambda j: j.taille or float("inf"))
            print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
            print(f"  Plus grand      : {grand.prenom or ''} {grand.nom} — {grand.taille} cm")
            print(f"  Plus petit      : {petit.prenom or ''} {petit.nom} — {petit.taille} cm")
        if poids_l:
            lourd = max(joueurs, key=lambda j: j.poids or 0)
            print(f"  Poids moyen     : {sum(poids_l)/len(poids_l):.1f} kg")
            print(f"  Plus lourd      : {lourd.prenom or ''} {lourd.nom} — {lourd.poids:.1f} kg")

        # ── Par position ──────────────────────────────────────
        positions: dict[str, dict] = {}
        for j in joueurs:
            if not j.position:
                continue
            pos = j.position
            if pos not in positions:
                positions[pos] = {"nb": 0, "tailles": [], "poids": []}
            positions[pos]["nb"] += 1
            if j.taille:
                positions[pos]["tailles"].append(j.taille)
            if j.poids:
                positions[pos]["poids"].append(j.poids)

        if positions:
            print(f"\n  Répartition par position :\n")
            print(f"  {'Position':<22} {'Nb':>4}   {'T. moy (cm)':>11}   {'P. moy (kg)':>11}")
            print("  " + "─" * 54)
            for pos, d in sorted(positions.items(), key=lambda x: -x[1]["nb"]):
                t = f"{sum(d['tailles'])/len(d['tailles']):.1f}" if d["tailles"] else "—"
                p = f"{sum(d['poids'])/len(d['poids']):.1f}"    if d["poids"]   else "—"
                print(f"  {pos:<22} {d['nb']:>4}   {t:>11}   {p:>11}")

        # ── Par équipe (top 5) ────────────────────────────────
        equipes: dict[str, int] = {}
        for j in joueurs:
            if j.equipe:
                equipes[j.equipe] = equipes.get(j.equipe, 0) + 1
        if equipes:
            top = sorted(equipes.items(), key=lambda x: -x[1])[:5]
            print(f"\n  Top 5 équipes (effectif) :")
            for eq, nb in top:
                print(f"    {eq:<30} : {nb} joueurs")


JoueurStatsLoader.register("basketball", BasketballJoueurStats)
