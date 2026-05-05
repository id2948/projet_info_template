from typing import Optional

import pandas as pd

from src.Model.Competition import Competition
from src.Model.Equipe import Equipe
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader


class FootballCompetitionLoader:
    """Affiche les classements de football par ligue et par saison."""

    DATA_MATCHES = "data/football/match.csv"
    DATA_TEAMS   = "data/football/team.csv"
    DATA_LEAGUES = "data/football/league.csv"
    DATA_COUNTRY = "data/football/country.csv"

    def run(self) -> None:
        """Affiche le menu de classement football et exécute le choix."""
        df_match   = pd.read_csv(self.DATA_MATCHES)
        df_team    = pd.read_csv(self.DATA_TEAMS)
        df_league  = pd.read_csv(self.DATA_LEAGUES)
        df_country = pd.read_csv(self.DATA_COUNTRY)

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

        lid    = self._choisir_ligue(leagues, countries, lg_ctry)
        if lid is None:
            return
        saison = self._choisir_saison(df_match) if choix in ["1", "2", "3"] else None

        df = df_match.copy()
        if lid:    df = df[df["league_id"] == lid]
        if saison: df = df[df["season"] == saison]
        if df.empty:
            print("Aucun match trouvé.")
            return

        comp = self._construire(df, teams, abbrevs, leagues.get(lid, str(lid)))

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_competition(comp, nul_possible=True)
        if nb:
            print(f"  (+ {nb} nouveau(x) résultat(s) inclus dans le classement)")

        if choix == "1":
            cl = comp.classement_par("points", "difference_score", "score_pour")
            self._afficher_classement(cl, f"{comp.nom} — {saison}")
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
            comp_all = self._construire(df_match, teams, abbrevs, "Toutes ligues — Toutes saisons")
            cl = comp_all.classement_par("points", "difference_score")
            self._afficher_classement(cl[:30], comp_all.nom)

    def _construire(self, df, teams: dict, abbrevs: dict, nom_comp: str) -> Competition:
        """Construit une Competition football depuis un DataFrame de matchs.

        Parameters
        ----------
        df : pd.DataFrame
            Matchs à traiter.
        teams : dict
            Correspondance identifiant → nom d'équipe.
        abbrevs : dict
            Correspondance identifiant → abréviation.
        nom_comp : str
            Nom de la compétition.

        Returns
        -------
        Competition
            Compétition avec toutes les équipes et leurs stats calculées.
        """
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

    def _choisir_ligue(self, leagues: dict, countries: dict, lg_ctry: dict) -> Optional[int]:
        """Invite l'utilisateur à choisir une ligue.

        Returns
        -------
        int | None
            Identifiant de la ligue, ou None si toutes.
        """
        print("\nLigues disponibles :")
        for lid, lname in leagues.items():
            print(f"  {lid} - {lname} ({countries.get(lg_ctry.get(lid), '?')})")
        try:
            return int(input("ID de la ligue (0 = toutes) : ").strip()) or None
        except ValueError:
            return None

    def _choisir_saison(self, df_match) -> Optional[str]:
        """Invite l'utilisateur à choisir une saison.

        Returns
        -------
        str | None
            Saison choisie, ou None si non trouvée.
        """
        saisons = sorted(df_match["season"].unique())
        print("\nSaisons :", ", ".join(saisons))
        saison = input("Saison (ex: 2014/2015) : ").strip()
        return saison if saison in saisons else None

    def _afficher_classement(self, classement: list, titre: str) -> None:
        """Affiche un classement au format football (MJ/V/N/D/BP/BC/DB/Pts).

        Parameters
        ----------
        classement : list
            Équipes triées.
        titre : str
            Titre du tableau.
        """
        print(f"\n=== {titre} ===\n")
        print(f"{'#':<4}{'Équipe':<30}{'MJ':>4}{'V':>4}{'N':>4}{'D':>4}{'BP':>5}{'BC':>5}{'DB':>6}{'Pts':>5}")
        print("-" * 72)
        for i, e in enumerate(classement, 1):
            print(f"{i:<4}{e.nom:<30}{e.matchs_joues:>4}{e.victoires:>4}{e.nuls:>4}"
                  f"{e.defaites:>4}{e.score_pour:>5.0f}{e.score_contre:>5.0f}"
                  f"{e.difference_score:>+6.0f}{e.points:>5}")


CompetitionMenuLoader.register("football", FootballCompetitionLoader)
