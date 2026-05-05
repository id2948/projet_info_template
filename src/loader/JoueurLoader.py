from datetime import date

import pandas as pd

from src.sport import Sport
from src.Model.Joueur import Joueur


def _age(dob_str: str) -> int | None:
    """Calcule l'âge à partir d'une chaîne de date ISO (AAAA-MM-JJ)."""
    try:
        dob = date.fromisoformat(dob_str[:10])
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except Exception:
        return None


def _pct_main(groupe: list, main: str) -> str:
    """Calcule le pourcentage de joueurs utilisant une main donnée."""
    total = 0
    nb = 0
    for j in groupe:
        if j.main:
            total += 1
            if j.main == main:
                nb += 1
    if total == 0:
        return "—"
    return f"{nb/total*100:.0f}%"


class JoueurLoader:
    """Dispatcher pour le chargement et les statistiques des joueurs.

    Les loaders spécifiques s'enregistrent via `register`.
    Chaque loader sport-spécifique implémente `load_all_joueurs` et `afficher_stats`.
    """

    _loaders = {}

    @staticmethod
    def register(sport_nom: str, loader) -> None:
        JoueurLoader._loaders[sport_nom] = loader

    def load_all_joueurs(self, sport: Sport) -> list[Joueur]:
        """Charge tous les joueurs du sport sélectionné.

        Parameters
        ----------
        sport : Sport
            Sport dont on veut charger les joueurs.

        Returns
        -------
        list[Joueur]
            Liste de joueurs.
        """
        loader = self._loaders.get(sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader de joueurs enregistré pour '{sport.nom}'")
        return loader().load_all_joueurs()

    def afficher_stats(self, joueurs: list, sport: Sport) -> None:
        """Affiche les statistiques des joueurs, spécifiques au sport si disponible.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur déjà chargés.
        sport : Sport
            Sport concerné.
        """
        loader = self._loaders.get(sport.nom)
        if loader is not None:
            loader().afficher_stats(joueurs)
        else:
            self._stats_generiques(joueurs, sport)

    @staticmethod
    def _stats_generiques(joueurs: list, sport: Sport) -> None:
        if not joueurs:
            print("Aucun joueur disponible.")
            return
        print(f"\n=== Statistiques des joueurs — {sport.nom} ({len(joueurs)}) ===\n")
        tailles = [j.taille for j in joueurs if j.taille is not None]
        if tailles:
            print(f"  Taille moyenne : {sum(tailles)/len(tailles):.1f} cm")
        poids = [j.poids for j in joueurs if j.poids is not None]
        if poids:
            print(f"  Poids moyen    : {sum(poids)/len(poids):.1f} kg")


# ── Basketball ────────────────────────────────────────────────────────────────

class BasketballJoueurLoader:

    DATA_PLAYERS = "data/basketball/player.csv"
    DATA_TEAMS   = "data/basketball/team.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df_players = pd.read_csv(self.DATA_PLAYERS)
        df_teams   = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        for _, row in df_teams.iterrows():
            teams[str(row["id"])] = row["full_name"]
        joueurs = []
        for _, row in df_players.iterrows():
            joueurs.append(Joueur(
                nom=str(row["last_name"]),
                prenom=str(row["first_name"]),
                sport="basketball",
                equipe=teams.get(str(row["team_id"]), str(row["team_id"])),
                position=str(row["position"]) if pd.notna(row["position"]) else None,
                date_naissance=str(row["birthdate"]) if pd.notna(row["birthdate"]) else None,
                taille=self._pieds_vers_cm(str(row["height"])),
                poids=float(row["weight"]) * 0.453592 if pd.notna(row["weight"]) else None,
            ))
        return joueurs

    def _pieds_vers_cm(self, valeur: str) -> float | None:
        try:
            pieds, pouces = valeur.split("-")
            return round((int(pieds) * 12 + int(pouces)) * 2.54, 1)
        except Exception:
            return None

    def afficher_stats(self, joueurs: list) -> None:
        print(f"\n=== Statistiques des joueurs — Basketball ({len(joueurs)}) ===\n")
        tailles = [j.taille for j in joueurs if j.taille is not None]
        poids_l = [j.poids  for j in joueurs if j.poids  is not None]
        if tailles:
            grand = None
            petit = None
            for j in joueurs:
                if j.taille is None:
                    continue
                if grand is None or j.taille > grand.taille:
                    grand = j
                if petit is None or j.taille < petit.taille:
                    petit = j
            print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
            print(f"  Plus grand      : {grand.prenom or ''} {grand.nom} — {grand.taille} cm")
            print(f"  Plus petit      : {petit.prenom or ''} {petit.nom} — {petit.taille} cm")
        if poids_l:
            lourd = None
            for j in joueurs:
                if j.poids is not None and (lourd is None or j.poids > lourd.poids):
                    lourd = j
            print(f"  Poids moyen     : {sum(poids_l)/len(poids_l):.1f} kg")
            print(f"  Plus lourd      : {lourd.prenom or ''} {lourd.nom} — {lourd.poids:.1f} kg")

        positions = {}
        for j in joueurs:
            if not j.position:
                continue
            if j.position not in positions:
                positions[j.position] = {"nb": 0, "tailles": [], "poids": []}
            positions[j.position]["nb"] += 1
            if j.taille:
                positions[j.position]["tailles"].append(j.taille)
            if j.poids:
                positions[j.position]["poids"].append(j.poids)

        if positions:
            print(f"\n  Répartition par position :\n")
            print(f"  {'Position':<22} {'Nb':>4}   {'T. moy (cm)':>11}   {'P. moy (kg)':>11}")
            print("  " + "─" * 54)
            for pos, d in sorted(positions.items(), key=lambda x: x[1]["nb"], reverse=True):
                t = f"{sum(d['tailles'])/len(d['tailles']):.1f}" if d["tailles"] else "—"
                p = f"{sum(d['poids'])/len(d['poids']):.1f}"    if d["poids"]   else "—"
                print(f"  {pos:<22} {d['nb']:>4}   {t:>11}   {p:>11}")


JoueurLoader.register("basketball", BasketballJoueurLoader)


# ── Football ──────────────────────────────────────────────────────────────────

class FootballJoueurLoader:

    DATA_PLAYERS = "data/football/player.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df = pd.read_csv(self.DATA_PLAYERS)
        joueurs = []
        for _, row in df.iterrows():
            joueurs.append(Joueur(
                nom=str(row["player_name"]),
                sport="football",
                date_naissance=str(row["birthday"]) if pd.notna(row["birthday"]) else None,
                taille=float(row["height (cm)"]) if pd.notna(row["height (cm)"]) else None,
                poids=float(row["weight (kg)"]) if pd.notna(row["weight (kg)"]) else None,
            ))
        return joueurs

    def afficher_stats(self, joueurs: list) -> None:
        print(f"\n=== Statistiques des joueurs — Football ({len(joueurs)}) ===\n")
        tailles = [j.taille for j in joueurs if j.taille is not None]
        poids_l = [j.poids  for j in joueurs if j.poids  is not None]
        if tailles:
            grand = None
            petit = None
            for j in joueurs:
                if j.taille is None:
                    continue
                if grand is None or j.taille > grand.taille:
                    grand = j
                if petit is None or j.taille < petit.taille:
                    petit = j
            print(f"  Taille moyenne  : {sum(tailles)/len(tailles):.1f} cm")
            print(f"  Plus grand      : {grand.nom} — {grand.taille} cm")
            print(f"  Plus petit      : {petit.nom} — {petit.taille} cm")
        if poids_l:
            lourd = None
            leger = None
            for j in joueurs:
                if j.poids is None:
                    continue
                if lourd is None or j.poids > lourd.poids:
                    lourd = j
                if leger is None or j.poids < leger.poids:
                    leger = j
            print(f"  Poids moyen     : {sum(poids_l)/len(poids_l):.1f} kg")
            print(f"  Plus lourd      : {lourd.nom} — {lourd.poids:.1f} kg")
            print(f"  Plus léger      : {leger.nom} — {leger.poids:.1f} kg")

        ages_data = []
        for j in joueurs:
            if j.date_naissance:
                a = _age(j.date_naissance)
                if a is not None:
                    ages_data.append((a, j))
        if ages_data:
            ages = [a for a, _ in ages_data]
            jeune = ages_data[0]
            vieux = ages_data[0]
            for item in ages_data[1:]:
                if item[0] < jeune[0]:
                    jeune = item
                if item[0] > vieux[0]:
                    vieux = item
            print(f"\n  Âge moyen  : {sum(ages)/len(ages):.1f} ans")
            print(f"  Plus jeune : {jeune[1].nom} — {jeune[0]} ans")
            print(f"  Plus vieux : {vieux[1].nom} — {vieux[0]} ans")


JoueurLoader.register("football", FootballJoueurLoader)


# ── League of Legends ─────────────────────────────────────────────────────────

class LoLJoueurLoader:

    DATA_PLAYERS = "data/LOL/player.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df = pd.read_csv(self.DATA_PLAYERS)
        joueurs = []
        for _, row in df.iterrows():
            joueurs.append(Joueur(
                nom=str(row["name"]),
                sport="LOL",
                pseudo=str(row["pseudo"]) if pd.notna(row["pseudo"]) else None,
                equipe=str(row["team"]) if pd.notna(row["team"]) else None,
                position=str(row["role"]) if pd.notna(row["role"]) else None,
                date_naissance=str(row["birthdate"]) if pd.notna(row["birthdate"]) else None,
                pays=str(row["country_of_birth"]) if pd.notna(row["country_of_birth"]) else None,
            ))
        return joueurs

    def afficher_stats(self, joueurs: list) -> None:
        print(f"\n=== Statistiques des joueurs — League of Legends ({len(joueurs)}) ===\n")
        roles = {}
        equipes = {}
        pays = {}
        for j in joueurs:
            if j.position: roles[j.position] = roles.get(j.position, 0) + 1
            if j.equipe: equipes[j.equipe] = equipes.get(j.equipe, 0) + 1
            if j.pays: pays[j.pays] = pays.get(j.pays, 0) + 1

        if roles:
            print("  Répartition par rôle :")
            for role, nb in sorted(roles.items(), key=lambda x: x[1], reverse=True):
                print(f"    {role:<12} : {nb}")
        if equipes:
            print(f"\n  Répartition par équipe :")
            for eq, nb in sorted(equipes.items(), key=lambda x: x[1], reverse=True):
                print(f"    {eq:<25} : {nb}")
        if pays:
            top = sorted(pays.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"\n  Top nationalités :")
            for p, nb in top:
                print(f"    {p:<25} : {nb}")
        ages_data = []
        for j in joueurs:
            if j.date_naissance:
                a = _age(j.date_naissance)
                if a is not None:
                    ages_data.append((a, j))
        if ages_data:
            ages = [a for a, _ in ages_data]
            jeune = ages_data[0]
            vieux = ages_data[0]
            for item in ages_data[1:]:
                if item[0] < jeune[0]:
                    jeune = item
                if item[0] > vieux[0]:
                    vieux = item
            print(f"\n  Âge moyen  : {sum(ages)/len(ages):.1f} ans")
            print(f"  Plus jeune : {jeune[1].pseudo or jeune[1].nom} — {jeune[0]} ans")
            print(f"  Plus vieux : {vieux[1].pseudo or vieux[1].nom} — {vieux[0]} ans")


JoueurLoader.register("LOL", LoLJoueurLoader)


# ── Tennis ────────────────────────────────────────────────────────────────────

_MAIN_LABELS = {"R": "Droitier(ère)", "L": "Gaucher(ère)", "U": "Ambidextre"}


class TennisJoueurLoader:

    DATA_ATP = "data/tennis/atp_players_2024.csv"
    DATA_WTA = "data/tennis/wta_players_2024.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df_atp = pd.read_csv(self.DATA_ATP)
        df_wta = pd.read_csv(self.DATA_WTA)
        df_atp["circuit"] = "ATP"
        df_wta["circuit"] = "WTA"
        df = pd.concat([df_atp, df_wta], ignore_index=True)
        joueurs = []
        for _, row in df.iterrows():
            dob = str(row["dob"]) if pd.notna(row["dob"]) else None
            if dob and dob != "nan":
                dob = dob.split(".")[0]
                if len(dob) == 8:
                    dob = f"{dob[:4]}-{dob[4:6]}-{dob[6:]}"
            joueurs.append(Joueur(
                nom=str(row["name_last"]),
                prenom=str(row["name_first"]),
                sport="tennis",
                equipe=str(row["circuit"]),
                pays=str(row["ioc"]) if pd.notna(row["ioc"]) else None,
                date_naissance=dob,
                taille=float(row["height"]) if pd.notna(row["height"]) else None,
                main=str(row["hand"]) if pd.notna(row["hand"]) else None,
            ))
        return joueurs

    def afficher_stats(self, joueurs: list) -> None:
        atp = [j for j in joueurs if j.equipe == "ATP"]
        wta = [j for j in joueurs if j.equipe == "WTA"]
        print(f"\n=== Statistiques tennis — {len(joueurs)} joueurs au total ===")
        print(f"  ATP (hommes) : {len(atp)}  |  WTA (femmes) : {len(wta)}\n")

        tailles_a = [j.taille for j in atp if j.taille]
        tailles_w = [j.taille for j in wta if j.taille]
        ages_a = []
        for j in atp:
            if j.date_naissance:
                a = _age(j.date_naissance)
                if a is not None:
                    ages_a.append(a)
        ages_w = []
        for j in wta:
            if j.date_naissance:
                a = _age(j.date_naissance)
                if a is not None:
                    ages_w.append(a)

        if tailles_a and tailles_w:
            print(f"  {'':22} {'ATP':>10}  {'WTA':>10}")
            print("  " + "─" * 46)
            print(f"  {'Taille moyenne':<22} {sum(tailles_a)/len(tailles_a):>9.1f}  {sum(tailles_w)/len(tailles_w):>9.1f} cm")
            if ages_a and ages_w:
                print(f"  {'Âge moyen':<22} {sum(ages_a)/len(ages_a):>9.1f}  {sum(ages_w)/len(ages_w):>9.1f} ans")
            print(f"  {'Droitiers/ères':<22} {_pct_main(atp, 'R'):>10}  {_pct_main(wta, 'R'):>10}")
            print(f"  {'Gauchers/ères':<22} {_pct_main(atp, 'L'):>10}  {_pct_main(wta, 'L'):>10}")

        for groupe, label in [(atp, "ATP — Hommes"), (wta, "WTA — Femmes")]:
            if not groupe:
                continue
            tailles = [j.taille for j in groupe if j.taille]
            mains = {}
            pays = {}
            for j in groupe:
                if j.main: mains[j.main] = mains.get(j.main, 0) + 1
                if j.pays: pays[j.pays] = pays.get(j.pays, 0) + 1
            print(f"\n  ── {label} ({len(groupe)} joueurs) ──")
            if tailles:
                grand = None
                for j in groupe:
                    if j.taille is not None and (grand is None or j.taille > grand.taille):
                        grand = j
                print(f"  Taille moy. : {sum(tailles)/len(tailles):.1f} cm  |  Plus grand(e) : {grand.prenom or ''} {grand.nom} ({grand.taille:.0f} cm)")
            if mains:
                total = sum(mains.values())
                parts = [f"{_MAIN_LABELS.get(m, m)} {n} ({n/total*100:.0f}%)" for m, n in sorted(mains.items(), key=lambda x: x[1], reverse=True)]
                print(f"  Main        : " + "  |  ".join(parts))
            if pays:
                top = sorted(pays.items(), key=lambda x: x[1], reverse=True)[:8]
                print(f"  Top 8 pays  : " + "  |  ".join(f"{p} ({n})" for p, n in top))


JoueurLoader.register("tennis", TennisJoueurLoader)


# ── Volleyball ────────────────────────────────────────────────────────────────

class VolleyJoueurLoader:

    DATA_MEN = "data/volley/player_men.csv"
    DATA_WOMEN = "data/volley/player_women.csv"
    DATA_COUNTRIES = "data/volley/country.csv"

    def load_all_joueurs(self) -> list[Joueur]:
        df_men = pd.read_csv(self.DATA_MEN)
        df_women = pd.read_csv(self.DATA_WOMEN)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)
        countries = {}
        for _, row in df_countries.iterrows():
            countries[row["code"]] = row["country"]
        df_men["genre"] = "Hommes"
        df_women["genre"] = "Femmes"
        df = pd.concat([df_men, df_women], ignore_index=True)
        joueurs = []
        for _, row in df.iterrows():
            code = str(row["country_code"]) if pd.notna(row["country_code"]) else None
            joueurs.append(Joueur(
                nom=str(row["name"]),
                sport="volley",
                equipe=str(row["genre"]),
                pays=countries.get(code, code) if code else None,
                date_naissance=str(row["birth_date"]) if pd.notna(row["birth_date"]) else None,
                taille=float(row["height"]) if pd.notna(row["height"]) else None,
                pseudo=str(row["nickname"]) if pd.notna(row["nickname"]) and str(row["nickname"]) != "" else None,
            ))
        return joueurs

    def afficher_stats(self, joueurs: list) -> None:
        hommes = [j for j in joueurs if j.equipe == "Hommes"]
        femmes = [j for j in joueurs if j.equipe == "Femmes"]
        print(f"\n=== Statistiques volleyball — {len(joueurs)} joueurs au total ===")
        print(f"  Hommes : {len(hommes)}  |  Femmes : {len(femmes)}\n")

        for groupe, label in [(hommes, "Hommes"), (femmes, "Femmes")]:
            if not groupe:
                continue
            tailles = [j.taille for j in groupe if j.taille]
            ages_data = []
            for j in groupe:
                if j.date_naissance:
                    a = _age(j.date_naissance)
                    if a is not None:
                        ages_data.append((a, j))
            pays = {}
            for j in groupe:
                if j.pays: pays[j.pays] = pays.get(j.pays, 0) + 1
            print(f"\n  ── {label} ({len(groupe)}) ──")
            if tailles:
                grand = None
                petit = None
                for j in groupe:
                    if j.taille is None:
                        continue
                    if grand is None or j.taille > grand.taille:
                        grand = j
                    if petit is None or j.taille < petit.taille:
                        petit = j
                print(f"  Taille : moy {sum(tailles)/len(tailles):.1f} cm  |  max {grand.taille:.0f} cm ({grand.nom})  |  min {petit.taille:.0f} cm ({petit.nom})")
            if ages_data:
                ages = [a for a, _ in ages_data]
                jeune = ages_data[0]
                vieux = ages_data[0]
                for item in ages_data[1:]:
                    if item[0] < jeune[0]:
                        jeune = item
                    if item[0] > vieux[0]:
                        vieux = item
                print(f"  Âge   : moy {sum(ages)/len(ages):.1f} ans  |  min {jeune[0]} ({jeune[1].nom})  |  max {vieux[0]} ({vieux[1].nom})")
            if pays:
                top = sorted(pays.items(), key=lambda x: x[1], reverse=True)[:5]
                print(f"  Pays  : " + "  |  ".join(f"{p} ({n})" for p, n in top))


JoueurLoader.register("volley", VolleyJoueurLoader)
