import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import matplotlib.patches as mpatches
import numpy as np
import os

BG = "#FFFFFF"
LW = 1.0



def box(ax, cx, cy, w, h, texte, fs=7.5, bold=False, dash=False):
    ls = (0, (4, 3)) if dash else "-"
    ax.add_patch(
        FancyBboxPatch(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            boxstyle="round,pad=0.04,rounding_size=0.09",
            facecolor="#FFFFFF",
            edgecolor="#111111",
            linewidth=LW,
            linestyle=ls,
            zorder=3,
        )
    )
    fw = "bold" if bold else "normal"
    ax.text(
        cx,
        cy,
        texte,
        ha="center",
        va="center",
        fontsize=fs,
        color="#111111",
        fontweight=fw,
        zorder=4,
        linespacing=1.30,
    )


def box_filled(ax, cx, cy, w, h, texte, fs=8.5):
    ax.add_patch(
        FancyBboxPatch(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            boxstyle="round,pad=0.04,rounding_size=0.09",
            facecolor="#1a1a1a",
            edgecolor="#111111",
            linewidth=LW,
            zorder=3,
        )
    )
    ax.text(
        cx,
        cy,
        texte,
        ha="center",
        va="center",
        fontsize=fs,
        color="#FFFFFF",
        fontweight="bold",
        zorder=4,
        linespacing=1.30,
    )


def diamond(ax, cx, cy, w=0.42, h=0.28):
    pts = np.array([[cx, cy + h], [cx + w, cy], [cx, cy - h], [cx - w, cy]])
    ax.add_patch(
        Polygon(
            pts,
            closed=True,
            facecolor="#FFFFFF",
            edgecolor="#111111",
            linewidth=LW,
            zorder=3,
        )
    )


def oval(ax, cx, cy, w, h, texte, fs=8.5):
    ax.add_patch(
        mpatches.Ellipse(
            (cx, cy),
            w,
            h,
            facecolor="#FFFFFF",
            edgecolor="#111111",
            linewidth=LW,
            zorder=3,
        )
    )
    ax.text(
        cx,
        cy,
        texte,
        ha="center",
        va="center",
        fontsize=fs,
        color="#111111",
        fontweight="bold",
        zorder=4,
    )


def arr(ax, x1, y1, x2, y2, rad=0.0, lw=LW):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#111111",
            lw=lw,
            connectionstyle=f"arc3,rad={rad}",
            mutation_scale=8,
        ),
        zorder=2,
    )


def lbl(ax, x, y, t, fs=7, ha="left", col="#333333"):
    ax.text(
        x,
        y,
        t,
        ha=ha,
        va="center",
        fontsize=fs,
        color=col,
        bbox=dict(boxstyle="round,pad=0.08", fc=BG, ec="none", alpha=0.92),
        zorder=5,
    )


def hline(ax, x1, x2, y, lw=LW):
    ax.plot([x1, x2], [y, y], color="#111111", lw=lw, zorder=2)


def vline(ax, x, y1, y2, lw=LW):
    ax.plot([x, x], [y1, y2], color="#111111", lw=lw, zorder=2)


W = 14

Y_TOP = 36.0
Y_BOT = 25.0  
H_COORD = Y_TOP - Y_BOT  

fig, ax = plt.subplots(figsize=(W, W * H_COORD / W))  
ax.set_xlim(0, W)
ax.axis("off")
fig.patch.set_facecolor(BG)


ax.text(
    W / 2,
    35.5,
    "Diagramme de fonctionnement — Application Sportive",
    ha="center",
    fontsize=14,
    fontweight="bold",
    color="#111111",
)


CX = W / 2

oval(ax, CX, 34.60, 1.4, 0.46, "Départ", fs=8.5)
arr(ax, CX, 34.37, CX, 34.00)

box_filled(ax, CX, 33.72, 3.4, 0.50, "Menu principal\n(choix du sport)", fs=8.5)


