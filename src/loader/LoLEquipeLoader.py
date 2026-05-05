import pandas as pd
from src.Model.Equipe import Equipe
from src.loader.EquipeMenuLoader import EquipeMenuLoader


class LoLEquipeLoader:
    """Affiche les statistiques d'une équipe de League of Legends."""

    DATA_MATCHES = "data/LOL/match.csv"
    DATA_TEAMS   = "data/LOL/team.csv"

    def run(self) -> None:
        """Charge les données et affiche les stats pour une équipe LoL."""
        df      = pd.read_csv(self.DATA_MATCHES)
        df_team = pd.read_csv(self.DATA_TEAMS)
        teams_info = dict(zip(df_team["team_abbreviation"], df_team["team"]))

        nom = input("Nom ou abréviation de l'équipe : ").strip()
        equipes_trouvees = {abrev: tname for abrev, tname in teams_info.items()
                            if nom.lower() in tname.lower() or nom.lower() in abrev.lower()}
        if not equipes_trouvees:
            print("Aucune équipe trouvée.")
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
                        e.victoires += 1
                        e.points    += 1
                    else:
                        e.defaites  += 1

        from src.loader.ResultatManager import ResultatManager
        nb = ResultatManager.appliquer_a_equipe(e, e.nom, nul_possible=False)
        if nb:
            print(f"\n  (+ {nb} nouveau(x) résultat(s) inclus)")

        mj = e.matchs_joues
        print(f"\n=== {e.nom} ({e.abreviation}) ===\n")
        print(f"  Matchs joués : {mj}")
        print(f"  Victoires    : {e.victoires}  Défaites : {e.defaites}  ({e.winrate:.1f}% winrate)")
        print(f"  Kills totaux : {e.kills}  (moy: {e.kills/mj:.1f}/match)")
        print(f"  Dragons      : {e.dragons}  (moy: {e.dragons/mj:.1f}/match)")
        print(f"  Barons       : {e.barons}  (moy: {e.barons/mj:.1f}/match)")
        print(f"  Gold total   : {e.gold:.0f}  (moy: {e.gold/mj:.0f}/match)")


EquipeMenuLoader.register("LOL", LoLEquipeLoader)
