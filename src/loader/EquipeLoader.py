import pandas as pd

from src.sport import Sport
from src.Model.Equipe import Equipe


class EquipeLoader:
    """Dispatcher pour les statistiques d'équipe selon le sport.

    Les loaders spécifiques s'enregistrent via `register`.
    Chaque loader implémente `run()` qui affiche les stats pour une équipe.
    """

    _loaders = {}

    @staticmethod
    def register(sport_nom: str, loader) -> None:
        EquipeLoader._loaders[sport_nom] = loader

    def run(self, sport: Sport) -> None:
        """Lance le menu de stats d'équipe pour le sport sélectionné.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        loader = self._loaders.get(sport.nom)
        if loader is None:
            print(f"Pas de stats d'équipe disponibles pour {sport.nom}.")
            return
        loader().run()


# ── Football ──────────────────────────────────────────────────────────────────

class FootballEquipeLoader:

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS   = "data/football/team.csv"

    def run(self) -> None:
        df_match = pd.read_csv(self.DATA_MATCHES)
        df_team  = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        for _, row in df_team.iterrows():
            teams[row["team_api_id"]] = row["team_long_name"]

        nom = input("  Nom de l'équipe : ").strip()
        matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not matches:
            print("  Aucune équipe trouvée.")
            return
        if len(matches) > 1:
            for tid, tname in matches.items():
                print(f"  {tid} - {tname}")
            try:
                team_id = int(input("  ID : ").strip())
            except ValueError:
                return
        else:
            team_id = list(matches.keys())[0]

        saisons = sorted(df_match["season"].unique())
        print("\n  Saisons :", ", ".join(saisons))
        saison = input("  Saison (ex: 2014/2015) : ").strip()
        if saison not in saisons:
            print("  Saison non trouvée.")
            return

        df = df_match[
            ((df_match["home_team_api_id"] == team_id) | (df_match["away_team_api_id"] == team_id)) &
            (df_match["season"] == saison)
        ]
        e = Equipe(teams.get(team_id, str(team_id)), "football")
        for _, row in df.iterrows():
            if int(row["home_team_api_id"]) == team_id:
                e.ajouter_match(int(row["home_team_goal"]), int(row["away_team_goal"]))
            else:
                e.ajouter_match(int(row["away_team_goal"]), int(row["home_team_goal"]))

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_equipe(e, e.nom)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — {saison} ===\n")
        print(f"  Matchs joués   : {e.matchs_joues}")
        print(f"  Victoires      : {e.victoires}  Nuls : {e.nuls}  Défaites : {e.defaites}")
        print(f"  Buts marqués   : {e.score_pour:.0f}  (moy: {e.score_pour/e.matchs_joues:.2f}/match)")
        print(f"  Buts encaissés : {e.score_contre:.0f}  (moy: {e.score_contre/e.matchs_joues:.2f}/match)")
        print(f"  Différence     : {e.difference_score:+.0f}  |  Points : {e.points}  |  Winrate : {e.winrate:.1f}%")


EquipeLoader.register("football", FootballEquipeLoader)


# ── Basketball ────────────────────────────────────────────────────────────────

class BasketballEquipeLoader:

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def run(self) -> None:
        df_game = pd.read_csv(self.DATA_GAMES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        for _, row in df_team.iterrows():
            teams[row["id"]] = row["full_name"]

        print("\n  Type de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("  Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        nom = input("  Nom de l'équipe : ").strip()
        team_matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not team_matches:
            print("  Aucune équipe trouvée.")
            return
        team_id = list(team_matches.keys())[0]

        df = df[(df["team_id_home"] == team_id) | (df["team_id_away"] == team_id)]
        e = Equipe(teams.get(team_id, str(team_id)), "basketball")
        for _, row in df.iterrows():
            if int(row["team_id_home"]) == team_id:
                e.ajouter_match(int(row["pts_home"]), int(row["pts_away"]), nul_possible=False)
                e.rebonds += float(row["reb_home"] or 0); e.passes += float(row["ast_home"] or 0)
                e.interceptions += float(row["stl_home"] or 0); e.contres += float(row["blk_home"] or 0)
            else:
                e.ajouter_match(int(row["pts_away"]), int(row["pts_home"]), nul_possible=False)
                e.rebonds += float(row["reb_away"] or 0); e.passes += float(row["ast_away"] or 0)
                e.interceptions += float(row["stl_away"] or 0); e.contres += float(row["blk_away"] or 0)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        mj = e.matchs_joues
        print(f"\n=== {e.nom} — {season_type} ===\n")
        print(f"  Matchs joués     : {mj}  |  V:{e.victoires} D:{e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Points marqués   : {e.score_pour:.0f}  (moy: {e.score_pour/mj:.1f}/match)")
        print(f"  Points encaissés : {e.score_contre:.0f}  (moy: {e.score_contre/mj:.1f}/match)")
        print(f"  Rebonds          : {e.rebonds:.0f}  (moy: {e.rebonds/mj:.1f})  |  Passes : {e.passes:.0f}  (moy: {e.passes/mj:.1f})")
        print(f"  Interceptions    : {e.interceptions:.0f}  (moy: {e.interceptions/mj:.1f})  |  Contres : {e.contres:.0f}  (moy: {e.contres/mj:.1f})")


EquipeLoader.register("basketball", BasketballEquipeLoader)


# ── League of Legends ─────────────────────────────────────────────────────────

class LoLEquipeLoader:

    DATA_MATCHES = "data/LOL/match.csv"
    DATA_TEAMS   = "data/LOL/team.csv"

    def run(self) -> None:
        df      = pd.read_csv(self.DATA_MATCHES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams_info = {}
        for _, row in df_team.iterrows():
            teams_info[row["team_abbreviation"]] = row["team"]

        nom = input("  Nom ou abréviation de l'équipe : ").strip()
        equipes_trouvees = {abrev: tname for abrev, tname in teams_info.items()
                            if nom.lower() in tname.lower() or nom.lower() in abrev.lower()}
        if not equipes_trouvees:
            print("  Aucune équipe trouvée.")
            return
        abrev = list(equipes_trouvees.keys())[0]

        e = Equipe(teams_info.get(abrev, abrev), "LOL", abrev)
        for _, row in df.iterrows():
            for side, opp in [("blue", "red"), ("red", "blue")]:
                if str(row[f"team_{side}"]) == abrev:
                    e.matchs_joues  += 1
                    e.kills         += int(row[f"kills_team_{side}"] or 0)
                    e.dragons       += int(row[f"dragons_team_{side}"] or 0)
                    e.barons        += int(row[f"barons_team_{side}"] or 0)
                    e.gold          += float(row[f"gold_team_{side}"] or 0)
                    e.score_pour    += int(row[f"kills_team_{side}"] or 0)
                    e.score_contre  += int(row[f"kills_team_{opp}"] or 0)
                    if str(row["winner"]) == abrev:
                        e.victoires += 1; e.points += 1
                    else:
                        e.defaites  += 1

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        mj = e.matchs_joues
        print(f"\n=== {e.nom} ({e.abreviation}) ===\n")
        print(f"  Matchs joués : {mj}  |  V:{e.victoires} D:{e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Kills totaux : {e.kills}  (moy: {e.kills/mj:.1f}/match)")
        print(f"  Dragons      : {e.dragons}  (moy: {e.dragons/mj:.1f})  |  Barons : {e.barons}  (moy: {e.barons/mj:.1f})")
        print(f"  Gold total   : {e.gold:.0f}  (moy: {e.gold/mj:.0f}/match)")


EquipeLoader.register("LOL", LoLEquipeLoader)


# ── Tennis ────────────────────────────────────────────────────────────────────

class TennisEquipeLoader:

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
            print("  Circuit invalide."); return

        nom = input("  Nom du joueur : ").strip()
        pid = None
        for p_id, p_nom in players.items():
            if nom.lower() in p_nom.lower():
                pid = p_id
                break
        if not pid:
            print("  Joueur non trouvé."); return

        e = Equipe(players[pid], "tennis")
        for _, row in df_m.iterrows():
            wid = str(int(row["winner_id"]))
            lid = str(int(row["loser_id"]))
            if wid == pid:
                e.ajouter_match(1, 0, nul_possible=False)
            elif lid == pid:
                e.ajouter_match(0, 1, nul_possible=False)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — {circuit} 2024 ===\n")
        print(f"  Matchs joués : {e.matchs_joues}  |  V:{e.victoires} D:{e.defaites}  ({e.winrate:.1f}% winrate)")


EquipeLoader.register("tennis", TennisEquipeLoader)


# ── Volleyball ────────────────────────────────────────────────────────────────

class VolleyEquipeLoader:

    DATA_MEN_MATCHES   = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES     = "data/volley/country.csv"

    def run(self) -> None:
        df_men   = pd.read_csv(self.DATA_MEN_MATCHES)
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
        df  = df_men if cat in ["hommes", "h", "men"] else df_women
        genre = "Hommes" if cat in ["hommes", "h", "men"] else "Femmes"

        nom = input("  Nom du pays : ").strip()
        code = None
        for c, pays in countries.items():
            if nom.lower() in pays.lower():
                code = c
                break
        if not code:
            print("  Pays non trouvé."); return

        e = Equipe(countries[code], "volley", code)
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            if c1 == code:
                e.ajouter_match(s1, s2, nul_possible=False)
            elif c2 == code:
                e.ajouter_match(s2, s1, nul_possible=False)

        from src.loader.GestionResultats import GestionResultats
        nb = GestionResultats.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        print(f"\n=== {e.nom} — Volley {genre} JO 2024 ===\n")
        print(f"  Matchs joués : {e.matchs_joues}  |  V:{e.victoires} D:{e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Sets gagnés  : {e.score_pour:.0f}  |  Sets perdus : {e.score_contre:.0f}  |  Diff : {e.difference_score:+.0f}")


EquipeLoader.register("volley", VolleyEquipeLoader)
