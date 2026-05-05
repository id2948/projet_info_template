# Projet Info 1A 2025 — Gestion de compétitions sportives

## Objectif

Application Python en ligne de commande permettant de gérer des compétitions sportives : consulter les résultats et statistiques des matchs, joueurs, équipes et classements ; enregistrer de nouveaux résultats qui mettent à jour automatiquement les statistiques.

Sports supportés : basketball, football, League of Legends, tennis, volleyball.

## Version Python

Python **3.11** ou supérieur.

## Installation

Créer et activer un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer l'application

```bash
python main.py
```

L'application propose un menu interactif. Choisissez un sport puis une catégorie :

| Catégorie   | Description |
|-------------|-------------|
| `match`     | Recherche et statistiques de matchs |
| `joueur`    | Recherche et statistiques des joueurs |
| `equipe`    | Statistiques d'une équipe |
| `competition` | Classements de la compétition |
| `ajouter`   | Enregistrer le résultat d'un nouveau match |
| `historique` | Consulter les résultats enregistrés |

Les résultats ajoutés via `ajouter` sont sauvegardés dans `data/resultats/nouveaux_matchs.csv` et pris en compte automatiquement dans toutes les statistiques et classements.

## Structure du projet

```
projet_info_template/
├── main.py                        ← point d'entrée
├── requirements.txt               ← dépendances avec versions exactes
├── pyproject.toml                 ← config linter, formatter et tests
├── data/
│   ├── basketball/ football/ LOL/ tennis/ volley/   ← données CSV
│   └── resultats/nouveaux_matchs.csv                ← résultats ajoutés
├── src/
│   ├── sport.py
│   ├── Model/       ← Match, Joueur, Equipe, Competition
│   ├── loader/      ← chargement CSV et gestion des résultats
│   └── Common/      ← utilitaires
└── test/            ← tests pytest
```

## Tests

Lancer les tests :

```bash
pytest
```

Lancer les tests avec la couverture :

```bash
pytest --cov=src --cov-report=term-missing
```

## Linter

Linter utilisé : **Flake8**

```bash
flake8 src/
```

## Formatter

Formatter utilisé : **Black**

```bash
black src/
```

## Style de documentation

Les docstrings suivent le style **NumPy**.

## Dépendances

| Paquet | Version | Usage |
|--------|---------|-------|
| pandas | 2.3.3 | Chargement des CSV |
| pytest | 9.0.3 | Tests unitaires |
| pytest-cov | 7.1.0 | Couverture des tests |
| black | 25.1.0 | Formatage du code |

## Sports supportés

| Sport | Matchs | Joueurs | Équipes | Compétition | Ajout résultats |
|-------|--------|---------|---------|-------------|-----------------|
| Basketball | ✅ | ✅ | ✅ | ✅ | ✅ |
| Football | ✅ | ✅ | ✅ | ✅ | ✅ |
| LoL | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tennis | ✅ | ✅ | ✅ | ✅ | ✅ |
| Volleyball | ✅ | ✅ | ✅ | ✅ | ✅ |