arr(ax, CX - 1.70, 33.72, CX - 3.10, 33.72)
lbl(ax, CX - 3.85, 33.82, "q", fs=8)
oval(ax, CX - 4.15, 33.72, 0.90, 0.42, "Fin", fs=8)


diamond(ax, CX, 33.18)
arr(ax, CX, 33.47, CX, 33.47 - 0.01)
lbl(ax, CX + 0.48, 33.18, "sport\nreconnu ?", fs=7)

vline(ax, CX - 1.80, 33.18, 33.98)
hline(ax, CX - 1.80, CX - 0.42, 33.18)
hline(ax, CX - 1.80, CX - 1.70, 33.98)
lbl(ax, CX - 2.95, 33.55, "Non", fs=7, col="#B71C1C")
lbl(ax, CX + 0.08, 32.82, "Oui", fs=7, col="#1B5E20")


arr(ax, CX, 32.90, CX, 32.58)
SX = [2.0, 4.3, 7.0, 9.7, 12.0]
for sx in SX:
    arr(ax, CX, 32.40, sx, 32.10)
lbl(ax, 5.5, 32.48, "Sélection du sport", fs=7)
SPORTS = ["basketball", "football", "LOL", "tennis", "volley"]
for sx, sp in zip(SX, SPORTS):
    box(ax, sx, 31.85, 2.05, 0.42, sp, fs=8, bold=True)


vline(ax, 13.20, 31.85, 33.98)
hline(ax, 12.03, 13.20, 31.85)
hline(ax, 13.20, CX + 1.70, 33.98)
lbl(ax, 13.25, 32.85, "retour", fs=7, col="#546E7A")


for sx in SX:
    arr(ax, sx, 31.64, CX, 31.30)

box_filled(
    ax,
    CX,
    31.02,
    6.0,
    0.50,
    "Menu catégorie\n"
    "match · joueur · equipe · competition · graphiques · ajouter · historique",
    fs=8,
)


BW = 1.78  
BH = 0.42  
DY = 0.60  
TOP_Y = 30.60  
CXS = [1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 13.0]

BRANCHES = [
    (
        "match",
        "Sous-menu Match",
        [
            "Matchs d'une équipe",
            "Confrontations directes",
            "Matchs par date",
            "Filtre score / seuil",
            "Statistiques agrégées",
        ],
    ),
    (
        "joueur",
        "Sous-menu Joueur",
        [
            "Chercher par nom",
            "Chercher par équipe",
            "Chercher par position",
            "Stats d'un joueur",
        ],
    ),
    (
        "equipe",
        "Sous-menu Équipe",
        [
            "Stats V/D/N/Pts",
            "Top attaque",
            "Top défense",
            "Classement",
        ],
    ),
    (
        "competition",
        "Sous-menu Compétition",
        [
            "Classement général",
            "Stats par ligue",
            "Top attaque / défense",
            "Toutes saisons",
        ],
    ),
    (
        "graphiques",
        "Sous-menu Graphiques",
        [
            "[c] Classement PNG",
            "[1-N] Stats graphiques",
            "[7] Radar équipe",
            "[8] Comparaison",
            "Saisie paramètres",
        ],
    ),
    (
        "ajouter",
        "Saisie guidée",
        [
            "Date (AAAA-MM-JJ)",
            "Équipe 1",
            "Équipe 2",
            "Score 1",
            "Score 2",
        ],
    ),
    (
        "historique",
        "Lecture historique",
        [
            "Lecture CSV",
            "Affichage liste triée",
        ],
    ),
]


for cx in CXS:
    arr(ax, CX, 30.77, cx, TOP_Y + 0.25)

