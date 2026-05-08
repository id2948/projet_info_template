"""Diagramme d'états et de fonctionnement — format A4 portrait, lisible."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

# ── Palette ───────────────────────────────────────────────────────────────────
C_INIT = "#1a1a2e"
C_MENU = "#0D47A1"
C_ACT = "#1B5E20"
C_GRAPH = "#4A148C"
C_DATA = "#37474F"
C_OUT = "#004D40"
C_ERR = "#B71C1C"
BG = "#FFFFFF"
FW = "#FFFFFF"
FD = "#212121"
ARROW = "#37474F"

# ── Helpers ───────────────────────────────────────────────────────────────────


def rounded_box(
    ax, cx, cy, w, h, title, lines, color, title_fs=10, body_fs=8.5, lw=1.3
):
    """Boîte avec titre gras et liste de lignes de contenu."""
    rect = FancyBboxPatch(
        (cx - w / 2, cy - h / 2),
        w,
        h,
        boxstyle="round,pad=0.06,rounding_size=0.10",
        facecolor=color,
        edgecolor="#37474F",
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(rect)
    # Trait séparateur sous le titre
    n_total = 1 + len(lines)
    row_h = h / n_total
    ty = cy + h / 2 - row_h / 2
    ax.text(
        cx,
        ty,
        title,
        ha="center",
        va="center",
        fontsize=title_fs,
        color=FW,
        fontweight="bold",
        zorder=4,
    )
    if lines:
        sep_y = cy + h / 2 - row_h
        ax.plot(
            [cx - w / 2 + 0.05, cx + w / 2 - 0.05],
            [sep_y, sep_y],
            color="white",
            lw=0.6,
            alpha=0.5,
            zorder=4,
        )
        body_top = sep_y - 0.02
        body_h = h - row_h - 0.04
        step = body_h / len(lines)
        for i, line in enumerate(lines):
            ly = body_top - step / 2 - i * step
            ax.text(
                cx - w / 2 + 0.18,
                ly,
                "• " + line,
                ha="left",
                va="center",
                fontsize=body_fs,
                color=FW,
                zorder=4,
                alpha=0.93,
            )


def dot_init(ax, cx, cy, r=0.14):
    ax.add_patch(plt.Circle((cx, cy), r, color=C_INIT, zorder=5))


def dot_end(ax, cx, cy, r=0.14):
    ax.add_patch(plt.Circle((cx, cy), r, color=C_INIT, zorder=5))
    ax.add_patch(
        plt.Circle((cx, cy), r + 0.09, color="none", ec=C_INIT, lw=2.0, zorder=5)
    )


def arrow(
    ax,
    x1,
    y1,
    x2,
    y2,
    label="",
    color=ARROW,
    rad=0.0,
    lw=1.5,
    ls="-",
    label_dx=0.08,
    label_dy=0.0,
    label_ha="left",
):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=lw,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=ls,
        ),
        zorder=2,
    )
    if label:
        mx = (x1 + x2) / 2 + label_dx
        my = (y1 + y2) / 2 + label_dy
        ax.text(
            mx,
            my,
            label,
            fontsize=7.5,
            color=color,
            ha=label_ha,
            va="center",
            bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none", alpha=0.85),
            zorder=5,
        )


def band(ax, y0, h, label, color="#F5F5F5", ec="#CFD8DC"):
    ax.add_patch(
        FancyBboxPatch(
            (0.2, y0),
            13.6,
            h,
            boxstyle="square,pad=0",
            facecolor=color,
            edgecolor=ec,
            lw=0.7,
            zorder=0,
            alpha=0.55,
        )
    )
    ax.text(
        0.28,
        y0 + h - 0.07,
        label,
        fontsize=7,
        color="#78909C",
        ha="left",
        va="top",
        style="italic",
    )


# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 22))
ax.set_xlim(0, 14)
ax.set_ylim(0, 22)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(
    7,
    21.65,
    "Diagramme d'états et de fonctionnement",
    ha="center",
    va="center",
    fontsize=16,
    fontweight="bold",
    color=C_INIT,
)
ax.text(
    7,
    21.28,
    "Application Sportive  ·  5 sports : Basketball · Football · LoL · Tennis · Volleyball",
    ha="center",
    va="center",
    fontsize=9,
    color="#546E7A",
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION A — NAVIGATION PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════
band(ax, 19.20, 1.80, "A — NAVIGATION PRINCIPALE", "#E3F2FD", "#90CAF9")

# Init
dot_init(ax, 2.5, 20.80)
arrow(ax, 2.5, 20.66, 2.5, 20.26)

# Menu Sport
rounded_box(
    ax,
    2.5,
    19.98,
    4.0,
    0.52,
    "MENU SPORT",
    ["basketball · football · LOL · tennis · volley"],
    C_MENU,
    title_fs=10,
    body_fs=8,
)

# → q / FIN
arrow(
    ax,
    4.5,
    19.98,
    5.5,
    19.98,
    label="q",
    color="#546E7A",
    label_dx=0.06,
    label_ha="left",
)
dot_end(ax, 5.72, 19.98)
ax.text(6.0, 19.98, "FIN", fontsize=8.5, color=C_INIT, va="center", fontweight="bold")

# → sport invalide (boucle)
arrow(ax, 0.5, 19.98, 0.5, 20.50, color=C_ERR, rad=0.0, lw=1.1, ls="dashed")
ax.text(0.55, 20.24, "invalide", fontsize=7, color=C_ERR, va="center")

# → valide descend
arrow(ax, 2.5, 19.72, 2.5, 19.42, label="sport valide", label_dx=0.1, label_ha="left")

# Menu Catégorie
rounded_box(
    ax,
    2.5,
    19.14,
    4.6,
    0.52,
    "MENU CATÉGORIE",
    ["match · joueur · equipe · competition · graphiques · ajouter · historique"],
    C_MENU,
    title_fs=10,
    body_fs=7.8,
)

# → q / FIN
arrow(
    ax,
    4.8,
    19.14,
    5.5,
    19.14,
    label="q",
    color="#546E7A",
    label_dx=0.06,
    label_ha="left",
)
dot_end(ax, 5.72, 19.14)
ax.text(6.0, 19.14, "FIN", fontsize=8.5, color=C_INIT, va="center", fontweight="bold")

# retour → menu sport
arrow(
    ax,
    0.5,
    19.14,
    0.5,
    19.72,
    color="#546E7A",
    rad=0.0,
    lw=1.1,
    label="retour",
    label_dx=0.08,
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION B — SOUS-MENUS (rangée 1 : 4 catégories)
# ══════════════════════════════════════════════════════════════════════════════
band(ax, 15.00, 3.95, "B — SOUS-MENUS PAR CATÉGORIE", "#E8F5E9", "#A5D6A7")

# Flèche menu catégorie → sous-menus
arrow(
    ax,
    2.5,
    18.88,
    7.0,
    18.82,
    color=ARROW,
    lw=1.2,
    ls="dashed",
    label="catégorie choisie",
    label_dx=0.1,
)

# 4 boîtes rangée 1
R1Y = 16.70
R1_BOXES = [
    (
        1.65,
        "MATCH",
        [
            "Matchs d'une équipe",
            "Confrontation directe",
            "Matchs à une date",
            "Filtre par score seuil",
            "Statistiques agrégées",
        ],
        C_ACT,
    ),
    (
        4.65,
        "JOUEUR",
        [
            "Recherche par nom",
            "Statistiques d'un joueur",
            "Top N joueurs",
            "Classement par stat",
        ],
        C_ACT,
    ),
    (
        7.65,
        "ÉQUIPE",
        [
            "Stats globales équipe",
            "Forme récente",
            "Comparaison 2 équipes",
        ],
        C_ACT,
    ),
    (
        11.0,
        "COMPÉTITION",
        [
            "Classement général",
            "Meilleures attaques",
            "Meilleures défenses",
            "Classement toutes saisons",
        ],
        C_ACT,
    ),
]

for cx, title, lines, col in R1_BOXES:
    bh = 0.40 + len(lines) * 0.30
    by = R1Y - bh / 2 + 0.38
    rounded_box(ax, cx, by, 2.65, bh, title, lines, col, title_fs=9.5, body_fs=8)
    # sortie affichage
    note_y = by - bh / 2 - 0.20
    ax.text(
        cx,
        note_y,
        "→ affichage terminal",
        ha="center",
        va="center",
        fontsize=7.5,
        color=C_OUT,
        bbox=dict(boxstyle="round,pad=0.18", fc="#E8F5E9", ec="#66BB6A", lw=0.8),
    )
    # retour
    arrow(ax, cx, note_y - 0.18, cx, note_y - 0.45, color="#546E7A", lw=1.0)
    ax.text(
        cx,
        note_y - 0.55,
        "↺ retour menu catégorie",
        ha="center",
        va="center",
        fontsize=6.8,
        color="#546E7A",
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION C — SOUS-MENUS (rangée 2 : 3 catégories)
# ══════════════════════════════════════════════════════════════════════════════
band(ax, 10.00, 4.75, "C — CATÉGORIES SPÉCIALES", "#EDE7F6", "#CE93D8")

R2Y = 12.80
R2_BOXES = [
    (
        2.5,
        "GRAPHIQUES",
        [
            "[c]  Classement tableau PNG",
            "[1–N]  Graphiques statistiques",
            "[7]  Radar spider chart",
            "[8]  Comparaison 2 équipes",
            "Paramètres : ligue, saison,",
            "  circuit, genre selon sport",
        ],
        C_GRAPH,
    ),
    (
        7.0,
        "AJOUTER UN RÉSULTAT",
        [
            "Saisie : date (AAAA-MM-JJ)",
            "Saisie : nom équipe 1",
            "Saisie : nom équipe 2",
            "Saisie : score équipe 1",
            "Saisie : score équipe 2",
            "Validation et enregistrement",
        ],
        C_GRAPH,
    ),
    (
        11.8,
        "HISTORIQUE",
        [
            "Lecture nouveaux_matchs.csv",
            "Affichage liste triée",
            "par date et sport",
        ],
        C_ACT,
    ),
]

for cx, title, lines, col in R2_BOXES:
    bh = 0.42 + len(lines) * 0.31
    by = R2Y - bh / 2 + 0.42
    rounded_box(ax, cx, by, 2.80, bh, title, lines, col, title_fs=9.5, body_fs=8.0)
    # sorties spécifiques
    note_y = by - bh / 2 - 0.20
    if "GRAPHIQUES" in title:
        ax.text(
            cx,
            note_y,
            "→ sauvegarde  output/*.png",
            ha="center",
            va="center",
            fontsize=7.5,
            color=C_GRAPH,
            bbox=dict(boxstyle="round,pad=0.18", fc="#EDE7F6", ec="#CE93D8", lw=0.8),
        )
    elif "AJOUTER" in title:
        ax.text(
            cx,
            note_y,
            "✓ valide → data/resultats/nouveaux_matchs.csv\n✗ invalide → annulation + message erreur",
            ha="center",
            va="center",
            fontsize=7.2,
            color=C_ERR,
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFF3E0", ec="#FFCC80", lw=0.8),
        )
    else:
        ax.text(
            cx,
            note_y,
            "→ affichage terminal",
            ha="center",
            va="center",
            fontsize=7.5,
            color=C_OUT,
            bbox=dict(boxstyle="round,pad=0.18", fc="#E8F5E9", ec="#66BB6A", lw=0.8),
        )
    arrow(ax, cx, note_y - 0.22, cx, note_y - 0.50, color="#546E7A", lw=1.0)
    ax.text(
        cx,
        note_y - 0.60,
        "↺ retour menu catégorie",
        ha="center",
        va="center",
        fontsize=6.8,
        color="#546E7A",
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION D — COUCHE DONNÉES
# ══════════════════════════════════════════════════════════════════════════════
band(ax, 6.60, 3.15, "D — COUCHE DONNÉES CSV", "#ECEFF1", "#90A4AE")

data = [
    (1.3, "football/", "match · team\nleague · country\nplayer"),
    (3.6, "basketball/", "game · team\nplayer"),
    (5.7, "LOL/", "match · team\nplayer · coach"),
    (7.9, "tennis/", "atp_matches\natp_players\nwta_matches · wta_players"),
    (10.3, "volley/", "match_men/women\ncountry\nplayer_men/women"),
    (12.7, "resultats/", "nouveaux_matchs.csv\n← écriture (ajouter)\n→ lecture (tous)"),
]

for xd, folder, content in data:
    is_res = "resultats" in folder
    fc = "#FBE9E7" if is_res else "#F5F5F5"
    ec = "#BF360C" if is_res else "#78909C"
    rect = FancyBboxPatch(
        (xd - 1.0, 6.85),
        2.0,
        2.65,
        boxstyle="round,pad=0.07,rounding_size=0.08",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
        zorder=3,
    )
    ax.add_patch(rect)
    ax.text(
        xd,
        9.17,
        folder,
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#BF360C" if is_res else C_DATA,
        zorder=4,
    )
    ax.plot([xd - 0.90, xd + 0.90], [8.93, 8.93], color=ec, lw=0.6, zorder=4)
    ax.text(
        xd,
        8.20,
        content,
        ha="center",
        va="center",
        fontsize=7.2,
        color=FD,
        zorder=4,
        linespacing=1.4,
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION E — SORTIES
# ══════════════════════════════════════════════════════════════════════════════
band(ax, 3.90, 2.45, "E — SORTIES DE L'APPLICATION", "#E0F2F1", "#80CBC4")

rounded_box(
    ax,
    3.5,
    5.10,
    5.5,
    1.60,
    "TERMINAL (stdout)",
    [
        "Classements ASCII (compétition)",
        "Statistiques joueurs et équipes",
        "Résultats de matchs filtrés",
        "Historique des résultats ajoutés",
        "Menus et messages interactifs",
    ],
    C_DATA,
    title_fs=10,
    body_fs=8.2,
)

rounded_box(
    ax,
    10.5,
    5.10,
    5.5,
    1.60,
    "FICHIERS  output/*.png",
    [
        "Classements visuels (tableau stylisé)",
        "Graphiques statistiques par sport",
        "Radar spider chart par équipe",
        "Comparaisons et distributions",
        "Pyramides des âges, scatter plots…",
    ],
    C_GRAPH,
    title_fs=10,
    body_fs=8.2,
)

# ── Flèches de lecture CSV (sections B/C → données) ─────────────────────────
for xsrc in [1.65, 4.65, 7.65, 11.0, 2.5, 7.0, 11.8]:
    ax.annotate(
        "",
        xy=(xsrc, 9.50),
        xytext=(xsrc, 9.90),
        arrowprops=dict(arrowstyle="-|>", color="#B0BEC5", lw=0.9, linestyle="dashed"),
        zorder=2,
    )

# Flèche écriture ajouter → resultats
ax.annotate(
    "",
    xy=(12.7, 9.50),
    xytext=(7.0, 9.80),
    arrowprops=dict(arrowstyle="-|>", color="#BF360C", lw=1.5),
    zorder=2,
)
ax.text(10.2, 9.92, "écriture CSV", fontsize=7.5, color="#BF360C", ha="center")

# Flèches sections E (sorties) ← données (lecture)
ax.annotate(
    "",
    xy=(3.5, 6.85),
    xytext=(3.5, 6.30),
    arrowprops=dict(arrowstyle="-|>", color="#B0BEC5", lw=0.9, linestyle="dashed"),
)
ax.annotate(
    "",
    xy=(10.5, 6.85),
    xytext=(10.5, 6.30),
    arrowprops=dict(arrowstyle="-|>", color="#B0BEC5", lw=0.9, linestyle="dashed"),
)

# Note intégration automatique
ax.text(
    7.0,
    3.65,
    "Les résultats ajoutés via « ajouter » sont automatiquement pris en compte\n"
    "dans tous les classements, statistiques et graphiques (GestionResultats)",
    ha="center",
    va="center",
    fontsize=8.0,
    color=C_DATA,
    bbox=dict(boxstyle="round,pad=0.35", fc="#ECEFF1", ec="#90A4AE", lw=1.0),
)

# ── Légende ───────────────────────────────────────────────────────────────────
légende = [
    (C_MENU, "Menu (état composite)"),
    (C_ACT, "Action / affichage terminal"),
    (C_GRAPH, "Saisie / génération PNG"),
    (C_DATA, "Données CSV / Sorties"),
    (C_ERR, "Transition d'erreur"),
]
handles = [
    mpatches.Patch(facecolor=c, edgecolor="#37474F", label=l) for c, l in légende
]
ax.legend(
    handles=handles,
    loc="lower center",
    ncol=5,
    fontsize=8,
    frameon=True,
    edgecolor="#CFD8DC",
    facecolor=BG,
    bbox_to_anchor=(0.5, 0.002),
)

plt.tight_layout(pad=0.4)
os.makedirs("output", exist_ok=True)
path = "output/diagramme_etats.png"
plt.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Diagramme sauvegardé : {path}")
