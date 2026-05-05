import pandas as pd
from src.sport import Sport
from src.Model.Match import Match


class MatchLoader:
    """Dispatcher qui charge les matchs selon le sport sélectionné.

    Les loaders spécifiques s'enregistrent via `register`.
    Les nouveaux résultats (GestionResultats) sont automatiquement ajoutés.
    """

    _loaders = {}

    @staticmethod
    def register(sport_nom: str, loader) -> None:
        MatchLoader._loaders[sport_nom] = loader

    def load_all_matches(self, sport: Sport) -> list[Match]:
        """Charge tous les matchs du sport, y compris les nouveaux résultats.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné.

        Returns
        -------
        list[Match]
            Matchs historiques + nouveaux résultats enregistrés.
        """
        loader = MatchLoader._loaders.get(sport.nom)
        if loader is None:
            raise Exception(f"Aucun loader enregistré pour {sport.nom}")
        matchs = loader().load_all_matches()
        from src.loader.GestionResultats import GestionResultats
        return matchs + GestionResultats.charger(sport.nom)


# ── Basketball ────────────────────────────────────────────────────────────────

class BasketballMatchLoader:

    DATA_GAMES = "data/basketball/game.csv"
    DATA_TEAMS = "data/basketball/team.csv"

    def load_all_matches(self) -> list[Match]:
        df_games = pd.read_csv(self.DATA_GAMES)
        df_teams = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        for _, row in df_teams.iterrows():
            teams[str(row["id"])] = row["full_name"]
        df = pd.DataFrame({
            "date":        df_games["game_date"],
            "equipe_1":    df_games["team_id_home"].astype(str).map(teams).fillna(df_games["team_id_home"].astype(str)),
            "equipe_2":    df_games["team_id_away"].astype(str).map(teams).fillna(df_games["team_id_away"].astype(str)),
            "score_1":     df_games["pts_home"],
            "score_2":     df_games["pts_away"],
            "sport":       "basketball",
            "season":      df_games["season"],
            "season_type": df_games["season_type"],
        })
        return [Match(**r) for r in df.to_dict("records")]


MatchLoader.register("basketball", BasketballMatchLoader)


# ── Football ──────────────────────────────────────────────────────────────────

class FootballMatchLoader:

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS = "data/football/team.csv"

    def load_all_matches(self) -> list[Match]:
        df_matches = pd.read_csv(self.DATA_MATCHES)
        df_teams = pd.read_csv(self.DATA_TEAMS)
        teams = {}
        for _, row in df_teams.iterrows():
            teams[str(row["team_api_id"])] = row["team_long_name"]
        df = pd.DataFrame({
            "date":      df_matches["date"],
            "equipe_1":  df_matches["home_team_api_id"].astype(str).map(teams).fillna(df_matches["home_team_api_id"].astype(str)),
            "equipe_2":  df_matches["away_team_api_id"].astype(str).map(teams).fillna(df_matches["away_team_api_id"].astype(str)),
            "score_1":   df_matches["home_team_goal"],
            "score_2":   df_matches["away_team_goal"],
            "sport":     "football",
            "league_id": df_matches["league_id"],
            "stage":     df_matches["stage"],
        })
        return [Match(**r) for r in df.to_dict("records")]


MatchLoader.register("football", FootballMatchLoader)


# ── League of Legends ─────────────────────────────────────────────────────────

class LoLMatchLoader:

    DATA_MATCHES = "data/LOL/match.csv"

    def load_all_matches(self) -> list[Match]:
        df = pd.read_csv(self.DATA_MATCHES)
        df_out = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["team_blue"],
            "equipe_2": df["team_red"],
            "score_1":  df["kills_team_blue"],
            "score_2":  df["kills_team_red"],
            "sport":    "LOL",
            "patch":    df["patch"],
            "week":     df["week"],
            "winner":   df["winner"],
        })
        return [Match(**r) for r in df_out.to_dict("records")]


MatchLoader.register("LOL", LoLMatchLoader)


# ── Tennis ────────────────────────────────────────────────────────────────────

