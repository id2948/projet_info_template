import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
import os

BG = "#FFFFFF"
FC = "#FFFFFF"  
EC = "#222222"  
TXT = "#111111"  
ARR = "#333333"  
LBL = "#333333"  
LW = 1.2




def box(ax, cx, cy, w, h, texte, fs=8.5, bold=False):
    ax.add_patch(
        FancyBboxPatch(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor=FC,
            edgecolor=EC,
            linewidth=LW,
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
        color=TXT,
        fontweight=fw,
        zorder=4,
        linespacing=1.35,
    )


def oval(ax, cx, cy, w, h, texte, fs=9, bold=True):
    ax.add_patch(
        Ellipse((cx, cy), w, h, facecolor=FC, edgecolor=EC, linewidth=LW, zorder=3)
    )
    ax.text(
        cx,
        cy,
        texte,
        ha="center",
        va="center",
        fontsize=fs,
        color=TXT,
        fontweight="bold" if bold else "normal",
        zorder=4,
    )


def arr(ax, x1, y1, x2, y2, label="", rad=0.0, label_side="mid", lfs=7.2, lw=LW):
    """Flèche avec label positionné au milieu ou décalé."""
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=ARR,
            lw=lw,
            connectionstyle=f"arc3,rad={rad}",
            mutation_scale=10,
        ),
        zorder=2,
    )
    if label:
        if label_side == "mid":
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dx, dy = 0.0, 0.0
            if abs(x2 - x1) < 0.01: 
                dx = 0.12
        elif label_side == "left":
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dx = -0.12
            dy = 0
        else:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dx = 0.12
            dy = 0
        ax.text(
            mx + dx,
            my + dy,
            label,
            ha="left" if dx >= 0 else "right",
            va="center",
            fontsize=lfs,
            color=LBL,
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.10", fc=BG, ec="none", alpha=0.9),
        )


def label_on_arrow(ax, x, y, texte, fs=7.2, ha="left"):
    ax.text(
        x,
        y,
        texte,
        ha=ha,
        va="center",
        fontsize=fs,
        color=LBL,
        zorder=5,
        bbox=dict(boxstyle="round,pad=0.10", fc=BG, ec="none", alpha=0.9),
    )



fig, ax = plt.subplots(figsize=(14, 20))
ax.set_xlim(0, 14)
ax.set_ylim(0, 20)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.text(
    7,
    19.70,
    "Diagramme de fonctionnement — Application Sportive",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color=TXT,
)


oval(ax, 1.4, 19.10, 1.6, 0.50, "Départ", fs=9)
box(ax, 7.0, 19.10, 4.2, 0.52, "Menu principal\n(choix du sport)", fs=9, bold=True)

arr(ax, 2.2, 19.10, 4.88, 19.10)

arr(ax, 9.1, 19.10, 11.0, 19.10)
label_on_arrow(ax, 9.18, 19.22, "L'utilisateur saisit « q »", fs=7)
oval(ax, 11.9, 19.10, 1.6, 0.50, "Fin", fs=9)

ax.annotate(
    "",
    xy=(6.0, 18.94),
    xytext=(6.0, 18.65),
    arrowprops=dict(arrowstyle="-|>", color=ARR, lw=LW, connectionstyle="arc3,rad=0.0"),
    zorder=2,
)
ax.annotate(
    "",
    xy=(6.0, 18.65),
    xytext=(8.0, 18.65),
    arrowprops=dict(arrowstyle="-", color=ARR, lw=LW),
    zorder=2,
)
ax.annotate(
    "",
    xy=(8.0, 18.65),
    xytext=(8.0, 18.84),
    arrowprops=dict(arrowstyle="-", color=ARR, lw=LW),
    zorder=2,
)
label_on_arrow(ax, 6.05, 18.58, "Sport non reconnu → re-affichage du menu", fs=7)


arr(ax, 7.0, 18.84, 7.0, 18.28, label="L'utilisateur saisit un sport valide", lfs=7.2)

SPORTS_X = [1.5, 4.0, 7.0, 10.0, 12.5]
SPORTS = ["basketball", "football", "LOL", "tennis", "volley"]

for sx, sp in zip(SPORTS_X, SPORTS):
    arr(ax, 7.0, 18.00, sx, 17.68, lw=1.0)

for sx, sp in zip(SPORTS_X, SPORTS):
    box(ax, sx, 17.42, 2.30, 0.48, f"Menu\n{sp}", fs=8, bold=True)

