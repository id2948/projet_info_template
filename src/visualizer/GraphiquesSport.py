
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import os

os.makedirs("output", exist_ok=True)

# ── Style commun ──────────────────────────────────────────────────────────────
PALETTE = [
    "#2196F3",
    "#F44336",
    "#4CAF50",
    "#FF9800",
    "#9C27B0",
    "#00BCD4",
    "#FF5722",
    "#607D8B",
    "#E91E63",
    "#8BC34A",
]


def _save(fig, nom: str) -> str:
    safe = nom.replace("/", "-").replace(" ", "_").replace("\\", "-")
    path = f"output/{safe}.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def _style(ax, titre: str, xlabel: str = "", ylabel: str = "") -> None:
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")


# ══════════════════════════════════════════════════════════════════════════════
# FOOTBALL
# ══════════════════════════════════════════════════════════════════════════════


def _charger_football(league_id: int | None = None, saison: str | None = None):
    df = pd.read_csv("data/football/match.csv")
    df_team = pd.read_csv("data/football/team.csv")
    df_league = pd.read_csv("data/football/league.csv")
    teams = {r["team_api_id"]: r["team_long_name"] for _, r in df_team.iterrows()}
    leagues = {r["id"]: r["name"] for _, r in df_league.iterrows()}
    if league_id:
        df = df[df["league_id"] == league_id]
    if saison:
        df = df[df["season"] == saison]
    return df, teams, leagues


def graph_foot_buts_journee(
    league_id: int | None = None, saison: str | None = None
) -> str:
    """Évolution des buts moyens par journée (stage) sur une saison."""
    df, _, leagues = _charger_football(league_id, saison)
    if df.empty:
        raise ValueError("Aucun match trouvé.")
    df["total_buts"] = df["home_team_goal"] + df["away_team_goal"]
    par_journee = df.groupby("stage")["total_buts"].mean().reset_index()
    par_journee = par_journee.sort_values("stage")

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(
        par_journee["stage"],
        par_journee["total_buts"],
        marker="o",
        color=PALETTE[0],
        linewidth=2,
        markersize=5,
    )
    ax.fill_between(
        par_journee["stage"], par_journee["total_buts"], alpha=0.15, color=PALETTE[0]
    )
    nom = leagues.get(league_id, "Toutes ligues") if league_id else "Toutes ligues"
    titre = f"Buts moyens par journée — {nom}" + (f" {saison}" if saison else "")
    _style(ax, titre, "Journée", "Buts moyens / match")
    ax.set_xticks(par_journee["stage"])
    ax.tick_params(axis="x", rotation=45)
    return _save(fig, f"foot_buts_journee_{league_id or 'all'}_{saison or 'all'}")


def graph_foot_dist_scores(
    league_id: int | None = None, saison: str | None = None
) -> str:
    """Histogramme de la distribution des buts par équipe par match."""
    df, _, leagues = _charger_football(league_id, saison)
    scores = pd.concat([df["home_team_goal"], df["away_team_goal"]])

    fig, ax = plt.subplots(figsize=(9, 5))
    max_s = int(scores.max()) + 1
    ax.hist(
        scores,
        bins=range(max_s + 1),
        color=PALETTE[0],
        edgecolor="white",
        rwidth=0.8,
        align="left",
    )
    nom = leagues.get(league_id, "Toutes ligues") if league_id else "Toutes ligues"
    _style(
        ax,
        f"Distribution des buts par équipe — {nom}",
        "Buts marqués",
        "Nombre de matchs",
    )
    ax.set_xticks(range(max_s))
    return _save(fig, f"foot_dist_scores_{league_id or 'all'}_{saison or 'all'}")


