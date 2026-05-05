# Projet Informatique 1A — Gestion de compétitions sportives

## Présentation

Ce projet propose une application en ligne de commande pour gérer des compétitions sportives. Elle permet de consulter les résultats et les statistiques des matchs, des joueurs, des équipes et des classements, ainsi qu'enregistrer de nouveaux résultats qui mettent à jour automatiquement les statistiques.

Les sports pris en charge sont : basketball, football, League of Legends, tennis et volleyball.

## Auteurs

Voir le fichier `AUTHORS.md`.

## Prérequis

Python 3.11 ou supérieur.

## Installation

Créer et activer un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

L'application présente un menu interactif. L'utilisateur choisit d'abord un sport, puis une catégorie parmi les suivantes :

- `match` : recherche et statistiques de matchs
- `joueur` : recherche et statistiques des joueurs
- `equipe` : statistiques d'une équipe
- `competition` : classements de la compétition
- `ajouter` : enregistrer le résultat d'un nouveau match
- `historique` : consulter les résultats enregistrés manuellement

Les résultats ajoutés sont sauvegardés dans `data/resultats/nouveaux_matchs.csv` et sont automatiquement intégrés aux statistiques et aux classements lors de la prochaine consultation.

## Structure du projet

```
projet_info_template/
├── main.py
├── requirements.txt
├── pyproject.toml
├── data/
│   ├── basketball/
│   ├── football/
│   ├── LOL/
│   ├── tennis/
│   ├── volley/
│   └── resultats/
├── src/
│   ├── sport.py
│   ├── Model/
│   ├── loader/
│   └── Common/
└── test/
```

## Tests

Exécuter les tests :

```bash
pytest
```

Mesurer la couverture du code :

```bash
pytest --cov=src --cov-report=term-missing
```

## Qualité du code

Linter utilisé : Flake8

```bash
flake8 src/
```

Formatter utilisé : Black

```bash
black src/
```

## Documentation

Les docstrings suivent le style NumPy.

## Dépendances

| Paquet     | Version |
|------------|---------|
| pandas     | 2.3.3   |
| pytest     | 9.0.3   |
| pytest-cov | 7.1.0   |
| black      | 25.1.0  |
