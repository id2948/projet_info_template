import pandas as pd

from src.sport import Sport
from src.Model.Competition import Competition
from src.Model.Equipe import Equipe


class CompetitionLoader:
    """Dispatcher pour les classements de compétition selon le sport.

    Les loaders spécifiques s'enregistrent via `register`.
    Chaque loader implémente `run()` qui affiche les classements.
    """

    _loaders = {}

    @staticmethod
    def register(sport_nom: str, loader) -> None:
        CompetitionLoader._loaders[sport_nom] = loader

    def run(self, sport: Sport) -> None:
        """Lance le menu de classement pour le sport sélectionné.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        loader = self._loaders.get(sport.nom)
        if loader is None:
            print(f"Pas de classement disponible pour {sport.nom}.")
            return
        loader().run()


# ── Football ──────────────────────────────────────────────────────────────────

class FootballCompetitionLoader:

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS = "data/football/team.csv"
    DATA_LEAGUES = "data/football/league.csv"
    DATA_COUNTRY = "data/football/country.csv"

    def run(self) -> None:
        df_match = pd.read_csv(self.DATA_MATCHES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        df_league = pd.read_csv(self.DATA_LEAGUES)
        df_country = pd.read_csv(self.DATA_COUNTRY)
        teams = {}
        abbrevs = {}
        for _, row in df_team.iterrows():
            teams[row["team_api_id"]] = row["team_long_name"]
            abbrevs[row["team_api_id"]] = row["team_short_name"]

        leagues = {}
        lg_ctry = {}
        for _, row in df_league.iterrows():
            leagues[row["id"]] = row["name"]
            lg_ctry[row["id"]] = row["country_id"]

        countries = {}
        for _, row in df_country.iterrows():
            countries[row["id"]] = row["name"]

        print("\n  Que voulez-vous faire ?")
        print("  1 - Classement d'une ligue pour une saison")
        print("  2 - Meilleures attaques d'une ligue")
        print("  3 - Meilleures défenses d'une ligue")
        print("  4 - Classement général d'un championnat (toutes saisons)")
        choix = input("\n  Votre choix : ").strip()

        lid = self._choisir_ligue(leagues, countries, lg_ctry)
        saison = self._choisir_saison(df_match) if choix in ["1", "2", "3"] else None

        df = df_match.copy()
        if lid: df = df[df["league_id"] == lid]
        if saison: df = df[df["season"] == saison]
        if df.empty: print("  Aucun match trouvé."); return

        nom_ligue = leagues.get(lid, "Toutes ligues") if lid else "Toutes ligues"
        comp = self._construire(df, teams, abbrevs, nom_ligue)
        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_competition(comp, nul_possible=True)
        if nb: print(f"  (+ {nb} nouveau(x) résultat(s) inclus)")

        if choix == "1":
            cl = comp.classement_par("points")
            self._afficher_foot(cl, f"{nom_ligue} — {saison}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Meilleures attaques — {nom_ligue} {saison or ''} ===\n")
            print(f"  {'#':<4}{'Équipe':<30}{'Buts':>6}{'Moy/match':>10}")
            print("  " + "─" * 52)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i:<4}{e.nom:<30}{e.score_pour:>6.0f}{moy:>10.2f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: e.score_contre)
            print(f"\n=== Meilleures défenses — {nom_ligue} {saison or ''} ===\n")
            print(f"  {'#':<4}{'Équipe':<30}{'Buts enc.':>10}{'Moy/match':>10}")
            print("  " + "─" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_contre / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i:<4}{e.nom:<30}{e.score_contre:>10.0f}{moy:>10.2f}")
        elif choix == "4":
            cl = comp.classement_par("points")
            self._afficher_foot(cl, f"{nom_ligue} — Toutes saisons")

    def _construire(self, df, teams, abbrevs, nom_comp: str) -> Competition:
        comp = Competition(nom_comp, "football")
        for _, row in df.iterrows():
            hid, aid = int(row["home_team_api_id"]), int(row["away_team_api_id"])
            hg,  ag  = int(row["home_team_goal"]),   int(row["away_team_goal"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(str(tid), Equipe(teams.get(tid, str(tid)), "football", abbrevs.get(tid)))
            comp.equipes[str(hid)].ajouter_match(hg, ag)
            comp.equipes[str(aid)].ajouter_match(ag, hg)
        return comp

    def _choisir_ligue(self, leagues, countries, lg_ctry) -> int | None:
        print("\n  Ligues disponibles :")
        for lid, lname in leagues.items():
            print(f"    {lid} - {lname} ({countries.get(lg_ctry.get(lid), '?')})")
        try:
            return int(input("  ID de la ligue (0 = toutes) : ").strip()) or None
        except ValueError:
            return None

    def _choisir_saison(self, df_match) -> str | None:
        saisons = sorted(df_match["season"].unique())
        print("\n  Saisons :", ", ".join(saisons))
        saison = input("  Saison (ex: 2014/2015) : ").strip()
        return saison if saison in saisons else None

    def _afficher_foot(self, classement: list, titre: str) -> None:
        print(f"\n=== {titre} ===\n")
        print(f"  {'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'N':>4}{'D':>4}{'BP':>5}{'BC':>5}{'DB':>6}{'Pts':>5}")
        print("  " + "─" * 72)
        for i, e in enumerate(classement, 1):
            print(f"  {i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.nuls:>4}"
                  f"{e.defaites:>4}{e.score_pour:>5.0f}{e.score_contre:>5.0f}"
                  f"{e.difference_score:>+6.0f}{e.points:>5}")


CompetitionLoader.register("football", FootballCompetitionLoader)


# ── Basketball ────────────────────────────────────────────────────────────────

class BasketballCompetitionLoader:

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def run(self) -> None:
        df_game = pd.read_csv(self.DATA_GAMES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        abbrevs = {}
        for _, row in df_team.iterrows():
            teams[row["id"]] = row["full_name"]
            abbrevs[row["id"]] = row["abbreviation"]

        print("\n  Type de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("  Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        comp = Competition(f"NBA — {season_type}", "basketball")
        for _, row in df.iterrows():
            hid, aid   = int(row["team_id_home"]), int(row["team_id_away"])
            hpts, apts = int(row["pts_home"]),     int(row["pts_away"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(str(tid), Equipe(teams.get(tid, str(tid)), "basketball", abbrevs.get(tid)))
            eh = comp.equipes[str(hid)]; ea = comp.equipes[str(aid)]
            eh.ajouter_match(hpts, apts, nul_possible=False)
            ea.ajouter_match(apts, hpts, nul_possible=False)
            eh.rebonds += float(row["reb_home"] or 0); eh.passes += float(row["ast_home"] or 0)
            eh.interceptions += float(row["stl_home"] or 0); eh.contres += float(row["blk_home"] or 0)
            ea.rebonds += float(row["reb_away"] or 0); ea.passes += float(row["ast_away"] or 0)
            ea.interceptions += float(row["stl_away"] or 0); ea.contres += float(row["blk_away"] or 0)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_competition(comp, nul_possible=False)
        if nb: print(f"  (+ {nb} nouveau(x) résultat(s) inclus)")

        print("\n  Que voulez-vous faire ?")
        print("  1 - Classement général  2 - Meilleures attaques  3 - Meilleures défenses")
        print("  4 - Classement rebonds  5 - Classement passes")
        choix = input("\n  Votre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires")
            print(f"\n=== {comp.nom} ===\n")
            print(f"  {'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Pts+':>6}{'Pts-':>6}{'Diff':>7}")
            print("  " + "─" * 65)
            for i, e in enumerate(cl, 1):
                print(f"  {i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>6.0f}{e.score_contre:>6.0f}{e.difference_score:>+7.0f}")
        elif choix in ["2", "3", "4", "5"]:
            critere = {"2": ("score_pour", "Pts marqués"), "3": ("score_contre", "Pts encaissés"),
                       "4": ("rebonds", "Rebonds"), "5": ("passes", "Passes")}[choix]
            if choix == "3":
                cl = sorted(comp.equipes.values(), key=lambda e: e.score_contre)
            else:
                cl = comp.classement_par(critere[0])
            print(f"\n=== {critere[1]} — {comp.nom} ===\n")
            print(f"  {'#':<4}{'Équipe':<30}{critere[1]:>12}{'Moy/match':>10}")
            print("  " + "─" * 58)
            for i, e in enumerate(cl, 1):
                val = getattr(e, critere[0])
                moy = val / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i:<4}{e.nom:<30}{val:>12.0f}{moy:>10.1f}")


CompetitionLoader.register("basketball", BasketballCompetitionLoader)


# ── League of Legends ─────────────────────────────────────────────────────────

class LoLCompetitionLoader:

    DATA_MATCHES = "data/LOL/match.csv"
    DATA_TEAMS = "data/LOL/team.csv"

    def run(self) -> None:
        df = pd.read_csv(self.DATA_MATCHES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams_info = {}
        for _, row in df_team.iterrows():
            teams_info[row["team_abbreviation"]] = row["team"]

        comp = Competition("LoL EMEA 2025", "LOL")
        for _, row in df.iterrows():
            for side, opp in [("blue", "red"), ("red", "blue")]:
                abrev = str(row[f"team_{side}"])
                if abrev not in comp.equipes:
                    comp.ajouter_equipe(abrev, Equipe(teams_info.get(abrev, abrev), "LOL", abrev))
                e = comp.equipes[abrev]
                e.matchs_joues += 1
                e.kills += int(row[f"kills_team_{side}"] or 0)
                e.dragons += int(row[f"dragons_team_{side}"] or 0)
                e.barons += int(row[f"barons_team_{side}"] or 0)
                e.gold += float(row[f"gold_team_{side}"] or 0)
                e.score_pour += int(row[f"kills_team_{side}"] or 0)
                e.score_contre += int(row[f"kills_team_{opp}"] or 0)
                if str(row["winner"]) == abrev:
                    e.victoires += 1
                    e.points += 1
                else:
                    e.defaites += 1

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_competition(comp, nul_possible=False)
        if nb: print(f"  (+ {nb} nouveau(x) résultat(s) inclus)")

        print("\n  Que voulez-vous faire ?")
        print("  1 - Classement général  2 - Classement kills  3 - Dragons & Barons  4 - Gold")
        choix = input("\n  Votre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires")
            print(f"\n=== {comp.nom} ===\n")
            print(f"  {'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
            print("  " + "─" * 52)
            for i, e in enumerate(cl, 1):
                print(f"  {i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}{e.winrate:>6.1f}%")
        elif choix == "2":
            cl = comp.classement_par("kills")
            print(f"\n=== Kills — {comp.nom} ===\n")
            for i, e in enumerate(cl, 1):
                moy = e.kills / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i}. {e.nom:<25} {e.kills} kills  (moy: {moy:.1f}/match)")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: e.dragons + e.barons, reverse=True)
            print(f"\n=== Objectifs — {comp.nom} ===\n")
            for i, e in enumerate(cl, 1):
                print(f"  {i}. {e.nom:<25} Dragons: {e.dragons}  Barons: {e.barons}")
        elif choix == "4":
            cl = comp.classement_par("gold")
            print(f"\n=== Gold — {comp.nom} ===\n")
            for i, e in enumerate(cl, 1):
                moy = e.gold / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i}. {e.nom:<25} {e.gold:.0f} gold  (moy: {moy:.0f}/match)")


CompetitionLoader.register("LOL", LoLCompetitionLoader)


# ── Tennis ────────────────────────────────────────────────────────────────────

class TennisCompetitionLoader:

    DATA_ATP_MATCHES = "data/tennis/atp_matches_2024.csv"
    DATA_WTA_MATCHES = "data/tennis/wta_matches_2024.csv"
    DATA_ATP_PLAYERS = "data/tennis/atp_players_2024.csv"
    DATA_WTA_PLAYERS = "data/tennis/wta_players_2024.csv"

    def run(self) -> None:
        df_atp_p = pd.read_csv(self.DATA_ATP_PLAYERS)
        df_wta_p = pd.read_csv(self.DATA_WTA_PLAYERS)
        df_atp_m = pd.read_csv(self.DATA_ATP_MATCHES)
        df_wta_m = pd.read_csv(self.DATA_WTA_MATCHES)
        atp_players = {}
        for _, row in df_atp_p.iterrows():
            atp_players[str(row["player_id"])] = row["name_first"] + " " + row["name_last"]

        wta_players = {}
        for _, row in df_wta_p.iterrows():
            wta_players[str(row["player_id"])] = row["name_first"] + " " + row["name_last"]

        circuit = input("\n  Circuit (ATP / WTA) : ").strip().upper()
        if circuit == "ATP":
            df_m, players = df_atp_m, atp_players
        elif circuit == "WTA":
            df_m, players = df_wta_m, wta_players
        else:
            print("  Circuit invalide.")
            return

        print("\n  1 - Classement général  2 - Classement par tournoi")
        choix = input("  Votre choix : ").strip()

        if choix == "2":
            tournois = list(df_m["tourney_name"].unique())
            print("\n  Tournois disponibles :")
            for i, t in enumerate(tournois[:20], 1):
                print(f"    {i}. {t}")
            try:
                idx = int(input("  Numéro du tournoi : ").strip()) - 1
                df_m = df_m[df_m["tourney_name"] == tournois[idx]]
                nom_comp = tournois[idx]
            except (ValueError, IndexError):
                print("  Choix invalide.")
                return
        else:
            nom_comp = f"{circuit} 2024"

        comp = Competition(nom_comp, "tennis")
        for _, row in df_m.iterrows():
            wid = str(int(row["winner_id"]))
            lid = str(int(row["loser_id"]))
            for pid in [wid, lid]:
                if pid not in comp.equipes:
                    comp.ajouter_equipe(pid, Equipe(players.get(pid, pid), "tennis"))
            comp.equipes[wid].ajouter_match(1, 0, nul_possible=False)
            comp.equipes[lid].ajouter_match(0, 1, nul_possible=False)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_competition(comp, nul_possible=False)
        if nb: print(f"  (+ {nb} nouveau(x) résultat(s) inclus)")

        cl = comp.classement_par("victoires")
        print(f"\n=== {comp.nom} ===\n")
        print(f"  {'#':<4}{'Joueur':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
        print("  " + "─" * 52)
        for i, e in enumerate(cl[:20], 1):
            print(f"  {i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}{e.winrate:>6.1f}%")


CompetitionLoader.register("tennis", TennisCompetitionLoader)


# ── Volleyball ────────────────────────────────────────────────────────────────

class VolleyCompetitionLoader:

    DATA_MEN_MATCHES = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES = "data/volley/country.csv"

    def run(self) -> None:
        df_men = pd.read_csv(self.DATA_MEN_MATCHES)
        df_women = pd.read_csv(self.DATA_WOMEN_MATCHES)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)
        countries = {}
        for _, row in df_countries.iterrows():
            countries[row["code"]] = row["country"]
        df_men["code_1"]   = df_men["country_code_1"]
        df_men["code_2"]   = df_men["country_code_2"]
        df_women["code_1"] = df_women["country_1"]
        df_women["code_2"] = df_women["country_2"]

        cat = input("\n  Catégorie (Hommes / Femmes) : ").strip().lower()
        df = df_men if cat in ["hommes", "h", "men"] else df_women
        genre = "Hommes" if cat in ["hommes", "h", "men"] else "Femmes"

        comp = Competition(f"Volley {genre} — JO 2024", "volley")
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            for code in [c1, c2]:
                if code not in comp.equipes:
                    comp.ajouter_equipe(code, Equipe(countries.get(code, code), "volley", code))
            comp.equipes[c1].ajouter_match(s1, s2, nul_possible=False)
            comp.equipes[c2].ajouter_match(s2, s1, nul_possible=False)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_competition(comp, nul_possible=False)
        if nb: print(f"  (+ {nb} nouveau(x) résultat(s) inclus)")

        print("\n  1 - Classement général  2 - Classement sets gagnés")
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires")
            print(f"\n=== {comp.nom} ===\n")
            print(f"  {'#':<4}{'Pays':<25}{'MJ':>4}{'V':>4}{'D':>4}{'Sets+':>7}{'Sets-':>7}{'Diff':>7}")
            print("  " + "─" * 62)
            for i, e in enumerate(cl, 1):
                print(f"  {i:<4}{e.nom:<25}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>7.0f}{e.score_contre:>7.0f}{e.difference_score:>+7.0f}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Sets gagnés — {comp.nom} ===\n")
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"  {i}. {e.nom:<25} {e.score_pour:.0f} sets  (moy: {moy:.2f}/match)")


CompetitionLoader.register("volley", VolleyCompetitionLoader)