def graph_foot_attaque_defense(
    league_id: int | None = None, saison: str | None = None
) -> str:
    """Scatter buts pour vs buts contre — taille de bulle = matchs joués."""
    df, teams, leagues = _charger_football(league_id, saison)

    stats: dict = {}
    for _, row in df.iterrows():
        hid, aid = int(row["home_team_api_id"]), int(row["away_team_api_id"])
        hg, ag = int(row["home_team_goal"]), int(row["away_team_goal"])
        for tid, g_for, g_ag in [(hid, hg, ag), (aid, ag, hg)]:
            if tid not in stats:
                stats[tid] = [0, 0, 0]
            stats[tid][0] += g_for
            stats[tid][1] += g_ag
            stats[tid][2] += 1

    noms = [teams.get(t, str(t)) for t in stats]
    pour = [v[0] for v in stats.values()]
    contr = [v[1] for v in stats.values()]
    mj = [v[2] for v in stats.values()]

    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(
        pour,
        contr,
        s=[m * 2 for m in mj],
        c=PALETTE[0],
        alpha=0.55,
        edgecolors="white",
        linewidth=0.5,
    )
    lim = max(max(pour), max(contr)) * 1.05
    ax.plot(
        [0, lim], [0, lim], color="gray", linestyle="--", alpha=0.5, label="Équilibre"
    )
    nom = leagues.get(league_id, "Toutes ligues") if league_id else "Toutes ligues"
    _style(ax, f"Attaque vs Défense — {nom}", "Buts marqués", "Buts encaissés")
    ax.legend(fontsize=9)
    # Labels top 5 attaque
    idx_top = sorted(range(len(pour)), key=lambda i: pour[i], reverse=True)[:5]
    for i in idx_top:
        ax.annotate(
            noms[i],
            (pour[i], contr[i]),
            fontsize=7,
            ha="center",
            xytext=(0, 7),
            textcoords="offset points",
        )
    return _save(fig, f"foot_attaque_defense_{league_id or 'all'}_{saison or 'all'}")


# ══════════════════════════════════════════════════════════════════════════════
# BASKETBALL
# ══════════════════════════════════════════════════════════════════════════════


def _charger_basketball(season_type: str = "Regular Season"):
    df_game = pd.read_csv("data/basketball/game.csv")
    df_team = pd.read_csv("data/basketball/team.csv")
    teams = {r["id"]: r["full_name"] for _, r in df_team.iterrows()}
    abbrevs = {r["id"]: r["abbreviation"] for _, r in df_team.iterrows()}
    df = df_game[df_game["season_type"] == season_type]
    return df, teams, abbrevs


def graph_basket_dist_scores(season_type: str = "Regular Season") -> str:
    """Histogramme de la distribution des points marqués par équipe par match."""
    df, _, _ = _charger_basketball(season_type)
    scores = pd.concat([df["pts_home"], df["pts_away"]])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(scores, bins=30, color=PALETTE[1], edgecolor="white")
    _style(
        ax,
        f"Distribution des points — NBA {season_type}",
        "Points par match",
        "Fréquence",
    )
    mean_s = scores.mean()
    ax.axvline(
        mean_s,
        color="black",
        linestyle="--",
        alpha=0.7,
        label=f"Moyenne : {mean_s:.1f}",
    )
    ax.legend(fontsize=9)
    return _save(fig, f"basket_dist_scores_{season_type.replace(' ', '_')}")


def graph_basket_pts_marqués_encaissés(season_type: str = "Regular Season") -> str:
    """Scatter points marqués vs points encaissés par équipe."""
    df, teams, abbrevs = _charger_basketball(season_type)

    stats: dict = {}
    for _, row in df.iterrows():
        for hid, apts, bpts in [
            (int(row["team_id_home"]), int(row["pts_home"]), int(row["pts_away"])),
            (int(row["team_id_away"]), int(row["pts_away"]), int(row["pts_home"])),
        ]:
            if hid not in stats:
                stats[hid] = [0, 0, 0]
            stats[hid][0] += apts
            stats[hid][1] += bpts
            stats[hid][2] += 1

    pour = [v[0] / v[2] for v in stats.values()]
    contr = [v[1] / v[2] for v in stats.values()]
    noms = [abbrevs.get(t, str(t)) for t in stats]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(pour, contr, s=80, color=PALETTE[1], alpha=0.7, edgecolors="white")
    lim = [min(pour + contr) - 2, max(pour + contr) + 2]
    ax.plot(lim, lim, color="gray", linestyle="--", alpha=0.5, label="Équilibre")
    for i, nom in enumerate(noms):
        ax.annotate(
            nom,
            (pour[i], contr[i]),
            fontsize=7.5,
            xytext=(4, 0),
            textcoords="offset points",
        )
    _style(
        ax,
        f"Points marqués vs encaissés — NBA {season_type}",
        "Pts marqués / match",
        "Pts encaissés / match",
    )
    ax.legend(fontsize=9)
    return _save(fig, f"basket_pts_vs_{season_type.replace(' ', '_')}")


