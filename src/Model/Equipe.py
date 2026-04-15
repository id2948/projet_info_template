from typing import Optional
from src.sport import Sport


class Equipe:
    """Représente une équipe avec ses statistiques, tous sports confondus."""

    def __init__(self, nom: str, sport: str, abreviation: Optional[str] = None):
        self.nom         = nom
        self.sport       = sport
        self.abreviation = abreviation

        # Stats communes
        self.matchs_joues = 0
        self.victoires    = 0
        self.defaites     = 0
        self.nuls         = 0
        self.points       = 0
        self.score_pour   = 0.0
        self.score_contre = 0.0

        # Stats basketball
        self.rebonds       = 0.0
        self.passes        = 0.0
        self.interceptions = 0.0
        self.contres       = 0.0

        # Stats LoL
        self.kills   = 0
        self.dragons = 0
        self.barons  = 0
        self.gold    = 0.0

    @property
    def difference_score(self) -> float:
        return self.score_pour - self.score_contre

    @property
    def winrate(self) -> float:
        return self.victoires / self.matchs_joues * 100 if self.matchs_joues else 0.0

    def ajouter_match(self, score_pour: float, score_contre: float, nul_possible: bool = True) -> None:
        """Enregistre le résultat d'un match pour cette équipe."""
        self.matchs_joues += 1
        self.score_pour   += score_pour
        self.score_contre += score_contre

        if score_pour > score_contre:
            self.victoires += 1
            self.points    += 3 if nul_possible else 1
        elif nul_possible and score_pour == score_contre:
            self.nuls   += 1
            self.points += 1
        else:
            self.defaites += 1

    def __str__(self):
        return (f"{self.nom:<30} | "
                f"MJ:{self.matchs_joues:>3} V:{self.victoires:>3} "
                f"N:{self.nuls:>3} D:{self.defaites:>3} | "
                f"Pour:{self.score_pour:>6.0f} Contre:{self.score_contre:>6.0f} "
                f"Diff:{self.difference_score:>+7.0f} | Pts:{self.points:>4}")

    def __repr__(self):
        return f"Equipe(nom={self.nom}, sport={self.sport}, pts={self.points})"

    # ──────────────────────────────────────────────
    #  Menu principal
    # ──────────────────────────────────────────────

    @staticmethod
    def run_menu(sport: Sport) -> None:
        if sport.nom == "football":
            Equipe._menu_football()
        elif sport.nom == "basketball":
            Equipe._menu_basketball()
        elif sport.nom == "LOL":
            Equipe._menu_lol()
        elif sport.nom == "tennis":
            Equipe._menu_tennis()
        elif sport.nom == "volley":
            Equipe._menu_volley()
        else:
            print(f"Pas de stats d'équipe disponibles pour {sport.nom}.")

    # ══════════════════════════════════════════════
    #  FOOTBALL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_football() -> None:
        import pandas as pd
        df_match = pd.read_csv("data/football/match.csv")
        df_team  = pd.read_csv("data/football/team.csv")
        teams    = dict(zip(df_team["team_api_id"], df_team["team_long_name"]))

        nom = input("Nom de l'équipe : ").strip()
        matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not matches: print("Aucune équipe trouvée."); return
        if len(matches) > 1:
            for tid, tname in matches.items(): print(f"  {tid} - {tname}")
            try: team_id = int(input("ID : ").strip())
            except ValueError: return
        else:
            team_id = list(matches.keys())[0]

        saisons = sorted(df_match["season"].unique())
        print("\nSaisons :", ", ".join(saisons))
        saison = input("Saison (ex: 2014/2015) : ").strip()
        if saison not in saisons: print("Saison non trouvée."); return

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

        print(f"\n=== {e.nom} — {saison} ===\n")
        print(f"  Matchs joués     : {e.matchs_joues}")
        print(f"  Victoires        : {e.victoires}  Nuls : {e.nuls}  Défaites : {e.defaites}")
        print(f"  Buts marqués     : {e.score_pour:.0f}  (moy: {e.score_pour/e.matchs_joues:.2f}/match)")
        print(f"  Buts encaissés   : {e.score_contre:.0f}  (moy: {e.score_contre/e.matchs_joues:.2f}/match)")
        print(f"  Différence       : {e.difference_score:+.0f}")
        print(f"  Points           : {e.points}")
        print(f"  Winrate          : {e.winrate:.1f}%")

    # ══════════════════════════════════════════════
    #  BASKETBALL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_basketball() -> None:
        import pandas as pd
        df_game = pd.read_csv("data/basketball/game.csv")
        df_team = pd.read_csv("data/basketball/team.csv")
        teams   = dict(zip(df_team["id"], df_team["full_name"]))

        print("\nType de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        nom = input("Nom de l'équipe : ").strip()
        team_matches = {tid: tname for tid, tname in teams.items() if nom.lower() in tname.lower()}
        if not team_matches: print("Aucune équipe trouvée."); return
        team_id = list(team_matches.keys())[0]

        df = df[(df["team_id_home"] == team_id) | (df["team_id_away"] == team_id)]
        e = Equipe(teams.get(team_id, str(team_id)), "basketball")
        for _, row in df.iterrows():
            if int(row["team_id_home"]) == team_id:
                e.ajouter_match(int(row["pts_home"]), int(row["pts_away"]), nul_possible=False)
                e.rebonds += float(row["reb_home"] or 0)
                e.passes  += float(row["ast_home"] or 0)
                e.interceptions += float(row["stl_home"] or 0)
                e.contres += float(row["blk_home"] or 0)
            else:
                e.ajouter_match(int(row["pts_away"]), int(row["pts_home"]), nul_possible=False)
                e.rebonds += float(row["reb_away"] or 0)
                e.passes  += float(row["ast_away"] or 0)
                e.interceptions += float(row["stl_away"] or 0)
                e.contres += float(row["blk_away"] or 0)

        mj = e.matchs_joues
        print(f"\n=== {e.nom} — {season_type} ===\n")
        print(f"  Matchs joués       : {mj}")
        print(f"  Victoires          : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Points marqués     : {e.score_pour:.0f}  (moy: {e.score_pour/mj:.1f}/match)")
        print(f"  Points encaissés   : {e.score_contre:.0f}  (moy: {e.score_contre/mj:.1f}/match)")
        print(f"  Rebonds            : {e.rebonds:.0f}  (moy: {e.rebonds/mj:.1f}/match)")
        print(f"  Passes décisives   : {e.passes:.0f}  (moy: {e.passes/mj:.1f}/match)")
        print(f"  Interceptions      : {e.interceptions:.0f}  (moy: {e.interceptions/mj:.1f}/match)")
        print(f"  Contres            : {e.contres:.0f}  (moy: {e.contres/mj:.1f}/match)")

    # ══════════════════════════════════════════════
    #  LOL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_lol() -> None:
        import pandas as pd
        df = pd.read_csv("data/LOL/match.csv")
        df_team = pd.read_csv("data/LOL/team.csv")
        teams_info = dict(zip(df_team["team_abbreviation"], df_team["team"]))

        nom = input("Nom ou abréviation de l'équipe : ").strip()
        equipes_trouvees = {abrev: tname for abrev, tname in teams_info.items()
                            if nom.lower() in tname.lower() or nom.lower() in abrev.lower()}
        if not equipes_trouvees: print("Aucune équipe trouvée."); return
        abrev = list(equipes_trouvees.keys())[0]

        e = Equipe(teams_info.get(abrev, abrev), "LOL", abrev)
        for _, row in df.iterrows():
            for side, opp in [("blue", "red"), ("red", "blue")]:
                if str(row[f"team_{side}"]) == abrev:
                    e.matchs_joues += 1
                    e.kills   += int(row[f"kills_team_{side}"] or 0)
                    e.dragons += int(row[f"dragons_team_{side}"] or 0)
                    e.barons  += int(row[f"barons_team_{side}"] or 0)
                    e.gold    += float(row[f"gold_team_{side}"] or 0)
                    e.score_pour   += int(row[f"kills_team_{side}"] or 0)
                    e.score_contre += int(row[f"kills_team_{opp}"] or 0)
                    if str(row["winner"]) == abrev:
                        e.victoires += 1
                        e.points    += 1
                    else:
                        e.defaites += 1

        mj = e.matchs_joues
        print(f"\n=== {e.nom} ({e.abreviation}) ===\n")
        print(f"  Matchs joués  : {mj}")
        print(f"  Victoires     : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Kills totaux  : {e.kills}  (moy: {e.kills/mj:.1f}/match)")
        print(f"  Dragons       : {e.dragons}  (moy: {e.dragons/mj:.1f}/match)")
        print(f"  Barons        : {e.barons}  (moy: {e.barons/mj:.1f}/match)")
        print(f"  Gold total    : {e.gold:.0f}  (moy: {e.gold/mj:.0f}/match)")

    # ══════════════════════════════════════════════
    #  TENNIS
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_tennis() -> None:
        import pandas as pd
        df_atp_m = pd.read_csv("data/tennis/atp_matches_2024.csv")
        df_wta_m = pd.read_csv("data/tennis/wta_matches_2024.csv")
        df_atp_p = pd.read_csv("data/tennis/atp_players_2024.csv")
        df_wta_p = pd.read_csv("data/tennis/wta_players_2024.csv")

        atp_players = dict(zip(df_atp_p["player_id"].astype(str),
                               df_atp_p["name_first"] + " " + df_atp_p["name_last"]))
        wta_players = dict(zip(df_wta_p["player_id"].astype(str),
                               df_wta_p["name_first"] + " " + df_wta_p["name_last"]))

        circuit = input("\nCircuit (ATP / WTA) : ").strip().upper()
        if circuit == "ATP":
            df_m, players = df_atp_m, atp_players
        elif circuit == "WTA":
            df_m, players = df_wta_m, wta_players
        else:
            print("Circuit invalide."); return

        nom = input("Nom du joueur : ").strip()
        pid_trouve = None
        for pid, pname in players.items():
            if nom.lower() in pname.lower():
                pid_trouve = pid
                break
        if not pid_trouve: print("Joueur non trouvé."); return

        e = Equipe(players[pid_trouve], "tennis")
        for _, row in df_m.iterrows():
            wid = str(int(row["winner_id"]))
            lid = str(int(row["loser_id"]))
            if wid == pid_trouve:
                e.ajouter_match(1, 0, nul_possible=False)
            elif lid == pid_trouve:
                e.ajouter_match(0, 1, nul_possible=False)

        print(f"\n=== {e.nom} — {circuit} 2024 ===\n")
        print(f"  Matchs joués : {e.matchs_joues}")
        print(f"  Victoires    : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")

    # ══════════════════════════════════════════════
    #  VOLLEY
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_volley() -> None:
        import pandas as pd
        df_men   = pd.read_csv("data/volley/match_men.csv")
        df_women = pd.read_csv("data/volley/match_women.csv")
        df_countries = pd.read_csv("data/volley/country.csv")
        countries = dict(zip(df_countries["code"], df_countries["country"]))

        df_men["code_1"]   = df_men["country_code_1"]
        df_men["code_2"]   = df_men["country_code_2"]
        df_women["code_1"] = df_women["country_1"]
        df_women["code_2"] = df_women["country_2"]

        cat = input("\nCatégorie (Hommes / Femmes) : ").strip().lower()
        df  = df_men if cat in ["hommes", "h", "men"] else df_women
        genre = "Hommes" if cat in ["hommes", "h", "men"] else "Femmes"

        nom = input("Nom du pays : ").strip()
        code_trouve = None
        for code, pays in countries.items():
            if nom.lower() in pays.lower():
                code_trouve = code
                break
        if not code_trouve: print("Pays non trouvé."); return

        e = Equipe(countries[code_trouve], "volley", code_trouve)
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            if c1 == code_trouve:
                e.ajouter_match(s1, s2, nul_possible=False)
            elif c2 == code_trouve:
                e.ajouter_match(s2, s1, nul_possible=False)

        print(f"\n=== {e.nom} — Volley {genre} JO 2024 ===\n")
        print(f"  Matchs joués  : {e.matchs_joues}")
        print(f"  Victoires     : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Sets gagnés   : {e.score_pour:.0f}")
        print(f"  Sets perdus   : {e.score_contre:.0f}")
        print(f"  Différence    : {e.difference_score:+.0f}")