label_on_arrow(ax, 1.55, 17.95, "basketball", fs=6.8, ha="left")
label_on_arrow(ax, 4.05, 17.95, "football", fs=6.8, ha="left")
label_on_arrow(ax, 7.05, 17.85, "LOL", fs=6.8, ha="left")
label_on_arrow(ax, 9.50, 17.90, "tennis", fs=6.8, ha="left")
label_on_arrow(ax, 11.80, 17.92, "volley", fs=6.8, ha="left")

for sx in SPORTS_X:
    arr(ax, sx, 17.18, 7.0, 16.70, lw=0.9)
label_on_arrow(
    ax, 7.08, 17.05, "L'utilisateur choisit une catégorie ou « retour »", fs=7.0
)

box(
    ax,
    7.0,
    16.46,
    6.0,
    0.50,
    "Menu catégorie\n(match · joueur · equipe · competition · graphiques · ajouter · historique)",
    fs=8,
    bold=True,
)

ax.annotate(
    "",
    xy=(1.4, 18.85),
    xytext=(1.4, 16.46),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=1.0, connectionstyle="arc3,rad=0.0"
    ),
    zorder=2,
)
label_on_arrow(ax, 0.05, 17.65, "L'utilisateur saisit\n« retour »", fs=7, ha="left")

arr(ax, 10.0, 16.46, 11.5, 16.46, lw=1.0)
label_on_arrow(ax, 10.05, 16.58, "L'utilisateur saisit « q »", fs=7)
oval(ax, 12.4, 16.46, 1.6, 0.50, "Fin", fs=9)


CATS_X = [1.0, 2.85, 4.7, 6.55, 8.4, 10.5, 12.6]
CATS = [
    "match",
    "joueur",
    "equipe",
    "compé-\ntition",
    "gra-\nphiques",
    "ajouter",
    "histo-\nrique",
]

for cx, cat in zip(CATS_X, CATS):
    arr(ax, 7.0, 16.21, cx, 15.78, lw=0.9)
label_on_arrow(ax, 7.08, 16.08, "catégorie saisie", fs=6.8)

for cx, cat in zip(CATS_X, CATS):
    box(ax, cx, 15.52, 1.65, 0.48, cat, fs=8, bold=True)


arr(ax, 1.0, 15.28, 1.0, 14.82)
box(ax, 1.0, 14.58, 1.7, 0.48, "Sous-menu\nMatch", fs=7.8, bold=True)

match_actions = [
    "saisit équipe → affiche matchs de l'équipe",
    "saisit 2 équipes → affiche confrontations",
    "saisit date → affiche matchs du jour",
    "saisit seuil → filtre par score",
    "choisit stats → affiche agrégats",
]
for i, act in enumerate(match_actions):
    yi = 14.10 - i * 0.52
    arr(ax, 1.0, 14.34 - i * 0.52, 1.0, yi + 0.18, lw=0.8)
    box(ax, 1.0, yi, 1.75, 0.30, act, fs=6.5)

y_last_m = 14.10 - (len(match_actions) - 1) * 0.52
arr(ax, 1.0, y_last_m - 0.15, 1.0, y_last_m - 0.50, lw=0.8)
box(ax, 1.0, y_last_m - 0.65, 1.75, 0.28, "Affichage terminal", fs=6.5)

ax.annotate(
    "",
    xy=(4.0, 16.21),
    xytext=(1.0, y_last_m - 0.78),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=0.9, connectionstyle="arc3,rad=-0.3"
    ),
    zorder=2,
)
label_on_arrow(ax, 1.55, 12.35, "L'utilisateur saisit « retour »", fs=6.8)

arr(ax, 8.4, 15.28, 8.4, 14.82)
box(ax, 8.4, 14.58, 1.8, 0.48, "Sous-menu\nGraphiques", fs=7.8, bold=True)

arr(ax, 8.4, 14.34, 8.4, 13.88)
box(ax, 8.4, 13.65, 1.80, 0.46, "L'utilisateur saisit\nle n° du graphique", fs=7.3)

arr(ax, 8.4, 13.42, 8.4, 12.96)
box(
    ax,
    8.4,
    12.73,
    1.80,
    0.46,
    "Paramètres demandés\nsi besoin (ligue, saison…)",
    fs=7.3,
)