def graph_basket_top_rebondeurs(
    season_type: str = "Regular Season", top_n: int = 15
) -> str:
    """Top N équipes au rebond — moyenne par match."""
    df, teams, _ = _charger_basketball(season_type)

    reb: dict = {}
    mj: dict = {}
    for _, row in df.iterrows():
        for tid, col in [
            (int(row["team_id_home"]), "reb_home"),
            (int(row["team_id_away"]), "reb_away"),
        ]:
            reb[tid] = reb.get(tid, 0) + float(row.get(col) or 0)
            mj[tid] = mj.get(tid, 0) + 1

    data = sorted(
        [(teams.get(t, str(t)), reb[t] / mj[t]) for t in reb],
        key=lambda x: x[1],
        reverse=True,
    )[:top_n]
    noms, vals = zip(*data)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(noms[::-1], vals[::-1], color=PALETTE[1], edgecolor="white")
    _style(
        ax, f"Top {top_n} équipes au rebond — NBA {season_type}", "Rebonds / match", ""
    )
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    for bar, val in zip(bars, vals[::-1]):
        ax.text(
            val + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}",
            va="center",
            fontsize=8,
        )
    return _save(fig, f"basket_top_rebonds_{season_type.replace(' ', '_')}")


def graph_basket_evol_scores_saison() -> str:
    """Score moyen par match selon le type de saison (Regular Season vs Playoffs)."""
    df_game = pd.read_csv("data/basketball/game.csv")
    scores = pd.concat([df_game["pts_home"], df_game["pts_away"]])
    df_all = pd.DataFrame({"pts": scores, "type": list(df_game["season_type"]) * 2})
    moy = df_all.groupby("type")["pts"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(
        moy["type"], moy["pts"], color=PALETTE[: len(moy)], edgecolor="white", width=0.5
    )
    _style(ax, "Score moyen par type de saison — NBA", "", "Points / match")
    for i, row in moy.iterrows():
        ax.text(i, row["pts"] + 0.3, f"{row['pts']:.1f}", ha="center", fontsize=10)
    return _save(fig, "basket_evol_scores_saison")


# ══════════════════════════════════════════════════════════════════════════════
# LEAGUE OF LEGENDS
# ══════════════════════════════════════════════════════════════════════════════


def _charger_lol():
    df = pd.read_csv("data/LOL/match.csv")
    df_team = pd.read_csv("data/LOL/team.csv")
    df_player = pd.read_csv("data/LOL/player.csv")
    teams_info = {r["team_abbreviation"]: r["team"] for _, r in df_team.iterrows()}
    return df, teams_info, df_player


def graph_lol_barres_groupees() -> str:
    """Kills, Dragons et Barons moyens par équipe — barres groupées."""
    df, teams_info, _ = _charger_lol()

    stats: dict = {}
    for _, row in df.iterrows():
        for side, opp in [("blue", "red"), ("red", "blue")]:
            abrev = str(row[f"team_{side}"])
            if abrev not in stats:
                stats[abrev] = {"kills": 0, "dragons": 0, "barons": 0, "mj": 0}
            stats[abrev]["kills"] += int(row.get(f"kills_team_{side}") or 0)
            stats[abrev]["dragons"] += int(row.get(f"dragons_team_{side}") or 0)
            stats[abrev]["barons"] += int(row.get(f"barons_team_{side}") or 0)
            stats[abrev]["mj"] += 1

    equipes = list(stats.keys())
    noms = [teams_info.get(e, e) for e in equipes]
    mj_arr = [stats[e]["mj"] or 1 for e in equipes]
    kills = [stats[e]["kills"] / mj_arr[i] for i, e in enumerate(equipes)]
    dragons = [stats[e]["dragons"] / mj_arr[i] for i, e in enumerate(equipes)]
    barons = [stats[e]["barons"] / mj_arr[i] for i, e in enumerate(equipes)]

    x = np.arange(len(noms))
    w = 0.25
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(
        x - w, kills, width=w, label="Kills/match", color=PALETTE[0], edgecolor="white"
    )
    ax.bar(
        x, dragons, width=w, label="Dragons/match", color=PALETTE[2], edgecolor="white"
    )
    ax.bar(
        x + w,
        barons,
        width=w,
        label="Barons/match",
        color=PALETTE[3],
        edgecolor="white",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(noms, rotation=30, ha="right", fontsize=9)
    _style(
        ax, "Kills / Dragons / Barons par équipe — LoL EMEA 2025", "", "Moyenne / match"
    )
    ax.legend(fontsize=9)
    return _save(fig, "lol_barres_groupees")


def graph_lol_gold_winrate() -> str:
    """Scatter : gold moyen par match vs taux de victoire."""
    df, teams_info, _ = _charger_lol()

    stats: dict = {}
    for _, row in df.iterrows():
        for side, opp in [("blue", "red"), ("red", "blue")]:
            abrev = str(row[f"team_{side}"])
            if abrev not in stats:
                stats[abrev] = {"gold": 0, "victoires": 0, "mj": 0}
            stats[abrev]["gold"] += float(row.get(f"gold_team_{side}") or 0)
            stats[abrev]["victoires"] += 1 if str(row["winner"]) == abrev else 0
            stats[abrev]["mj"] += 1

    noms = [teams_info.get(e, e) for e in stats]
    gold = [stats[e]["gold"] / (stats[e]["mj"] or 1) for e in stats]
    winrate = [stats[e]["victoires"] / (stats[e]["mj"] or 1) * 100 for e in stats]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(gold, winrate, s=100, color=PALETTE[4], alpha=0.8, edgecolors="white")
    for i, nom in enumerate(noms):
        ax.annotate(
            nom,
            (gold[i], winrate[i]),
            fontsize=8,
            xytext=(5, 3),
            textcoords="offset points",
        )
    _style(
        ax, "Gold moyen vs Winrate — LoL EMEA 2025", "Gold moyen / match", "Winrate (%)"
    )
    ax.grid(axis="both", alpha=0.3, linestyle="--")
    return _save(fig, "lol_gold_winrate")


def graph_lol_classement() -> str:
    """Classement général LoL — barres horizontales par victoires."""
    df, teams_info, _ = _charger_lol()

    victoires: dict = {}
    mj: dict = {}
    for _, row in df.iterrows():
        for side in ["blue", "red"]:
            abrev = str(row[f"team_{side}"])
            victoires[abrev] = victoires.get(abrev, 0) + (
                1 if str(row["winner"]) == abrev else 0
            )
            mj[abrev] = mj.get(abrev, 0) + 1

    data = sorted(
        [(teams_info.get(e, e), victoires[e], mj[e]) for e in victoires],
        key=lambda x: x[1],
        reverse=True,
    )
    noms = [d[0] for d in data]
    vals = [d[1] for d in data]
    colors = (
        [PALETTE[2]] * min(4, len(noms))
        + [PALETTE[0]] * max(0, len(noms) - 6)
        + [PALETTE[1]] * 2
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(noms[::-1], vals[::-1], color=colors[::-1], edgecolor="white")
    _style(ax, "Classement LoL EMEA 2025", "Victoires", "")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.1, i, str(v), va="center", fontsize=9)
    return _save(fig, "lol_classement")


# ══════════════════════════════════════════════════════════════════════════════
# TENNIS
# ══════════════════════════════════════════════════════════════════════════════


def _charger_tennis(circuit: str = "ATP"):
    circuit = circuit.upper()
    if circuit == "ATP":
        df_m = pd.read_csv("data/tennis/atp_matches_2024.csv")
        df_p = pd.read_csv("data/tennis/atp_players_2024.csv")
    else:
        df_m = pd.read_csv("data/tennis/wta_matches_2024.csv")
        df_p = pd.read_csv("data/tennis/wta_players_2024.csv")
    players = {
        str(int(r["player_id"])): r["name_first"] + " " + r["name_last"]
        for _, r in df_p.iterrows()
    }
    return df_m, df_p, players


def graph_tennis_top10(circuit: str = "ATP", top_n: int = 10) -> str:
    """Barres horizontales — top N joueurs par victoires."""
    df_m, _, players = _charger_tennis(circuit)

    wins: dict = {}
    for _, row in df_m.iterrows():
        wid = str(int(row["winner_id"]))
        wins[wid] = wins.get(wid, 0) + 1

    data = sorted(wins.items(), key=lambda x: x[1], reverse=True)[:top_n]
    noms = [players.get(k, k) for k, _ in data]
    vals = [v for _, v in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(noms[::-1], vals[::-1], color=PALETTE[5], edgecolor="white")
    _style(ax, f"Top {top_n} joueurs {circuit} 2024 — victoires", "Victoires", "")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    for bar, val in zip(bars, vals[::-1]):
        ax.text(
            val + 0.3,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center",
            fontsize=9,
        )
    return _save(fig, f"tennis_top10_{circuit.lower()}")


def graph_tennis_surface(circuit: str = "ATP") -> str:
    """Camembert — répartition des matchs par surface."""
    df_m, _, _ = _charger_tennis(circuit)
    surfaces = df_m["surface"].fillna("Unknown").value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        surfaces.values,
        labels=surfaces.index,
        autopct="%1.1f%%",
        colors=PALETTE[: len(surfaces)],
        startangle=120,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title(
        f"Répartition des matchs par surface — {circuit} 2024",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    return _save(fig, f"tennis_surface_{circuit.lower()}")


def graph_tennis_atp_wta_taille() -> str:
    """Barres groupées — distribution des tailles ATP vs WTA."""
    df_atp = pd.read_csv("data/tennis/atp_players_2024.csv").dropna(subset=["height"])
    df_wta = pd.read_csv("data/tennis/wta_players_2024.csv").dropna(subset=["height"])

    bins = list(range(155, 215, 5))
    labels = [f"{b}–{b + 5}" for b in bins[:-1]]
    atp_counts = pd.cut(df_atp["height"], bins=bins).value_counts().sort_index().values
    wta_counts = pd.cut(df_wta["height"], bins=bins).value_counts().sort_index().values

    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(
        x - w / 2, atp_counts, width=w, label="ATP", color=PALETTE[0], edgecolor="white"
    )
    ax.bar(
        x + w / 2, wta_counts, width=w, label="WTA", color=PALETTE[3], edgecolor="white"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    _style(
        ax,
        "Distribution des tailles — ATP vs WTA 2024",
        "Taille (cm)",
        "Nombre de joueurs",
    )
    ax.legend(fontsize=10)
    return _save(fig, "tennis_atp_wta_taille")


def graph_tennis_nationalite(circuit: str = "ATP", top_n: int = 6) -> str:
    """Camembert — top N nationalités + Autres."""
    _, df_p, _ = _charger_tennis(circuit)
    nat = df_p["ioc"].fillna("?").value_counts()
    top = nat.head(top_n)
    autres = nat.iloc[top_n:].sum()
    labels = list(top.index) + ["Autres"]
    vals = list(top.values) + [autres]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        vals,
        labels=labels,
        autopct="%1.1f%%",
        colors=PALETTE[: len(vals)],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title(
        f"Répartition par nationalité — {circuit} 2024",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    return _save(fig, f"tennis_nationalite_{circuit.lower()}")


# ══════════════════════════════════════════════════════════════════════════════
# VOLLEYBALL
# ══════════════════════════════════════════════════════════════════════════════


def _charger_volley(genre: str = "Hommes"):
    is_men = genre.lower() in ("hommes", "h", "men")
    df_m = pd.read_csv(
        "data/volley/match_men.csv" if is_men else "data/volley/match_women.csv"
    )
    df_p = pd.read_csv(
        "data/volley/player_men.csv" if is_men else "data/volley/player_women.csv"
    )
    df_country = pd.read_csv("data/volley/country.csv")
    countries = {r["code"]: r["country"] for _, r in df_country.iterrows()}
    if is_men:
        df_m["code_1"], df_m["code_2"] = df_m["country_code_1"], df_m["country_code_2"]
    else:
        df_m["code_1"], df_m["code_2"] = df_m["country_1"], df_m["country_2"]
    return df_m, df_p, countries, is_men


def graph_volley_taille_pays() -> str:
    """Taille moyenne des joueurs par pays — Hommes vs Femmes."""
    df_men, dp_m, countries, _ = _charger_volley("Hommes")
    _, dp_w, _, _ = _charger_volley("Femmes")

    def _moy_taille(df_p):
        df_p = df_p.dropna(subset=["height"])
        df_p["height"] = pd.to_numeric(df_p["height"], errors="coerce")
        return df_p.groupby("country_code")["height"].mean()

    moy_m = _moy_taille(dp_m)
    moy_w = _moy_taille(dp_w)
    codes = sorted(set(list(moy_m.index) + list(moy_w.index)))
    noms = [countries.get(c, c) for c in codes]
    vals_m = [moy_m.get(c, float("nan")) for c in codes]
    vals_w = [moy_w.get(c, float("nan")) for c in codes]

    x = np.arange(len(noms))
    w = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(
        x - w / 2, vals_m, width=w, label="Hommes", color=PALETTE[0], edgecolor="white"
    )
    ax.bar(
        x + w / 2, vals_w, width=w, label="Femmes", color=PALETTE[3], edgecolor="white"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(noms, rotation=35, ha="right", fontsize=8)
    _style(ax, "Taille moyenne par pays — JO 2024", "", "Taille (cm)")
    ax.legend(fontsize=10)
    ax.set_ylim(160, 210)
    return _save(fig, "volley_taille_pays")


def graph_volley_camembert_pays(genre: str = "Hommes") -> str:
    """Répartition géographique des équipes participantes."""
    _, _, countries, is_men = _charger_volley(genre)
    df_m = pd.read_csv(
        "data/volley/match_men.csv" if is_men else "data/volley/match_women.csv"
    )
    col1 = "country_code_1" if is_men else "country_1"
    col2 = "country_code_2" if is_men else "country_2"
    codes = pd.concat([df_m[col1], df_m[col2]]).value_counts()
    labels = [countries.get(c, c) for c in codes.index]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        codes.values,
        labels=labels,
        autopct="%1.1f%%",
        colors=PALETTE[: len(codes)],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title(
        f"Répartition des matchs par pays — Volley {genre} JO 2024",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    return _save(fig, f"volley_camembert_{genre.lower()}")


# ══════════════════════════════════════════════════════════════════════════════
# GRAPHIQUES MULTI-SPORT (Équipe / Compétition)
# ══════════════════════════════════════════════════════════════════════════════


def graph_comparaison_equipes(sport: str, nom1: str, nom2: str) -> str:
    """Barres groupées comparant deux équipes sur leurs stats principales."""
    comps = _construire_competition_generique(sport)
    if comps is None:
        raise ValueError(f"Sport non supporté : {sport}")

    e1 = e2 = None
    for e in comps.equipes.values():
        if nom1.lower() in e.nom.lower():
            e1 = e
        if nom2.lower() in e.nom.lower():
            e2 = e
    if e1 is None or e2 is None:
        raise ValueError(f"Une des équipes introuvable.")

    metrics = ["Points", "Victoires", "Nuls", "Défaites"]
    vals1 = [e1.points, e1.victoires, e1.nuls, e1.defaites]
    vals2 = [e2.points, e2.victoires, e2.nuls, e2.defaites]

    x = np.arange(len(metrics))
    w = 0.35
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - w / 2, vals1, width=w, label=e1.nom, color=PALETTE[0], edgecolor="white")
    ax.bar(x + w / 2, vals2, width=w, label=e2.nom, color=PALETTE[1], edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9)
    _style(ax, f"Comparaison — {e1.nom} vs {e2.nom}", "", "Valeur")
    ax.legend(fontsize=10)
    return _save(fig, f"comparaison_{sport}_{nom1[:10]}_{nom2[:10]}".replace(" ", "_"))


def _construire_competition_generique(sport: str):
    """Construit une Competition à partir du sport, sans affichage."""
    import pandas as pd
    from src.Model.Competition import Competition
    from src.Model.Equipe import Equipe
    from src.loader.GestionResultats import GestionResultats

    if sport == "football":
        df = pd.read_csv("data/football/match.csv")
        df_team = pd.read_csv("data/football/team.csv")
        teams = {r["team_api_id"]: r["team_long_name"] for _, r in df_team.iterrows()}
        abbrevs = {
            r["team_api_id"]: r["team_short_name"] for _, r in df_team.iterrows()
        }
        comp = Competition("Football", sport)
        for _, row in df.iterrows():
            hid, aid = int(row["home_team_api_id"]), int(row["away_team_api_id"])
            hg, ag = int(row["home_team_goal"]), int(row["away_team_goal"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(
                        str(tid),
                        Equipe(teams.get(tid, str(tid)), sport, abbrevs.get(tid)),
                    )
            comp.equipes[str(hid)].ajouter_match(hg, ag)
            comp.equipes[str(aid)].ajouter_match(ag, hg)

    elif sport == "basketball":
        df = pd.read_csv("data/basketball/game.csv")
        df_team = pd.read_csv("data/basketball/team.csv")
        teams = {r["id"]: r["full_name"] for _, r in df_team.iterrows()}
        abbrevs = {r["id"]: r["abbreviation"] for _, r in df_team.iterrows()}
        comp = Competition("NBA", sport)
        for _, row in df.iterrows():
            hid, aid = int(row["team_id_home"]), int(row["team_id_away"])
            hpts, apts = int(row["pts_home"]), int(row["pts_away"])
            for tid in [hid, aid]:
                if str(tid) not in comp.equipes:
                    comp.ajouter_equipe(
                        str(tid),
                        Equipe(teams.get(tid, str(tid)), sport, abbrevs.get(tid)),
                    )
            comp.equipes[str(hid)].ajouter_match(hpts, apts, nul_possible=False)
            comp.equipes[str(aid)].ajouter_match(apts, hpts, nul_possible=False)

    elif sport == "LOL":
        df = pd.read_csv("data/LOL/match.csv")
        df_team = pd.read_csv("data/LOL/team.csv")
        teams_info = {r["team_abbreviation"]: r["team"] for _, r in df_team.iterrows()}
        comp = Competition("LoL EMEA 2025", sport)
        for _, row in df.iterrows():
            for side in ["blue", "red"]:
                abrev = str(row[f"team_{side}"])
                if abrev not in comp.equipes:
                    comp.ajouter_equipe(
                        abrev, Equipe(teams_info.get(abrev, abrev), sport, abrev)
                    )
                e = comp.equipes[abrev]
                e.matchs_joues += 1
                e.score_pour += int(row.get(f"kills_team_{side}") or 0)
                e.score_contre += int(
                    row.get(f"kills_team_{'red' if side == 'blue' else 'blue'}") or 0
                )
                if str(row["winner"]) == abrev:
                    e.victoires += 1
                    e.points += 1
                else:
                    e.defaites += 1

    elif sport == "tennis":
        df_m = pd.read_csv("data/tennis/atp_matches_2024.csv")
        df_p = pd.read_csv("data/tennis/atp_players_2024.csv")
        players = {
            str(int(r["player_id"])): r["name_first"] + " " + r["name_last"]
            for _, r in df_p.iterrows()
        }
        comp = Competition("ATP 2024", sport)
        for _, row in df_m.iterrows():
            wid, lid = str(int(row["winner_id"])), str(int(row["loser_id"]))
            for pid in [wid, lid]:
                if pid not in comp.equipes:
                    comp.ajouter_equipe(pid, Equipe(players.get(pid, pid), sport))
            comp.equipes[wid].ajouter_match(1, 0, nul_possible=False)
            comp.equipes[lid].ajouter_match(0, 1, nul_possible=False)

    elif sport == "volley":
        df_m = pd.read_csv("data/volley/match_men.csv")
        df_country = pd.read_csv("data/volley/country.csv")
        countries = {r["code"]: r["country"] for _, r in df_country.iterrows()}
        comp = Competition("Volley Hommes JO 2024", sport)
        for _, row in df_m.iterrows():
            c1, c2 = str(row["country_code_1"]), str(row["country_code_2"])
            s1, s2 = int(row["set_country_1"]), int(row["set_country_2"])
            for code in [c1, c2]:
                if code not in comp.equipes:
                    comp.ajouter_equipe(
                        code, Equipe(countries.get(code, code), sport, code)
                    )
            comp.equipes[c1].ajouter_match(s1, s2, nul_possible=False)
            comp.equipes[c2].ajouter_match(s2, s1, nul_possible=False)
    else:
        return None

    GestionResultats.appliquer_a_competition(comp, nul_possible=(sport == "football"))
    return comp


# ══════════════════════════════════════════════════════════════════════════════
# MENU INTERACTIF
# ══════════════════════════════════════════════════════════════════════════════

_MENUS: dict[str, list[tuple]] = {
    "football": [
        ("1", "Buts moyens par journée", graph_foot_buts_journee),
        ("2", "Distribution des scores", graph_foot_dist_scores),
        ("3", "Attaque vs Défense (scatter bulle)", graph_foot_attaque_defense),
        ("4", "Comparaison deux équipes", "comparaison"),
    ],
    "basketball": [
        ("1", "Distribution des scores", graph_basket_dist_scores),
        ("2", "Points marqués vs encaissés", graph_basket_pts_marqués_encaissés),
        ("3", "Top rebondeurs", graph_basket_top_rebondeurs),
        ("4", "Scores moyen Regular vs Playoffs", graph_basket_evol_scores_saison),
        ("5", "Comparaison deux équipes", "comparaison"),
    ],
    "LOL": [
        ("1", "Kills / Dragons / Barons (barres)", graph_lol_barres_groupees),
        ("2", "Gold moyen vs Winrate (scatter)", graph_lol_gold_winrate),
        ("3", "Comparaison deux équipes", "comparaison"),
    ],
    "tennis": [
        ("1", "Top 10 joueurs ATP", lambda: graph_tennis_top10("ATP")),
        ("2", "Top 10 joueuses WTA", lambda: graph_tennis_top10("WTA")),
        ("3", "Surface ATP (camembert)", lambda: graph_tennis_surface("ATP")),
        ("4", "Surface WTA (camembert)", lambda: graph_tennis_surface("WTA")),
        ("5", "Taille ATP vs WTA", graph_tennis_atp_wta_taille),
        ("6", "Nationalités ATP (camembert)", lambda: graph_tennis_nationalite("ATP")),
        ("7", "Nationalités WTA (camembert)", lambda: graph_tennis_nationalite("WTA")),
    ],
    "volley": [
        ("1", "Taille moyenne par pays H/F", graph_volley_taille_pays),
        (
            "2",
            "Matchs par pays — Hommes",
            lambda: graph_volley_camembert_pays("Hommes"),
        ),
        (
            "3",
            "Matchs par pays — Femmes",
            lambda: graph_volley_camembert_pays("Femmes"),
        ),
    ],
}


def run_menu(sport_nom: str) -> None:
    """Menu graphique interactif pour un sport donné."""
    os.makedirs("output", exist_ok=True)
    menu = _MENUS.get(sport_nom)
    if menu is None:
        print(f"  Pas de graphiques disponibles pour '{sport_nom}'.")
        return

    while True:
        print(f"\n  ── Graphiques — {sport_nom.upper()} " + "─" * 30)
        for num, label, _ in menu:
            print(f"    {num}  {label}")
        print("    0  Retour")

        choix = input("\n  Votre choix : ").strip()
        if choix == "0":
            break

        entree = next(((n, l, fn) for n, l, fn in menu if n == choix), None)
        if entree is None:
            print("  Choix invalide.")
            continue

        _, label, fn = entree

        if fn == "comparaison":
            nom1 = input("  Équipe 1 : ").strip()
            nom2 = input("  Équipe 2 : ").strip()
            try:
                path = graph_comparaison_equipes(sport_nom, nom1, nom2)
                print(f"\n  Graphique généré : {path}")
            except ValueError as e:
                print(f"  Erreur : {e}")
            continue

        # Graphiques avec paramètres optionnels pour le football/basket
        try:
            if sport_nom == "football" and choix in ("1", "2", "3"):
                df_league = pd.read_csv("data/football/league.csv")
                leagues = {r["id"]: r["name"] for _, r in df_league.iterrows()}
                print(
                    "  Ligues :", ", ".join(f"{lid}={n}" for lid, n in leagues.items())
                )
                lid_in = input("  ID ligue (0 = toutes) : ").strip()
                lid = int(lid_in) if lid_in and lid_in != "0" else None
                df_match = pd.read_csv("data/football/match.csv")
                saisons = sorted(df_match["season"].unique())
                print("  Saisons :", ", ".join(saisons))
                saison = input("  Saison (vide = toutes) : ").strip() or None
                path = fn(league_id=lid, saison=saison)
            elif sport_nom == "basketball" and choix in ("1", "2", "3"):
                df_game = pd.read_csv("data/basketball/game.csv")
                types = sorted(df_game["season_type"].unique())
                print("  Types :", ", ".join(types))
                st = input("  Type de saison : ").strip()
                path = fn(season_type=st) if st in types else fn()
            else:
                path = fn()
            print(f"\n  Graphique généré : {path}")
        except Exception as e:
            print(f"  Erreur : {e}")