for cx, (cat, subtitle, items) in zip(CXS, BRANCHES):
    
    box(ax, cx, TOP_Y, BW, 0.44, cat, fs=8, bold=True)
    ax.text(
        cx,
        TOP_Y - 0.32,
        subtitle,
        ha="center",
        va="center",
        fontsize=6,
        color="#555555",
        zorder=4,
    )
  
    for i, txt in enumerate(items):
        yi = TOP_Y - 0.68 - i * DY
        arr(ax, cx, TOP_Y - 0.44 - i * DY, cx, yi + BH / 2)
        box(ax, cx, yi, BW, BH, txt, fs=7)
   
    y_last = TOP_Y - 0.68 - (len(items) - 1) * DY
    y_out = y_last - BH / 2 - 0.14
    arr(ax, cx, y_last - BH / 2, cx, y_out)

    if cat == "graphiques":
        diamond(ax, cx, y_out, w=0.38, h=0.24)
        lbl(ax, cx + 0.42, y_out, "valide ?", fs=6.5)
        y_save = y_out - 0.55
        arr(ax, cx, y_out - 0.24, cx, y_save + BH / 2)
        lbl(ax, cx + 0.08, y_out - 0.38, "Oui", fs=6.5, col="#1B5E20")
        box(ax, cx, y_save, BW, BH, "Sauvegarde\noutput/*.png", fs=6.5, dash=True)
        y_bottom = y_save - BH / 2
        vline(ax, cx - 0.90, y_out, y_out + 0.45)
        hline(ax, cx - 0.90, cx - 0.38, y_out)
        lbl(ax, cx - 1.88, y_out + 0.12, "Non\n→retour", fs=6.2, col="#B71C1C")

    elif cat == "ajouter":
        diamond(ax, cx, y_out, w=0.38, h=0.24)
        lbl(ax, cx + 0.42, y_out, "valide ?", fs=6.5)
        y_save = y_out - 0.55
        arr(ax, cx, y_out - 0.24, cx, y_save + BH / 2)
        lbl(ax, cx + 0.08, y_out - 0.38, "Oui", fs=6.5, col="#1B5E20")
        box(ax, cx, y_save, BW, BH, "→ nouveaux_matchs.csv", fs=6.5, dash=True)
        box(ax, cx + 1.0, y_out, BW - 0.3, 0.32, "Annulation", fs=6.5, dash=True)
        hline(ax, cx + 0.38, cx + 1.0, y_out)
        lbl(ax, cx + 0.42, y_out + 0.20, "Non", fs=6.2, col="#B71C1C")
        y_bottom = y_save - BH / 2

    else:
        box(ax, cx, y_out, BW, BH, "Affichage\nterminal", fs=7, dash=True)
        y_bottom = y_out - BH / 2


    side = cx - BW / 2 - 0.08 if cx <= CX else cx + BW / 2 + 0.08
    rad = 0.3 if cx <= CX else -0.3
    arr(ax, cx, y_bottom - 0.04, cx, y_bottom - 0.20, lw=0.7)
    ax.text(
        cx,
        y_bottom - 0.33,
        "↺ retour",
        ha="center",
        va="center",
        fontsize=6,
        color="#546E7A",
        zorder=4,
    )


y_last_long = TOP_Y - 0.68 - 4 * DY  
y_out_long = y_last_long - BH / 2 - 0.14 
y_save_long = y_out_long - 0.55  
y_content_bot = y_save_long - BH / 2 - 0.40  

NOTE_Y = y_content_bot - 0.45
ax.text(
    W / 2,
    NOTE_Y,
    "Les résultats ajoutés via « ajouter » sont automatiquement intégrés\n"
    "dans tous les classements, statistiques et graphiques (GestionResultats).",
    ha="center",
    va="center",
    fontsize=7.5,
    color="#444",
    bbox=dict(boxstyle="round,pad=0.35", fc="#F5F5F5", ec="#BBBBBB", lw=0.8),
)


Y_TOP_REAL = 36.0
Y_BOT_REAL = NOTE_Y - 0.50
ax.set_ylim(Y_BOT_REAL, Y_TOP_REAL)

fig.set_size_inches(W, W * (Y_TOP_REAL - Y_BOT_REAL) / W)

plt.tight_layout(pad=0.3)
os.makedirs("output", exist_ok=True)
path = "output/diagramme_bw_v3.png"
plt.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Sauvegardé : {path}")
