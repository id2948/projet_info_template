from typing import Optional
from src.sport import Sport
from src.Model.Equipe import Equipe


class Competition:
    """Charge les équipes et génère les classements pour chaque sport."""

    def __init__(self, nom: str, sport: str):
        self.nom    = nom
        self.sport  = sport
        self.equipes: dict[str, Equipe] = {}

    def ajouter_equipe(self, cle: str, equipe: Equipe) -> None:
        self.equipes[cle] = equipe

    def classement_par(self, *criteres) -> list[Equipe]:
        """Trie les équipes selon les critères donnés (attributs de Equipe)."""
        return sorted(
            self.equipes.values(),
            key=lambda e: tuple(-getattr(e, c) for c in criteres)
        )

    def __repr__(self):
        return f"Competition(nom={self.nom}, sport={self.sport}, equipes={len(self.equipes)})"

    # ──────────────────────────────────────────────
    #  Menu principal
    # ──────────────────────────────────────────────

    @staticmethod
    def run_menu(sport: Sport) -> None:
        if sport.nom == "football":
            Competition._menu_football()
        elif sport.nom == "basketball":
            Competition._menu_basketball()
        elif sport.nom == "LOL":
            Competition._menu_lol()
        elif sport.nom == "tennis":
            Competition._menu_tennis()
        elif sport.nom == "volley":
            Competition._menu_volley()
        else:
            print(f"Pas de classement disponible pour {sport.nom}.")

    # ──────────────────────────────────────────────
    #  Affichage générique
    # ──────────────────────────────────────────────

    @staticmethod
    def _afficher_classement_foot(classement: list[Equipe], titre: str) -> None:
        print(f"\n=== {titre} ===\n")
        print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'N':>4}{'D':>4}{'BP':>5}{'BC':>5}{'DB':>6}{'Pts':>5}")
        print("-" * 72)
        for i, e in enumerate(classement, 1):
            print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.nuls:>4}"
                  f"{e.defaites:>4}{e.score_pour:>5.0f}{e.score_contre:>5.0f}"
                  f"{e.difference_score:>+6.0f}{e.points:>5}")

    @staticmethod
    def _afficher_classement_simple(classement: list[Equipe], titre: str, col1: str, col2: str) -> None:
        print(f"\n=== {titre} ===\n")
        print(f"{'#':<4}{'Équipe':<30}{col1:>8}{col2:>10}")
        print("-" * 55)
        for i, e in enumerate(classement, 1):
            val1 = getattr(e, col1.strip(), 0)
            mj   = e.matchs_joues
            moy  = val1 / mj if mj else 0
            print(f"{i:<4}{e.nom:<30}{val1:>8.0f}{moy:>10.2f}")

    # ══════════════════════════════════════════════
    #  FOOTBALL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_football() -> None:
        import pandas as pd
        df_match   = pd.read_csv("data/football/match.csv")
        df_team    = pd.read_csv("data/football/team.csv")
        df_league  = pd.read_csv("data/football/league.csv")
        df_country = pd.read_csv("data/football/country.csv")

        teams    = dict(zip(df_team["team_api_id"],  df_team["team_long_name"]))
        abbrevs  = dict(zip(df_team["team_api_id"],  df_team["team_short_name"]))
        leagues  = dict(zip(df_league["id"],          df_league["name"]))
        countries= dict(zip(df_country["id"],         df_country["name"]))
        lg_ctry  = dict(zip(df_league["id"],          df_league["country_id"]))

        print("\nQue voulez-vous faire ?")
        print("1 - Classement d'une ligue pour une saison")
        print("2 - Meilleures attaques d'une ligue")
        print("3 - Meilleures défenses d'une ligue")
        print("4 - Classement général toutes saisons")
        choix = input("\nVotre choix : ").strip()

        lid    = Competition._choisir_ligue(leagues, countries, lg_ctry)
        if lid is None: return
        saison = Competition._choisir_saison(df_match) if choix in ["1","2","3"] else None

        df = df_match.copy()
        if lid:    df = df[df["league_id"] == lid]
        if saison: df = df[df["season"] == saison]
        if df.empty: print("Aucun match trouvé."); return

        comp = Competition._foot_construire(df, teams, abbrevs, leagues.get(lid, str(lid)))

        if choix == "1":
            cl = comp.classement_par("points", "difference_score", "score_pour")
            Competition._afficher_classement_foot(cl, f"{comp.nom} — {saison}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Meilleures attaques — {comp.nom} {saison} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Buts':>6}{'Moy/match':>10}")
            print("-" * 52)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_pour:>6.0f}{moy:>10.2f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: e.score_contre)
            print(f"\n=== Meilleures défenses — {comp.nom} {saison} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Buts enc.':>10}{'Moy/match':>10}")
            print("-" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_contre / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_contre:>10.0f}{moy:>10.2f}")
        elif choix == "4":
            comp_all = Competition._foot_construire(df_match, teams, abbrevs, "Toutes ligues — Toutes saisons")
            cl = comp_all.classement_par("points", "difference_score")
            Competition._afficher_classement_foot(cl[:30], comp_all.nom)

    @staticmethod
    def _foot_construire(df, teams, abbrevs, nom_comp: str) -> "Competition":
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

    @staticmethod
    def _choisir_ligue(leagues, countries, lg_ctry) -> Optional[int]:
        print("\nLigues disponibles :")
        for lid, lname in leagues.items():
            print(f"  {lid} - {lname} ({countries.get(lg_ctry.get(lid), '?')})")
        try:
            return int(input("ID de la ligue (0 = toutes) : ").strip()) or None
        except ValueError:
            return None

    @staticmethod
    def _choisir_saison(df_match) -> Optional[str]:
        saisons = sorted(df_match["season"].unique())
        print("\nSaisons :", ", ".join(saisons))
        saison = input("Saison (ex: 2014/2015) : ").strip()
        return saison if saison in saisons else None

    # ══════════════════════════════════════════════
    #  BASKETBALL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_basketball() -> None:
        import pandas as pd
        df_game = pd.read_csv("data/basketball/game.csv")
        df_team = pd.read_csv("data/basketball/team.csv")
        teams   = dict(zip(df_team["id"], df_team["full_name"]))
        abbrevs = dict(zip(df_team["id"], df_team["abbreviation"]))

        print("\nType de saison :", ", ".join(df_game["season_type"].unique()))
        season_type = input("Type de saison : ").strip()
        df = df_game[df_game["season_type"] == season_type]

        comp = Competition(f"NBA — {season_type}", "basketball")
        for _, row in df.iterrows():
            hid, aid = int(row["team_id_home"]), int(row["team_id_away"])
            hpts, apts = int(row["pts_home"]), int(row["pts_away"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(str(tid), Equipe(teams.get(tid, str(tid)), "basketball", abbrevs.get(tid)))
            eh = comp.equipes[str(hid)]
            ea = comp.equipes[str(aid)]
            eh.ajouter_match(hpts, apts, nul_possible=False)
            ea.ajouter_match(apts, hpts, nul_possible=False)
            eh.rebonds += float(row["reb_home"] or 0)
            eh.passes  += float(row["ast_home"] or 0)
            eh.interceptions += float(row["stl_home"] or 0)
            eh.contres += float(row["blk_home"] or 0)
            ea.rebonds += float(row["reb_away"] or 0)
            ea.passes  += float(row["ast_away"] or 0)
            ea.interceptions += float(row["stl_away"] or 0)
            ea.contres += float(row["blk_away"] or 0)

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires)")
        print("2 - Meilleures attaques")
        print("3 - Meilleures défenses")
        print("4 - Classement rebonds")
        print("5 - Classement passes décisives")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Pts+':>6}{'Pts-':>6}{'Diff':>7}")
            print("-" * 65)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>6.0f}{e.score_contre:>6.0f}{e.difference_score:>+7.0f}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Meilleures attaques — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Pts total':>10}{'Moy/match':>10}")
            print("-" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_pour:>10.0f}{moy:>10.1f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: e.score_contre)
            print(f"\n=== Meilleures défenses — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Pts enc.':>10}{'Moy/match':>10}")
            print("-" * 56)
            for i, e in enumerate(cl, 1):
                moy = e.score_contre / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.score_contre:>10.0f}{moy:>10.1f}")
        elif choix == "4":
            cl = comp.classement_par("rebonds")
            print(f"\n=== Classement rebonds — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Rebonds':>8}{'Moy/match':>10}")
            print("-" * 55)
            for i, e in enumerate(cl, 1):
                moy = e.rebonds / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.rebonds:>8.0f}{moy:>10.1f}")
        elif choix == "5":
            cl = comp.classement_par("passes")
            print(f"\n=== Classement passes — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Passes':>8}{'Moy/match':>10}")
            print("-" * 55)
            for i, e in enumerate(cl, 1):
                moy = e.passes / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.passes:>8.0f}{moy:>10.1f}")

    # ══════════════════════════════════════════════
    #  LOL
    # ══════════════════════════════════════════════

    @staticmethod
    def _menu_lol() -> None:
        import pandas as pd
        df = pd.read_csv("data/LOL/match.csv")
        df_team = pd.read_csv("data/LOL/team.csv")
        teams_info = dict(zip(df_team["team_abbreviation"], df_team["team"]))

        comp = Competition("LoL EMEA 2025", "LOL")
        for _, row in df.iterrows():
            for side, opp in [("blue", "red"), ("red", "blue")]:
                abrev = str(row[f"team_{side}"])
                nom   = teams_info.get(abrev, abrev)
                if abrev not in comp.equipes:
                    comp.ajouter_equipe(abrev, Equipe(nom, "LOL", abrev))
                e = comp.equipes[abrev]
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

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires / winrate)")
        print("2 - Classement kills")
        print("3 - Classement dragons & barons")
        print("4 - Classement gold")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
            print("-" * 52)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}"
                      f"{e.defaites:>4}{e.winrate:>6.1f}%")
        elif choix == "2":
            cl = comp.classement_par("kills")
            print(f"\n=== Classement kills — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Kills':>7}{'Moy/match':>10}")
            print("-" * 54)
            for i, e in enumerate(cl, 1):
                moy = e.kills / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.kills:>7}{moy:>10.1f}")
        elif choix == "3":
            cl = sorted(comp.equipes.values(), key=lambda e: -(e.dragons + e.barons))
            print(f"\n=== Classement objectifs — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Dragons':>8}{'Barons':>8}{'Total':>7}")
            print("-" * 60)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<30}{e.dragons:>8}{e.barons:>8}{e.dragons+e.barons:>7}")
        elif choix == "4":
            cl = comp.classement_par("gold")
            print(f"\n=== Classement gold — {comp.nom} ===\n")
            print(f"{'#':<4}{'Équipe':<30}{'Gold total':>12}{'Moy/match':>12}")
            print("-" * 61)
            for i, e in enumerate(cl, 1):
                moy = e.gold / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<30}{e.gold:>12.0f}{moy:>12.0f}")

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

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général par victoires")
        print("2 - Classement par tournoi")
        choix = input("\nVotre choix : ").strip()

        if choix == "2":
            tournois = list(df_m["tourney_name"].unique())
            print("\nTournois disponibles :")
            for i, t in enumerate(tournois[:20], 1):
                print(f"  {i}. {t}")
            try:
                idx = int(input("Numéro du tournoi : ").strip()) - 1
                df_m = df_m[df_m["tourney_name"] == tournois[idx]]
                nom_comp = tournois[idx]
            except (ValueError, IndexError):
                print("Choix invalide."); return
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

        cl = comp.classement_par("victoires")
        print(f"\n=== {comp.nom} ===\n")
        print(f"{'#':<4}{'Joueur':<30}{'MJ':>4}{'V':>4}{'D':>4}{'Win%':>7}")
        print("-" * 52)
        for i, e in enumerate(cl[:20], 1):
            print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}"
                  f"{e.defaites:>4}{e.winrate:>6.1f}%")

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

        comp = Competition(f"Volley {genre} — JO 2024", "volley")
        for _, row in df.iterrows():
            c1, c2 = str(row["code_1"]), str(row["code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            for code in [c1, c2]:
                if code not in comp.equipes:
                    comp.ajouter_equipe(code, Equipe(countries.get(code, code), "volley", code))
            comp.equipes[c1].ajouter_match(s1, s2, nul_possible=False)
            comp.equipes[c2].ajouter_match(s2, s1, nul_possible=False)

        print("\nQue voulez-vous faire ?")
        print("1 - Classement général (victoires)")
        print("2 - Classement sets gagnés")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            cl = comp.classement_par("victoires", "difference_score")
            print(f"\n=== {comp.nom} ===\n")
            print(f"{'#':<4}{'Pays':<25}{'MJ':>4}{'V':>4}{'D':>4}{'Sets+':>7}{'Sets-':>7}{'Diff':>7}")
            print("-" * 62)
            for i, e in enumerate(cl, 1):
                print(f"{i:<4}{e.nom:<25}{e.matchs_joues:>4}{e.victoires:>4}{e.defaites:>4}"
                      f"{e.score_pour:>7.0f}{e.score_contre:>7.0f}{e.difference_score:>+7.0f}")
        elif choix == "2":
            cl = comp.classement_par("score_pour")
            print(f"\n=== Sets gagnés — {comp.nom} ===\n")
            print(f"{'#':<4}{'Pays':<25}{'Sets gagnés':>12}{'Moy/match':>10}")
            print("-" * 54)
            for i, e in enumerate(cl, 1):
                moy = e.score_pour / e.matchs_joues if e.matchs_joues else 0
                print(f"{i:<4}{e.nom:<25}{e.score_pour:>12.0f}{moy:>10.2f}")