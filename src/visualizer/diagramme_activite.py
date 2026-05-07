"""Diagramme d'activité UML — swim lanes Utilisateur / Application."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.patches as mpatches
import numpy as np
import os

BG  = "#FFFFFF"
EC  = "#333333"   # bords boîtes / flèches
FC  = "#FFFFFF"   # fill activités
TXT = "#111111"
LW  = 1.3

# ── Dimensions swim lanes ─────────────────────────────────────────────────────
FIG_W, FIG_H = 11, 18
LANE_L = 0.5    # x gauche du diagramme
LANE_R = 10.5   # x droit
MID    = 5.5    # séparation des deux couloirs
L_CX   = (LANE_L + MID) / 2    # centre couloir Utilisateur
R_CX   = (MID + LANE_R) / 2    # centre couloir Application

# ── Helpers ───────────────────────────────────────────────────────────────────

def activity(ax, cx, cy, w, h, texte, fs=8.5):
    """Rectangle arrondi = activité UML."""
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.06,rounding_size=0.14",
        facecolor=FC, edgecolor=EC, linewidth=LW, zorder=3,
    ))
    ax.text(cx, cy, texte, ha="center", va="center",
            fontsize=fs, color=TXT, zorder=4, linespacing=1.4)

def decision(ax, cx, cy, size=0.38, texte="", fs=7.5):
    """Losange = décision UML."""
    dx, dy = size, size * 0.60
    pts = np.array([[cx, cy+dy], [cx+dx, cy], [cx, cy-dy], [cx-dx, cy]])
    ax.add_patch(Polygon(pts, closed=True,
                         facecolor=FC, edgecolor=EC, linewidth=LW, zorder=3))
    if texte:
        ax.text(cx, cy, texte, ha="center", va="center",
                fontsize=fs, color=TXT, zorder=4)

def start_node(ax, cx, cy, r=0.18):
    ax.add_patch(plt.Circle((cx, cy), r, color=EC, zorder=5))

def end_node(ax, cx, cy, r=0.18):
    ax.add_patch(plt.Circle((cx, cy), r, color=EC, zorder=5))
    ax.add_patch(plt.Circle((cx, cy), r + 0.10,
                             color="none", ec=EC, lw=LW+0.5, zorder=5))

def arrow(ax, x1, y1, x2, y2, rad=0.0, lw=LW):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>", color=EC, lw=lw,
                    connectionstyle=f"arc3,rad={rad}",
                    mutation_scale=11,
                ), zorder=2)

def label(ax, x, y, texte, fs=7.5, ha="left", color="#444444"):
    ax.text(x, y, texte, ha=ha, va="center", fontsize=fs, color=color, zorder=5,
            bbox=dict(boxstyle="round,pad=0.10", fc=BG, ec="none", alpha=0.9))

def hline(ax, x1, x2, y, lw=LW):
    ax.plot([x1, x2], [y, y], color=EC, lw=lw, zorder=2)

def vline(ax, x, y1, y2, lw=LW, ls="-"):
    ax.plot([x, x], [y1, y2], color=EC, lw=lw, ls=ls, zorder=2)

# ══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(FIG_W / 2, 17.55,
        "Diagramme d'activité",
        ha="center", va="center", fontsize=16, fontweight="bold", color=TXT)

# ── Swim lane headers + bordure + séparateur ──────────────────────────────────
HEADER_Y = 17.10
HEADER_H = 0.60

# Fond entête gauche
ax.add_patch(FancyBboxPatch(
    (LANE_L, HEADER_Y - HEADER_H/2), MID - LANE_L, HEADER_H,
    boxstyle="square,pad=0",
    facecolor="#EEEEEE", edgecolor=EC, linewidth=LW, zorder=2
))
# Fond entête droite
ax.add_patch(FancyBboxPatch(
    (MID, HEADER_Y - HEADER_H/2), LANE_R - MID, HEADER_H,
    boxstyle="square,pad=0",
    facecolor="#EEEEEE", edgecolor=EC, linewidth=LW, zorder=2
))

ax.text(L_CX, HEADER_Y, "Utilisateur",
        ha="center", va="center", fontsize=11, fontweight="bold", color=TXT, zorder=3)
ax.text(R_CX, HEADER_Y, "Application",
        ha="center", va="center", fontsize=11, fontweight="bold", color=TXT, zorder=3)

# Bordure du diagramme
BOT_Y = 0.35
ax.add_patch(mpatches.Rectangle(
    (LANE_L, BOT_Y), LANE_R - LANE_L, HEADER_Y + HEADER_H/2 - BOT_Y,
    fill=False, edgecolor=EC, lw=LW, zorder=1
))
# Séparateur vertical
vline(ax, MID, BOT_Y, HEADER_Y - HEADER_H/2, lw=LW)

# ══════════════════════════════════════════════════════════════════════════════
# NŒUDS ET FLÈCHES — de haut en bas
# ══════════════════════════════════════════════════════════════════════════════

AW = 3.8    # largeur activité
AH = 0.58   # hauteur activité

# ── A0 : Nœud initial (Application) ──────────────────────────────────────────
Y_INIT = 16.35
start_node(ax, R_CX, Y_INIT)

# ── A1 : Charger données CSV (Application) ───────────────────────────────────
Y1 = 15.55
arrow(ax, R_CX, Y_INIT - 0.18, R_CX, Y1 + AH/2)
activity(ax, R_CX, Y1, AW, AH, "Charger les données CSV\n(pandas · 5 sports)", fs=8.5)

# ── A2 : Afficher menu sport (Application) ───────────────────────────────────
Y2 = 14.55
arrow(ax, R_CX, Y1 - AH/2, R_CX, Y2 + AH/2)
activity(ax, R_CX, Y2, AW, AH, "Afficher le menu sport\n(basketball · football · LOL · tennis · volley)", fs=7.8)

# ── Flèche Application → Utilisateur (demande saisie sport) ──────────────────
Y_CROSS1 = 13.88
arrow(ax, R_CX, Y2 - AH/2, R_CX, Y_CROSS1)
hline(ax, L_CX, R_CX, Y_CROSS1)
arrow(ax, L_CX + 0.01, Y_CROSS1, L_CX, Y_CROSS1 - 0.01)

# ── A3 : Saisie sport (Utilisateur) ──────────────────────────────────────────
Y3 = 13.30
arrow(ax, L_CX, Y_CROSS1, L_CX, Y3 + AH/2)
activity(ax, L_CX, Y3, AW, AH,
         "Saisit un sport\nou « q » pour quitter", fs=8.5)

# ── Flèche Utilisateur → Application ─────────────────────────────────────────
Y_CROSS2 = 12.63
arrow(ax, L_CX, Y3 - AH/2, L_CX, Y_CROSS2)
hline(ax, L_CX, R_CX, Y_CROSS2)
arrow(ax, R_CX - 0.01, Y_CROSS2, R_CX, Y_CROSS2 - 0.01)

# ── D1 : Décision — sport valide ? ───────────────────────────────────────────
Y_D1 = 12.15
arrow(ax, R_CX, Y_CROSS2, R_CX, Y_D1 + 0.38)
decision(ax, R_CX, Y_D1, texte="")
label(ax, R_CX + 0.50, Y_D1, "sport\nreconnu ?", fs=7.5, ha="left")

# Branche NON → retour affichage menu (boucle gauche)
vline(ax, R_CX - 1.50, Y_D1, Y2 - AH/2, lw=LW, ls="-")
hline(ax, R_CX - 1.50, R_CX - 0.38, Y_D1)
hline(ax, R_CX - 1.50, R_CX, Y2 - AH/2)
arrow(ax, R_CX, Y2 - AH/2 + 0.01, R_CX, Y2 - AH/2)
label(ax, R_CX - 2.55, Y_D1, "Non", fs=7.8, ha="left", color="#B71C1C")

# Branche OUI ↓
Y_OUI = Y_D1 - 0.38
label(ax, R_CX + 0.08, (Y_OUI + Y_D1 - 0.6) / 2, "Oui", fs=7.8, color="#1B5E20")

# ── A4 : Afficher menu catégorie (Application) ───────────────────────────────
Y4 = 11.18
arrow(ax, R_CX, Y_D1 - 0.38, R_CX, Y4 + AH/2)
activity(ax, R_CX, Y4, AW, AH,
         "Afficher le menu catégorie\n(match · joueur · equipe · competition\n"
         "graphiques · ajouter · historique)", fs=7.5)

# ── Flèche Application → Utilisateur ─────────────────────────────────────────
Y_CROSS3 = 10.38
arrow(ax, R_CX, Y4 - AH/2, R_CX, Y_CROSS3)
hline(ax, L_CX, R_CX, Y_CROSS3)
arrow(ax, L_CX + 0.01, Y_CROSS3, L_CX, Y_CROSS3 - 0.01)

# ── A5 : Saisie catégorie + paramètres (Utilisateur) ─────────────────────────
Y5 = 9.60
arrow(ax, L_CX, Y_CROSS3, L_CX, Y5 + AH/2)
activity(ax, L_CX, Y5, AW, AH + 0.15,
         "Saisit une catégorie et\nles paramètres associés\n"
         "(ligue, saison, circuit, équipe…)", fs=8.0)

# Branche RETOUR → boucle vers menu sport
Y_RET = 9.20
vline(ax, L_CX - 1.45, Y5 - AH/2, Y2)
hline(ax, L_CX - 1.45, L_CX - AW/2, Y5)
arrow(ax, R_CX, Y2 + 0.01, R_CX, Y2)
label(ax, 0.55, 9.60, "« retour »\n→ menu sport", fs=7.2, ha="left", color="#546E7A")

# ── Flèche Utilisateur → Application ─────────────────────────────────────────
Y_CROSS4 = 8.80
arrow(ax, L_CX, Y5 - (AH + 0.15)/2, L_CX, Y_CROSS4)
hline(ax, L_CX, R_CX, Y_CROSS4)
arrow(ax, R_CX - 0.01, Y_CROSS4, R_CX, Y_CROSS4 - 0.01)

# ── A6 : Charger, traiter, agréger (Application) ─────────────────────────────
Y6 = 8.02
arrow(ax, R_CX, Y_CROSS4, R_CX, Y6 + AH/2)
activity(ax, R_CX, Y6, AW, AH,
         "Charger et traiter les données\ndu sport sélectionné\n"
         "(pandas · GestionResultats)", fs=7.8)

# ── Flèche Application → Utilisateur (choix rendu) ───────────────────────────
Y_CROSS5 = 7.22
arrow(ax, R_CX, Y6 - AH/2, R_CX, Y_CROSS5)
hline(ax, L_CX, R_CX, Y_CROSS5)
arrow(ax, L_CX + 0.01, Y_CROSS5, L_CX, Y_CROSS5 - 0.01)

# ── A7 : Choix du rendu (Utilisateur) ────────────────────────────────────────
Y7 = 6.50
arrow(ax, L_CX, Y_CROSS5, L_CX, Y7 + AH/2)
activity(ax, L_CX, Y7, AW, AH,
         "Choisit le type de rendu\n(affichage terminal\nou graphique PNG)", fs=8.0)

# ── Flèche Utilisateur → Application ─────────────────────────────────────────
Y_CROSS6 = 5.88
arrow(ax, L_CX, Y7 - AH/2, L_CX, Y_CROSS6)
hline(ax, L_CX, R_CX, Y_CROSS6)
arrow(ax, R_CX - 0.01, Y_CROSS6, R_CX, Y_CROSS6 - 0.01)

# ── A8 : Produire le résultat (Application) ──────────────────────────────────
Y8 = 5.10
arrow(ax, R_CX, Y_CROSS6, R_CX, Y8 + AH/2)
activity(ax, R_CX, Y8, AW, AH,
         "Générer et fournir le résultat\n(classement · stats · graphique PNG\n"
         "· sauvegarde CSV)", fs=7.8)

# ── D2 : Décision — continuer ou quitter ? ───────────────────────────────────
Y_D2 = 4.15
arrow(ax, R_CX, Y8 - AH/2, R_CX, Y_D2 + 0.38)
decision(ax, R_CX, Y_D2)
label(ax, R_CX + 0.50, Y_D2, "continuer ?", fs=7.5, ha="left")

# Branche OUI → boucle vers afficher menu catégorie
vline(ax, LANE_R - 0.35, Y_D2, Y4)
hline(ax, R_CX + 0.38, LANE_R - 0.35, Y_D2)
hline(ax, R_CX + AW/2, LANE_R - 0.35, Y4)
arrow(ax, R_CX + AW/2 - 0.01, Y4, R_CX + AW/2, Y4)
label(ax, LANE_R - 0.30, (Y_D2 + Y4) / 2, "Oui", fs=7.8, ha="left", color="#1B5E20")

# Branche NON ↓
label(ax, R_CX + 0.08, (Y_D2 - 0.38 + Y_D2 - 0.6) / 2,
      "Non", fs=7.8, color="#B71C1C")

# ── A9 : Au revoir (Application) ─────────────────────────────────────────────
Y9 = 3.30
arrow(ax, R_CX, Y_D2 - 0.38, R_CX, Y9 + AH/2)
activity(ax, R_CX, Y9, AW, AH,
         "Afficher le message de fin\n« Au revoir »", fs=8.5)

# ── Nœud final (Application) ─────────────────────────────────────────────────
Y_END = 2.55
arrow(ax, R_CX, Y9 - AH/2, R_CX, Y_END + 0.28)
end_node(ax, R_CX, Y_END)

# ══════════════════════════════════════════════════════════════════════════════

plt.tight_layout(pad=0.3)
os.makedirs("output", exist_ok=True)
path = "output/diagramme_activite.png"
plt.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Diagramme sauvegardé : {path}")
