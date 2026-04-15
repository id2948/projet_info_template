import pandas as pd
from src.Model.Joueur import Joueur
from src.loader.JoueurLoader import JoueurLoader


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


JoueurLoader.register("tennis", TennisJoueurLoader)