arr(ax, 8.4, 12.50, 8.4, 12.04)
box(ax, 8.4, 11.82, 1.80, 0.44, "Génération\ndu graphique PNG", fs=7.3)

arr(ax, 8.4, 11.60, 8.4, 11.14)
box(ax, 8.4, 10.92, 1.80, 0.44, "Sauvegarde\noutput/*.png", fs=7.3)

arr(ax, 8.4, 10.70, 8.4, 10.24)
box(ax, 8.4, 10.02, 1.80, 0.44, "Affichage\ndu chemin fichier", fs=7.3)

ax.annotate(
    "",
    xy=(7.0, 16.21),
    xytext=(8.4, 9.80),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=0.9, connectionstyle="arc3,rad=0.35"
    ),
    zorder=2,
)
label_on_arrow(ax, 9.0, 13.0, "L'utilisateur saisit\n« retour » ou « 0 »", fs=6.8)

arr(ax, 10.5, 15.28, 10.5, 14.82)
box(ax, 10.5, 14.58, 1.80, 0.48, "Saisie guidée", fs=7.8, bold=True)

ajouter_steps = [
    "Date (AAAA-MM-JJ)",
    "Nom équipe 1",
    "Nom équipe 2",
    "Score équipe 1",
    "Score équipe 2",
]
for i, step in enumerate(ajouter_steps):
    yi = 14.10 - i * 0.52
    arr(ax, 10.5, 14.34 - i * 0.52, 10.5, yi + 0.18, lw=0.8)
    box(ax, 10.5, yi, 1.80, 0.30, f"L'utilisateur saisit\n{step}", fs=6.5)

y_last_a = 14.10 - (len(ajouter_steps) - 1) * 0.52

arr(ax, 10.5, y_last_a - 0.15, 10.5, y_last_a - 0.55, lw=0.8)
box(
    ax,
    10.5,
    y_last_a - 0.70,
    1.80,
    0.28,
    "Sauvegarde dans\nnouveaux_matchs.csv",
    fs=6.5,
)
label_on_arrow(ax, 10.55, y_last_a - 0.33, "Saisie valide", fs=6.5)

ax.annotate(
    "",
    xy=(12.6, 14.10),
    xytext=(11.40, y_last_a + 0.15),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=0.9, connectionstyle="arc3,rad=-0.3"
    ),
    zorder=2,
)
label_on_arrow(ax, 11.45, 13.65, "Saisie\ninvalide", fs=6.5)
box(ax, 12.85, 14.10, 1.5, 0.38, "Affichage\nmessage erreur\n→ annulation", fs=6.5)

ax.annotate(
    "",
    xy=(7.0, 16.21),
    xytext=(10.5, y_last_a - 0.85),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=0.9, connectionstyle="arc3,rad=0.3"
    ),
    zorder=2,
)
label_on_arrow(ax, 10.55, 12.00, "L'utilisateur saisit\n« retour »", fs=6.8)

arr(ax, 12.6, 15.28, 12.6, 14.82)
box(ax, 12.6, 14.58, 1.65, 0.48, "Historique", fs=7.8, bold=True)
arr(ax, 12.6, 14.34, 12.6, 13.88, lw=0.8)
box(ax, 12.6, 13.65, 1.65, 0.46, "Lecture\nnouveaux_matchs.csv", fs=7.0)
arr(ax, 12.6, 13.42, 12.6, 12.96, lw=0.8)
box(ax, 12.6, 12.73, 1.65, 0.46, "Affichage liste\ntriée par date", fs=7.0)
ax.annotate(
    "",
    xy=(7.0, 16.21),
    xytext=(12.6, 12.50),
    arrowprops=dict(
        arrowstyle="-|>", color=ARR, lw=0.9, connectionstyle="arc3,rad=0.45"
    ),
    zorder=2,
)

ax.text(
    7.0,
    9.20,
    "Les résultats ajoutés via « ajouter » sont automatiquement intégrés dans tous les\n"
    "classements, statistiques et graphiques à la prochaine exécution de ces fonctionnalités.",
    ha="center",
    va="center",
    fontsize=7.5,
    color="#444444",
    bbox=dict(boxstyle="round,pad=0.4", fc="#F5F5F5", ec="#BDBDBD", lw=0.9),
)

plt.tight_layout(pad=0.5)
os.makedirs("output", exist_ok=True)
path = "output/diagramme_flux.png"
plt.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Diagramme sauvegardé : {path}")
