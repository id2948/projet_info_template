"""Visualiseur de classements sportifs sous forme de tableaux matplotlib."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os

from src.Model.Competition import Competition
from src.Model.Equipe import Equipe


# ── Palette ──────────────────────────────────────────────────────────────────

_HEADER_BG   = "#1a1a2e"
_HEADER_FG   = "#ffffff"
_ROW_ODD     = "#f8f9fa"
_ROW_EVEN    = "#ffffff"
_ZONE_TOP    = "#d4edda"   # vert clair — podium / qualification
_ZONE_MID    = "#fff3cd"   # jaune — barrage
_ZONE_BOT    = "#f8d7da"   # rouge clair — relégation
_BORDER      = "#dee2e6"
_TITLE_COLOR = "#1a1a2e"


def _fig_classement(
    titre: str,
    colonnes: list[str],
    lignes: list[list],
    zones: dict[str, list[int]] | None = None,
    largeurs: list[float] | None = None,
    legende: list[tuple[str, str]] | None = None,
    save_path: str | None = None,
) -> str:
    """Génère et enregistre un tableau de classement stylisé.

    Parameters
    ----------
    titre : str
        Titre affiché en haut de la figure.
    colonnes : list[str]
        En-têtes des colonnes.
    lignes : list[list]
        Données, une liste par ligne.
    zones : dict, optional
        Mapping couleur → liste d'indices de lignes (0-based).
    largeurs : list[float], optional
        Largeurs relatives des colonnes (doit sommer à 1).
    legende : list[tuple[str, str]], optional
        Paires (couleur, label) pour la légende des zones.
    save_path : str, optional
        Chemin de sortie. Généré automatiquement si None.

    Returns
    -------
    str
        Chemin vers l'image sauvegardée.
    """
    n_rows = len(lignes)
    n_cols = len(colonnes)

    row_h = 0.45
    fig_h = max(4.0, 1.5 + n_rows * row_h + (0.6 if legende else 0))
    fig_w = max(10.0, n_cols * 1.4)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.set_title(titre, fontsize=15, fontweight="bold",
                 color=_TITLE_COLOR, pad=14, loc="center")

    col_w = largeurs if largeurs else [1 / n_cols] * n_cols
    total_w = sum(col_w)
    col_w = [w / total_w for w in col_w]

    cell_colors = []
    for i in range(n_rows):
        base = _ROW_ODD if i % 2 == 0 else _ROW_EVEN
        row_colors = []
        for _ in range(n_cols):
            color = base
            if zones:
                for zone_color, indices in zones.items():
                    if i in indices:
                        color = zone_color
            row_colors.append(color)
        cell_colors.append(row_colors)

    header_colors = [[_HEADER_BG] * n_cols]
    all_cell_text  = [colonnes] + lignes
    all_cell_color = header_colors + cell_colors

    tbl = ax.table(
        cellText=all_cell_text,
        cellColours=all_cell_color,
        cellLoc="center",
        loc="upper center",
        bbox=[0, 0 if not legende else 0.06, 1, 0.96],
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)

    for (row_idx, col_idx), cell in tbl.get_celld().items():
        cell.set_linewidth(0.4)
        cell.set_edgecolor(_BORDER)
        if row_idx == 0:
            cell.set_text_props(color=_HEADER_FG, fontweight="bold", fontsize=9)
            cell.set_height(0.06)
        else:
            cell.set_height(row_h / (n_rows + 1))

        if col_idx == 0:
            cell.set_width(col_w[0])
        elif col_idx < len(col_w):
            cell.set_width(col_w[col_idx])

    if legende:
        handles = [mpatches.Patch(facecolor=c, edgecolor=_BORDER, label=l) for c, l in legende]
        ax.legend(handles=handles, loc="lower center", ncol=len(legende),
                  fontsize=8, frameon=True, edgecolor=_BORDER,
                  bbox_to_anchor=(0.5, 0.0))

    plt.tight_layout(pad=0.4)

    if save_path is None:
        os.makedirs("output", exist_ok=True)
        safe = titre.replace("/", "-").replace(" ", "_").replace("—", "-")[:60]
        save_path = f"output/classement_{safe}.png"

    plt.savefig(save_path, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return save_path


# ── Football ──────────────────────────────────────────────────────────────────

def visualiser_football(
    league_id: int | None = None,
    saison: str | None = None,
    save_path: str | None = None,
) -> str:
    """Classement football style Ligue 1.

    Parameters
    ----------
    league_id : int | None
        ID de la ligue (None = toutes).
    saison : str | None
        Saison (ex : "2014/2015"). None = toutes.
    save_path : str | None
        Chemin de sortie.
    """
    df_match  = pd.read_csv("data/football/match.csv")
    df_team   = pd.read_csv("data/football/team.csv")
    df_league = pd.read_csv("data/football/league.csv")
    df_country = pd.read_csv("data/football/country.csv")

    teams   = {r["team_api_id"]: r["team_long_name"]  for _, r in df_team.iterrows()}
    abbrevs = {r["team_api_id"]: r["team_short_name"] for _, r in df_team.iterrows()}
    leagues  = {r["id"]: r["name"] for _, r in df_league.iterrows()}

    df = df_match.copy()
    if league_id:
        df = df[df["league_id"] == league_id]
    if saison:
        df = df[df["season"] == saison]

    if df.empty:
        raise ValueError("Aucun match trouvé pour ces critères.")

    nom_ligue = leagues.get(league_id, "Toutes ligues") if league_id else "Toutes ligues"
    nom_comp  = f"{nom_ligue} — {saison}" if saison else nom_ligue

    comp = Competition(nom_comp, "football")
    for _, row in df.iterrows():
        hid, aid = int(row["home_team_api_id"]), int(row["away_team_api_id"])
        hg,  ag  = int(row["home_team_goal"]),   int(row["away_team_goal"])
        for tid in [hid, aid]:
            if str(tid) not in comp.equipes:
                comp.ajouter_equipe(str(tid), Equipe(teams.get(tid, str(tid)), "football", abbrevs.get(tid)))
        comp.equipes[str(hid)].ajouter_match(hg, ag)
        comp.equipes[str(aid)].ajouter_match(ag, hg)

    _appliquer_nouveaux(comp, nul_possible=True)
    cl = comp.classement_par("points")

    n = len(cl)
    zones = {}
    if n >= 3:
        zones[_ZONE_TOP] = list(range(min(3, n)))
    if n >= 4:
        zones[_ZONE_MID] = [n - 4, n - 3] if n >= 6 else []
        zones[_ZONE_BOT] = [n - 2, n - 1] if n >= 4 else []

    colonnes = ["#", "Équipe", "MJ", "V", "N", "D", "BP", "BC", "DB", "Pts"]
    largeurs = [0.04, 0.22, 0.06, 0.06, 0.06, 0.06, 0.07, 0.07, 0.08, 0.07]
    lignes = []
    for i, e in enumerate(cl, 1):
        lignes.append([
            str(i), e.nom,
            str(e.matchs_joues), str(e.victoires), str(e.nuls), str(e.defaites),
            str(int(e.score_pour)), str(int(e.score_contre)),
            f"{e.difference_score:+.0f}", str(e.points),
        ])

    legende = [
        (_ZONE_TOP, "Qualification européenne"),
        (_ZONE_MID, "Barrage"),
        (_ZONE_BOT, "Relégation"),
    ]

    return _fig_classement(nom_comp, colonnes, lignes, zones, largeurs, legende, save_path)


# ── Basketball ────────────────────────────────────────────────────────────────

def visualiser_basketball(season_type: str = "Regular Season", save_path: str | None = None) -> str:
    """Classement NBA par victoires avec stats avancées.

    Parameters
    ----------
    season_type : str
        Type de saison ("Regular Season", "Playoffs", …).
    save_path : str | None
        Chemin de sortie.
    """
    df_game = pd.read_csv("data/basketball/game.csv")
    df_team = pd.read_csv("data/basketball/team.csv")

    teams   = {r["id"]: r["full_name"]    for _, r in df_team.iterrows()}
    abbrevs = {r["id"]: r["abbreviation"] for _, r in df_team.iterrows()}

    df = df_game[df_game["season_type"] == season_type]
    if df.empty:
        raise ValueError(f"Aucun match pour le type de saison '{season_type}'.")

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
        eh.rebonds += float(row.get("reb_home") or 0)
        eh.passes  += float(row.get("ast_home") or 0)
        ea.rebonds += float(row.get("reb_away") or 0)
        ea.passes  += float(row.get("ast_away") or 0)

    _appliquer_nouveaux(comp, nul_possible=False)
    cl = comp.classement_par("victoires")
    n = len(cl)

    zones = {}
    if n >= 8:
        zones[_ZONE_TOP] = list(range(8))      # 8 qualifiés playoffs (simulation)
    if n >= 10:
        zones[_ZONE_MID] = list(range(8, 10))  # play-in

    colonnes = ["#", "Équipe", "Abrév.", "MJ", "V", "D", "Pts+", "Pts-", "Diff", "Reb/m", "Ast/m", "Win%"]
    largeurs = [0.03, 0.18, 0.07, 0.05, 0.05, 0.05, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07]
    lignes = []
    for i, e in enumerate(cl, 1):
        mj = e.matchs_joues or 1
        lignes.append([
            str(i), e.nom, e.abreviation or "",
            str(e.matchs_joues), str(e.victoires), str(e.defaites),
            str(int(e.score_pour)), str(int(e.score_contre)),
            f"{e.difference_score:+.0f}",
            f"{e.rebonds / mj:.1f}", f"{e.passes / mj:.1f}",
            f"{e.winrate:.1f}%",
        ])

    legende = [
        (_ZONE_TOP, "Qualifié Playoffs"),
        (_ZONE_MID, "Play-in"),
    ]

    return _fig_classement(comp.nom, colonnes, lignes, zones, largeurs, legende, save_path)


# ── League of Legends ─────────────────────────────────────────────────────────

def visualiser_lol(save_path: str | None = None) -> str:
    """Classement LoL EMEA avec stats d'objectifs.

    Parameters
    ----------
    save_path : str | None
        Chemin de sortie.
    """
    df       = pd.read_csv("data/LOL/match.csv")
    df_team  = pd.read_csv("data/LOL/team.csv")

    teams_info = {r["team_abbreviation"]: r["team"] for _, r in df_team.iterrows()}

    comp = Competition("LoL EMEA 2025", "LOL")
    for _, row in df.iterrows():
        for side, opp in [("blue", "red"), ("red", "blue")]:
            abrev = str(row[f"team_{side}"])
            if abrev not in comp.equipes:
                comp.ajouter_equipe(abrev, Equipe(teams_info.get(abrev, abrev), "LOL", abrev))
            e = comp.equipes[abrev]
            e.matchs_joues += 1
            e.kills   += int(row.get(f"kills_team_{side}")  or 0)
            e.dragons += int(row.get(f"dragons_team_{side}") or 0)
            e.barons  += int(row.get(f"barons_team_{side}")  or 0)
            e.gold    += float(row.get(f"gold_team_{side}")  or 0)
            e.score_pour    += int(row.get(f"kills_team_{side}") or 0)
            e.score_contre  += int(row.get(f"kills_team_{opp}")  or 0)
            if str(row["winner"]) == abrev:
                e.victoires += 1
                e.points    += 1
            else:
                e.defaites += 1

    _appliquer_nouveaux(comp, nul_possible=False)
    cl = comp.classement_par("victoires")
    n = len(cl)

    zones = {}
    if n >= 4:
        zones[_ZONE_TOP] = list(range(min(4, n)))
    if n >= 2:
        zones[_ZONE_BOT] = [n - 1, n - 2] if n >= 4 else [n - 1]

    colonnes = ["#", "Équipe", "Abrév.", "MJ", "V", "D", "Win%", "Kills/m", "Dragons/m", "Barons/m", "Gold/m"]
    largeurs = [0.04, 0.18, 0.07, 0.05, 0.05, 0.05, 0.07, 0.08, 0.10, 0.09, 0.09]
    lignes = []
    for i, e in enumerate(cl, 1):
        mj = e.matchs_joues or 1
        lignes.append([
            str(i), e.nom, e.abreviation or "",
            str(e.matchs_joues), str(e.victoires), str(e.defaites),
            f"{e.winrate:.1f}%",
            f"{e.kills / mj:.1f}",
            f"{e.dragons / mj:.1f}",
            f"{e.barons / mj:.1f}",
            f"{e.gold / mj:.0f}",
        ])

    legende = [
        (_ZONE_TOP, "Playoffs"),
        (_ZONE_BOT, "Relégation"),
    ]

    return _fig_classement(comp.nom, colonnes, lignes, zones, largeurs, legende, save_path)


# ── Tennis ────────────────────────────────────────────────────────────────────

def visualiser_tennis(circuit: str = "ATP", tournoi: str | None = None, save_path: str | None = None) -> str:
    """Classement tennis par victoires.

    Parameters
    ----------
    circuit : str
        "ATP" ou "WTA".
    tournoi : str | None
        Nom exact d'un tournoi. None = tous les tournois.
    save_path : str | None
        Chemin de sortie.
    """
    circuit = circuit.upper()
    if circuit == "ATP":
        df_m = pd.read_csv("data/tennis/atp_matches_2024.csv")
        df_p = pd.read_csv("data/tennis/atp_players_2024.csv")
    elif circuit == "WTA":
        df_m = pd.read_csv("data/tennis/wta_matches_2024.csv")
        df_p = pd.read_csv("data/tennis/wta_players_2024.csv")
    else:
        raise ValueError(f"Circuit inconnu : {circuit}")

    players = {str(int(r["player_id"])): r["name_first"] + " " + r["name_last"]
               for _, r in df_p.iterrows()}

    nom_comp = f"{circuit} 2024"
    if tournoi:
        df_m = df_m[df_m["tourney_name"] == tournoi]
        nom_comp = tournoi
        if df_m.empty:
            raise ValueError(f"Tournoi '{tournoi}' introuvable.")

    comp = Competition(nom_comp, "tennis")
    for _, row in df_m.iterrows():
        wid = str(int(row["winner_id"]))
        lid = str(int(row["loser_id"]))
        for pid in [wid, lid]:
            if pid not in comp.equipes:
                comp.ajouter_equipe(pid, Equipe(players.get(pid, pid), "tennis"))
        comp.equipes[wid].ajouter_match(1, 0, nul_possible=False)
        comp.equipes[lid].ajouter_match(0, 1, nul_possible=False)

    _appliquer_nouveaux(comp, nul_possible=False)
    cl = comp.classement_par("victoires")[:30]
    n = len(cl)

    zones = {}
    if n >= 3:
        zones[_ZONE_TOP] = list(range(min(3, n)))

    colonnes = ["#", "Joueur", "MJ", "V", "D", "Win%"]
    largeurs = [0.05, 0.40, 0.10, 0.10, 0.10, 0.12]
    lignes = []
    for i, e in enumerate(cl, 1):
        lignes.append([
            str(i), e.nom,
            str(e.matchs_joues), str(e.victoires), str(e.defaites),
            f"{e.winrate:.1f}%",
        ])

    legende = [(_ZONE_TOP, "Top 3")]
    return _fig_classement(nom_comp, colonnes, lignes, zones, largeurs, legende, save_path)


# ── Volleyball ────────────────────────────────────────────────────────────────

def visualiser_volley(genre: str = "Hommes", save_path: str | None = None) -> str:
    """Classement volleyball JO 2024.

    Parameters
    ----------
    genre : str
        "Hommes" ou "Femmes".
    save_path : str | None
        Chemin de sortie.
    """
    df_countries = pd.read_csv("data/volley/country.csv")
    countries = {r["code"]: r["country"] for _, r in df_countries.iterrows()}

    is_men = genre.lower() in ("hommes", "h", "men", "m")
    if is_men:
        df = pd.read_csv("data/volley/match_men.csv")
        df["code_1"] = df["country_code_1"]
        df["code_2"] = df["country_code_2"]
        nom_comp = "Volleyball Hommes — JO 2024"
    else:
        df = pd.read_csv("data/volley/match_women.csv")
        df["code_1"] = df["country_1"]
        df["code_2"] = df["country_2"]
        nom_comp = "Volleyball Femmes — JO 2024"

    comp = Competition(nom_comp, "volley")
    for _, row in df.iterrows():
        c1, c2 = str(row["code_1"]), str(row["code_2"])
        s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
        for code in [c1, c2]:
            if code not in comp.equipes:
                comp.ajouter_equipe(code, Equipe(countries.get(code, code), "volley", code))
        comp.equipes[c1].ajouter_match(s1, s2, nul_possible=False)
        comp.equipes[c2].ajouter_match(s2, s1, nul_possible=False)

    _appliquer_nouveaux(comp, nul_possible=False)
    cl = comp.classement_par("victoires")
    n = len(cl)

    zones = {}
    if n >= 4:
        zones[_ZONE_TOP] = list(range(min(4, n)))
    if n >= 2:
        zones[_ZONE_BOT] = [n - 1]

    colonnes = ["#", "Pays", "Abrév.", "MJ", "V", "D", "Sets+", "Sets-", "Diff", "Win%"]
    largeurs = [0.04, 0.22, 0.07, 0.06, 0.06, 0.06, 0.08, 0.08, 0.08, 0.08]
    lignes = []
    for i, e in enumerate(cl, 1):
        lignes.append([
            str(i), e.nom, e.abreviation or "",
            str(e.matchs_joues), str(e.victoires), str(e.defaites),
            str(int(e.score_pour)), str(int(e.score_contre)),
            f"{e.difference_score:+.0f}", f"{e.winrate:.1f}%",
        ])

    legende = [
        (_ZONE_TOP, "Demi-finales"),
        (_ZONE_BOT, "Dernière place"),
    ]
    return _fig_classement(nom_comp, colonnes, lignes, zones, largeurs, legende, save_path)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _appliquer_nouveaux(comp: Competition, nul_possible: bool) -> None:
    from src.loader.GestionResultats import GestionResultats
    GestionResultats.appliquer_a_competition(comp, nul_possible=nul_possible)


# ── Menu interactif ───────────────────────────────────────────────────────────

def run_menu(sport_nom: str) -> None:
    """Point d'entrée du visualiseur pour un sport donné.

    Parameters
    ----------
    sport_nom : str
        Nom du sport (clé de SPORTS_DISPONIBLES dans __main__).
    """
    os.makedirs("output", exist_ok=True)

    if sport_nom == "football":
        _menu_football()
    elif sport_nom == "basketball":
        _menu_basketball()
    elif sport_nom == "LOL":
        _menu_lol()
    elif sport_nom == "tennis":
        _menu_tennis()
    elif sport_nom == "volley":
        _menu_volley()
    else:
        print(f"  Pas de visualiseur disponible pour '{sport_nom}'.")


def _menu_football() -> None:
    df_match  = pd.read_csv("data/football/match.csv")
    df_league = pd.read_csv("data/football/league.csv")
    df_country = pd.read_csv("data/football/country.csv")

    leagues  = {r["id"]: r["name"] for _, r in df_league.iterrows()}
    lg_ctry  = {r["id"]: r["country_id"] for _, r in df_league.iterrows()}
    countries = {r["id"]: r["name"] for _, r in df_country.iterrows()}

    print("\n  Ligues disponibles :")
    for lid, lname in leagues.items():
        print(f"    {lid} - {lname} ({countries.get(lg_ctry.get(lid), '?')})")
    try:
        lid_in = input("  ID de la ligue (0 = toutes) : ").strip()
        lid = int(lid_in) or None
    except ValueError:
        lid = None

    saisons = sorted(df_match["season"].unique())
    print("  Saisons :", ", ".join(saisons))
    saison = input("  Saison (ex: 2014/2015, vide = toutes) : ").strip() or None

    path = visualiser_football(league_id=lid, saison=saison)
    print(f"\n  Classement généré : {path}")


def _menu_basketball() -> None:
    df = pd.read_csv("data/basketball/game.csv")
    types = sorted(df["season_type"].unique())
    print("\n  Types de saison :", ", ".join(types))
    st = input("  Type de saison : ").strip()
    if st not in types:
        print("  Type invalide.")
        return
    path = visualiser_basketball(season_type=st)
    print(f"\n  Classement généré : {path}")


def _menu_lol() -> None:
    path = visualiser_lol()
    print(f"\n  Classement généré : {path}")


def _menu_tennis() -> None:
    circuit = input("\n  Circuit (ATP / WTA) : ").strip().upper()
    if circuit not in ("ATP", "WTA"):
        print("  Circuit invalide.")
        return

    if circuit == "ATP":
        df_m = pd.read_csv("data/tennis/atp_matches_2024.csv")
    else:
        df_m = pd.read_csv("data/tennis/wta_matches_2024.csv")

    tournois = list(df_m["tourney_name"].unique())
    print("\n  Tournois disponibles :")
    for i, t in enumerate(tournois[:25], 1):
        print(f"    {i}. {t}")
    print("    0. Tous les tournois")
    try:
        idx = int(input("  Numéro (0 = tous) : ").strip())
        tournoi = tournois[idx - 1] if idx > 0 else None
    except (ValueError, IndexError):
        tournoi = None

    path = visualiser_tennis(circuit=circuit, tournoi=tournoi)
    print(f"\n  Classement généré : {path}")


def _menu_volley() -> None:
    genre = input("\n  Catégorie (Hommes / Femmes) : ").strip()
    path = visualiser_volley(genre=genre)
    print(f"\n  Classement généré : {path}")