class TennisMatchLoader:

    DATA_ATP_MATCHES = "data/tennis/atp_matches_2024.csv"
    DATA_WTA_MATCHES = "data/tennis/wta_matches_2024.csv"
    DATA_ATP_PLAYERS = "data/tennis/atp_players_2024.csv"
    DATA_WTA_PLAYERS = "data/tennis/wta_players_2024.csv"

    def load_all_matches(self) -> list[Match]:
        df_atp_m = pd.read_csv(self.DATA_ATP_MATCHES)
        df_wta_m = pd.read_csv(self.DATA_WTA_MATCHES)
        df_atp_p = pd.read_csv(self.DATA_ATP_PLAYERS)
        df_wta_p = pd.read_csv(self.DATA_WTA_PLAYERS)

        atp_players = {}
        for _, row in df_atp_p.iterrows():
            atp_players[str(row["player_id"])] = row["name_first"] + " " + row["name_last"]

        wta_players = {}
        for _, row in df_wta_p.iterrows():
            wta_players[str(row["player_id"])] = row["name_first"] + " " + row["name_last"]

        df_atp = pd.DataFrame({
            "date":         df_atp_m["tourney_date"].astype(str),
            "equipe_1":     df_atp_m["winner_id"].astype(str).map(atp_players).fillna(df_atp_m["winner_id"].astype(str)),
            "equipe_2":     df_atp_m["loser_id"].astype(str).map(atp_players).fillna(df_atp_m["loser_id"].astype(str)),
            "score_1":      1.0,
            "score_2":      0.0,
            "sport":        "tennis",
            "tourney_name": df_atp_m["tourney_name"],
            "surface":      df_atp_m["surface"],
            "round":        df_atp_m["round"],
        })

        df_wta = pd.DataFrame({
            "date":         df_wta_m["tourney_date"].astype(str),
            "equipe_1":     df_wta_m["winner_id"].astype(str).map(wta_players).fillna(df_wta_m["winner_id"].astype(str)),
            "equipe_2":     df_wta_m["loser_id"].astype(str).map(wta_players).fillna(df_wta_m["loser_id"].astype(str)),
            "score_1":      1.0,
            "score_2":      0.0,
            "sport":        "tennis",
            "tourney_name": df_wta_m["tourney_name"],
            "surface":      df_wta_m["surface"],
            "round":        df_wta_m["round"],
        })

        df_all = pd.concat([df_atp, df_wta], ignore_index=True)
        return [Match(**r) for r in df_all.to_dict("records")]


MatchLoader.register("tennis", TennisMatchLoader)


# ── Volleyball ────────────────────────────────────────────────────────────────

class VolleyMatchLoader:

    DATA_MEN_MATCHES = "data/volley/match_men.csv"
    DATA_WOMEN_MATCHES = "data/volley/match_women.csv"
    DATA_COUNTRIES = "data/volley/country.csv"

    def load_all_matches(self) -> list[Match]:
        df_men = pd.read_csv(self.DATA_MEN_MATCHES)
        df_women = pd.read_csv(self.DATA_WOMEN_MATCHES)
        df_countries = pd.read_csv(self.DATA_COUNTRIES)
        countries = {}
        for _, row in df_countries.iterrows():
            countries[row["code"]] = row["country"]
        df_men = df_men.rename(columns={"country_code_1": "code_1", "country_code_2": "code_2"})
        df_women = df_women.rename(columns={"country_1": "code_1", "country_2": "code_2"})
        df = pd.concat([df_men, df_women], ignore_index=True)
        df_out = pd.DataFrame({
            "date":     df["date"],
            "equipe_1": df["code_1"].map(countries).fillna(df["code_1"]),
            "equipe_2": df["code_2"].map(countries).fillna(df["code_2"]),
            "score_1":  df["set_country_1"],
            "score_2":  df["set_country_2"],
            "sport":    "volley",
            "stage":    df["stage"],
        })
        return [Match(**r) for r in df_out.to_dict("records")]


MatchLoader.register("volley", VolleyMatchLoader)
