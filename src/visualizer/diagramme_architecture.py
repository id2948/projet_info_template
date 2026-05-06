"""Génère le diagramme d'architecture de l'application sous forme de PNG."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# ── Palette ────────────────────────────────────────────────────────────────────
C_CLI      = "#1a1a2e"   # bleu nuit — interface
C_MODEL    = "#16213e"   # bleu foncé — modèles
C_LOADER   = "#0f3460"   # bleu moyen — loaders
C_VIZ      = "#533483"   # violet — visualiseur
C_ANALYSIS = "#2d6a4f"   # vert — analyse
C_DATA     = "#b5451b"   # rouille — données
C_SPORT    = "#e94560"   # rouge — sport dispatcher

FG         = "#ffffff"
ARROW_COL  = "#555555"
BG         = "#f4f4f8"

def box(ax, x, y, w, h, label, sublabel=None, color=C_MODEL, fontsize=10, radius=0.012):
    """Dessine une boîte arrondie avec titre et sous-titre optionnel."""
    rect = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        linewidth=1.4, edgecolor="#333333",
        facecolor=color, zorder=3,
    )
    ax.add_patch(rect)
    ty = y + (h * 0.12 if sublabel else 0)
    ax.text(x, ty, label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color=FG, zorder=4)
    if sublabel:
        ax.text(x, y - h * 0.22, sublabel, ha="center", va="center",
                fontsize=7.5, color="#cccccc", zorder=4, style="italic")

def arrow(ax, x1, y1, x2, y2, label="", bidirectional=False):
    """Dessine une flèche entre deux points."""
    style = "<->" if bidirectional else "->"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle=style, color=ARROW_COL,
                                 lw=1.5, connectionstyle="arc3,rad=0.0"),
                 zorder=2)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.01, my, label, ha="left", va="center",
                fontsize=7, color=ARROW_COL, zorder=5)

def dashed_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", color=ARROW_COL,
                                 lw=1.2, linestyle="dashed",
                                 connectionstyle="arc3,rad=0.0"),
                 zorder=2)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.01, my, label, ha="left", va="center",
                fontsize=7, color=ARROW_COL, zorder=5)

def separator(ax, y, label, x0=0.01, x1=0.99):
    ax.axhline(y=y, xmin=x0, xmax=x1, color="#cccccc", lw=0.8, linestyle="--", zorder=1)
    ax.text(0.995, y + 0.005, label, ha="right", va="bottom",
            fontsize=7, color="#999999", fontstyle="italic")


fig, ax = plt.subplots(figsize=(18, 13))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(0.5, 0.965, "Architecture — Application Sportive",
        ha="center", va="center", fontsize=17, fontweight="bold", color=C_CLI)
ax.text(0.5, 0.945, "Résultats & Statistiques  |  Football · Basketball · LoL · Tennis · Volleyball",
        ha="center", va="center", fontsize=9, color="#555555")

# ── Couche 1 : Interface CLI ───────────────────────────────────────────────────
separator(ax, 0.91, "COUCHE INTERFACE")
box(ax, 0.5, 0.875, 0.30, 0.055, "__main__.py",
    "Boucle principale · menu sport · menu catégorie", color=C_CLI, fontsize=11)

# ── Couche 2 : Sport ──────────────────────────────────────────────────────────
separator(ax, 0.825, "COUCHE DOMAINE")
box(ax, 0.5, 0.795, 0.18, 0.045, "Sport",
    "Identifiant du sport", color=C_SPORT, fontsize=10)

# ── Couche 3 : Modèles ────────────────────────────────────────────────────────
separator(ax, 0.755, "COUCHE MODÈLE")
models = [
    (0.13, "Competition", "nom, sport\nequipes: dict"),
    (0.33, "Equipe", "stats communes\n+ stats sport-spécifiques"),
    (0.53, "Match", "date, scores\noptions sport"),
    (0.73, "Joueur", "nom, sport\nstatistiques"),
]
for xm, nom, sub in models:
    box(ax, xm, 0.700, 0.175, 0.075, nom, sub, color=C_MODEL, fontsize=9.5)

# Competition → Equipe
arrow(ax, 0.22, 0.700, 0.24, 0.700, "contient →")

# ── Couche 4 : Loaders ────────────────────────────────────────────────────────
separator(ax, 0.645, "COUCHE LOADER / DISPATCHER")

# Dispatcher central
box(ax, 0.50, 0.608, 0.28, 0.055,
    "CompetitionLoader  |  EquipeLoader",
    "MatchLoader  |  JoueurLoader  |  GestionResultats",
    color=C_LOADER, fontsize=9)

# Loaders sport-spécifiques
sports_loaders = [
    (0.09, "Football\nLoader"),
    (0.25, "Basketball\nLoader"),
    (0.41, "LoL\nLoader"),
    (0.59, "Tennis\nLoader"),
    (0.75, "Volley\nLoader"),
    (0.91, "Gestion\nRésultats"),
]
for xs, lbl in sports_loaders:
    color = C_DATA if "Résultats" in lbl else C_LOADER
    box(ax, xs, 0.533, 0.135, 0.055, lbl, color=color, fontsize=8.5)
    arrow(ax, xs, 0.561, xs, 0.575)

# ── Couche 5 : Visualiseur & Analyse ─────────────────────────────────────────
separator(ax, 0.480, "COUCHE VISUALISATION & ANALYSE")
box(ax, 0.25, 0.437, 0.35, 0.060,
    "ClassementVisualizer",
    "football · basketball · LoL · tennis · volley\n→ génère output/classement_*.png",
    color=C_VIZ, fontsize=9.5)

box(ax, 0.72, 0.437, 0.30, 0.060,
    "Analysis",
    "homemade/  ·  pandas/\nGoatFinder, statistiques avancées",
    color=C_ANALYSIS, fontsize=9.5)

# ── Couche 6 : Données CSV ────────────────────────────────────────────────────
separator(ax, 0.380, "COUCHE DONNÉES (CSV)")
data_files = [
    (0.09,  "football/",   "match · team\nleague · country"),
    (0.25,  "basketball/", "game · team\nplayer"),
    (0.41,  "LOL/",        "match · team\nplayer · coach"),
    (0.59,  "tennis/",     "atp/wta matches\natp/wta players"),
    (0.75,  "volley/",     "match_men/women\ncountry · player"),
    (0.91,  "resultats/",  "nouveaux_matchs.csv\n(ajouts manuels)"),
]
for xd, nom, sub in data_files:
    c = C_DATA if "resultats" in nom else "#8b3a0f"
    box(ax, xd, 0.300, 0.155, 0.090, nom, sub, color=c, fontsize=8.5)

# ── Couche 7 : Sorties ────────────────────────────────────────────────────────
separator(ax, 0.220, "SORTIES")
box(ax, 0.25, 0.170, 0.28, 0.060,
    "Terminal (stdout)",
    "classements ASCII · stats · historique\nrecherches joueurs / matchs",
    color="#444444", fontsize=9)
box(ax, 0.70, 0.170, 0.28, 0.060,
    "output/*.png",
    "tableaux de classement stylisés\npar sport et compétition",
    color=C_VIZ, fontsize=9)

# ── Flèches verticales principales ───────────────────────────────────────────
# CLI → Sport
arrow(ax, 0.5, 0.848, 0.5, 0.818)
# Sport → Modèles (via CLI)
arrow(ax, 0.50, 0.772, 0.50, 0.738)
# CLI → Loaders
arrow(ax, 0.44, 0.848, 0.44, 0.636, "run_menu(sport)")
# Loaders → Modèles (flèche gauche)
dashed_arrow(ax, 0.36, 0.608, 0.30, 0.740, "instancie")
# Loaders → Data
arrow(ax, 0.50, 0.580, 0.50, 0.348, "read_csv()")
# Loaders → Gestion (bidirectionnel)
dashed_arrow(ax, 0.82, 0.580, 0.88, 0.562)
# CLI → Visualiseur
arrow(ax, 0.38, 0.848, 0.26, 0.468, "visualiser")
# CLI → Analysis
dashed_arrow(ax, 0.58, 0.848, 0.71, 0.468, "analyse")
# Visualiseur → Output PNG
arrow(ax, 0.25, 0.407, 0.61, 0.200, "savefig()")
# Terminal output ← CLI
arrow(ax, 0.48, 0.848, 0.29, 0.200, "print()")
# GestionResultats → Data (écriture)
dashed_arrow(ax, 0.91, 0.506, 0.91, 0.348, "write CSV")

# ── Légende ───────────────────────────────────────────────────────────────────
legend_items = [
    (C_CLI,      "Interface / Point d'entrée"),
    (C_SPORT,    "Couche domaine (Sport)"),
    (C_MODEL,    "Modèles métier"),
    (C_LOADER,   "Loaders / Dispatchers"),
    (C_VIZ,      "Visualiseur"),
    (C_ANALYSIS, "Analyse"),
    (C_DATA,     "Données CSV"),
]
handles = [mpatches.Patch(facecolor=c, edgecolor="#333", label=l) for c, l in legend_items]
ax.legend(handles=handles, loc="lower center", ncol=len(legend_items),
          fontsize=8, frameon=True, edgecolor="#cccccc", facecolor=BG,
          bbox_to_anchor=(0.5, 0.005))

plt.tight_layout(pad=0.3)

os.makedirs("output", exist_ok=True)
path = "output/diagramme_architecture.png"
plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Diagramme sauvegardé : {path}")
