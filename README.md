# Projet Informatique 1A — Gestion de compétitions sportives

## Présentation

Application en ligne de commande pour consulter et analyser des compétitions sportives multiples. Elle permet de rechercher des matchs, des joueurs et des équipes, de consulter les classements, de générer des graphiques statistiques et d'enregistrer de nouveaux résultats qui sont automatiquement intégrés à toutes les statistiques.

**Sports pris en charge :** Basketball · Football · League of Legends · Tennis · Volleyball

## Auteurs

Voir le fichier `AUTHORS.md`.

## Prérequis

Python 3.11 ou supérieur.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Utilisation

```bash
python __main__.py
```

L'application présente un menu interactif en deux niveaux : choix du sport, puis choix de la catégorie.

## Catégories disponibles

| Catégorie | Description |
|---|---|
| `match` | Recherche et statistiques de matchs (par équipe, date, score…) |
| `joueur` | Recherche et statistiques des joueurs (par nom, équipe, position…) |
| `equipe` | Statistiques d'une équipe (V/D/N, scores, stats avancées selon le sport) |
| `competition` | Classements ASCII de la compétition (par ligue, saison, type…) |
| `graphiques` | Génération de graphiques PNG et classements visuels |
| `ajouter` | Enregistrer manuellement le résultat d'un match |
| `historique` | Consulter les résultats enregistrés manuellement |

### Graphiques disponibles (`graphiques`)

| Touche | Description |
|---|---|
| `c` | Classement tableau PNG stylisé (style Ligue 1) |
| `1`–`N` | Graphiques statistiques propres au sport sélectionné |
| `7` | Radar spider chart des performances d'une équipe |
| `8` | Comparaison côte à côte de deux équipes |

Les graphiques générés sont sauvegardés dans `output/`.

**Exemples de graphiques disponibles :**
- Football : buts par journée, distribution des scores, attaque vs défense, pyramide des âges
- Basketball : distribution des points, top rebondeurs, scatter pts marqués/encaissés
- LoL : kills/dragons/barons par équipe, gold vs winrate, répartition des rôles
- Tennis : top 10 ATP/WTA, répartition par surface, distribution des tailles
- Volleyball : sets gagnés par pays, taille moyenne hommes/femmes

## Intégration automatique des résultats

Les résultats ajoutés via `ajouter` sont écrits dans `data/resultats/nouveaux_matchs.csv` et **automatiquement intégrés** dans tous les classements, statistiques et graphiques à la prochaine consultation via `GestionResultats.appliquer_a_competition()`.

## Structure du projet

```
projet_info_template/
├── __main__.py                  ← point d'entrée, menus interactifs
├── requirements.txt
├── data/
│   ├── basketball/              ← game.csv · team.csv · player.csv
│   ├── football/                ← match.csv · team.csv · league.csv · country.csv · player.csv
│   ├── LOL/                     ← match.csv · team.csv · player.csv · coach.csv
│   ├── tennis/                  ← atp/wta matches & players 2024
│   ├── volley/                  ← match_men/women · country · player_men/women
│   └── resultats/               ← nouveaux_matchs.csv (ajouts manuels)
├── output/                      ← graphiques PNG générés
├── src/
│   ├── sport.py
│   ├── Model/
│   │   ├── Match.py
│   │   ├── Joueur.py
│   │   ├── Equipe.py            ← stats communes + stats sport-spécifiques
│   │   └── Competition.py
│   ├── loader/
│   │   ├── MatchLoader.py       ← dispatcher + loaders par sport
│   │   ├── JoueurLoader.py
│   │   ├── EquipeLoader.py
│   │   ├── CompetitionLoader.py
│   │   └── GestionResultats.py  ← persistance CSV des nouveaux résultats
│   ├── visualizer/
│   │   ├── ClassementVisualizer.py  ← tableaux de classement PNG (style Ligue 1)
│   │   └── GraphiquesSport.py       ← 26 graphiques statistiques matplotlib
│   ├── Common/
│   │   └── utils.py
│   └── Parsers/
│       └── parse_csv.py
├── test/
│   ├── Common/
│   ├── loader/
│   └── Model/
└── uml/
    ├── diagramme_classes.md          ← diagramme de classes Mermaid
    └── sous_menus/                   ← un diagramme Mermaid par sous-menu
        ├── match.md
        ├── joueur.md
        ├── equipe.md
        ├── competition.md
        ├── graphiques.md
        ├── ajouter.md
        └── historique.md
```

## Architecture

Le projet applique un **pattern Dispatcher + Registre** pour chaque type de données :

```python
MatchLoader.register("football", FootballMatchLoader)
MatchLoader.register("basketball", BasketballMatchLoader)
# ...
MatchLoader().load_all_matches(sport)  # dispatch automatique
```

Ajouter un nouveau sport revient à créer un loader spécifique et à l'enregistrer, sans modifier aucune autre classe.

## Tests

```bash
pytest
pytest --cov=src --cov-report=term-missing   # avec couverture
```

## Qualité du code

```bash
flake8 src/    # linting
black src/     # formatage
```

## Dépendances

| Paquet       | Version | Usage |
|---|---|---|
| `pandas`     | 2.3.3   | Lecture CSV, agrégations |
| `matplotlib` | —       | Génération des graphiques PNG |
| `pytest`     | 9.0.3   | Tests unitaires |
| `pytest-cov` | 7.1.0   | Couverture de tests |
| `black`      | 25.1.0  | Formatage du code |
