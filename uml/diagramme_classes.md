# Diagramme de classes

Ce diagramme peut être rendu :
- **En ligne** : copier le bloc `@startuml` dans [plantuml.com/plantuml](https://www.plantuml.com/plantuml/uml)
- **VS Code** : extension *PlantUML*
- **GitHub** : via le bloc Mermaid ci-dessous (rendu natif)

Note : seuls les attributs principaux de `Match` sont représentés pour la lisibilité
(`season`, `winner`, `patch`, `surface`, `round`, `tourney_name` sont omis).

---

## Version Mermaid (rendu natif GitHub)

```mermaid
classDiagram

    %% ── Modèle ────────────────────────────────────────

    class Sport {
        +nom : str
        +__str__() str
    }

    class Match {
        +date : str
        +equipe_1 : str
        +equipe_2 : str
        +score_1 : float
        +score_2 : float
        +sport : str
        +run_menu(sport : Sport)$
    }

    class Joueur {
        +nom : str
        +sport : str
        +prenom : str
        +pseudo : str
        +equipe : str
        +position : str
        +taille : float
        +poids : float
        +pays : str
        +run_menu(sport : Sport)$
    }

    class Equipe {
        +nom : str
        +sport : str
        +matchs_joues : int
        +victoires : int
        +defaites : int
        +nuls : int
        +points : int
        +score_pour : float
        +score_contre : float
        +rebonds : float
        +kills : int
        +difference_score() float
        +winrate() float
        +ajouter_match(s1, s2, nul)
        +run_menu(sport : Sport)$
    }

    class Competition {
        +nom : str
        +sport : str
        +equipes : dict
        +ajouter_equipe(cle, equipe)
        +classement_par(*criteres) list
        +run_menu(sport : Sport)$
    }

    %% ── Chargeurs ─────────────────────────────────────

    class MatchLoader {
        -_loaders : dict
        +register(sport, loader)$
        +load_all_matches(sport : Sport) list
    }

    class JoueurLoader {
        -_loaders : dict
        +register(sport, loader)$
        +load_all_joueurs(sport : Sport) list
        +afficher_stats(joueurs, sport : Sport)
    }

    class EquipeLoader {
        -_loaders : dict
        +register(sport, loader)$
        +run(sport : Sport)
    }

    class CompetitionLoader {
        -_loaders : dict
        +register(sport, loader)$
        +run(sport : Sport)
    }

    class ResultatManager {
        +sauvegarder(sport, date, eq1, eq2, s1, s2)$
        +charger(sport) list$
        +appliquer_a_equipe(equipe, nom) int$
        +appliquer_a_competition(comp) int$
        +lister(sport) list$
    }

    %% ── Relations ─────────────────────────────────────

    Competition "1" *-- "0..*" Equipe : contient

    Sport ..> Match : paramètre de run_menu
    Sport ..> Joueur : paramètre de run_menu
    Sport ..> Equipe : paramètre de run_menu
    Sport ..> Competition : paramètre de run_menu
    Sport ..> MatchLoader : paramètre de load_all_matches
    Sport ..> JoueurLoader : paramètre de load_all_joueurs

    Match ..> MatchLoader : délègue run_menu à
    Joueur ..> JoueurLoader : délègue run_menu à
    Equipe ..> EquipeLoader : délègue run_menu à
    Competition ..> CompetitionLoader : délègue run_menu à

    MatchLoader ..> ResultatManager : enrichit avec
    EquipeLoader ..> ResultatManager : enrichit avec
    CompetitionLoader ..> ResultatManager : enrichit avec

    MatchLoader ..> Match : crée
    JoueurLoader ..> Joueur : crée
    EquipeLoader ..> Equipe : met à jour
    CompetitionLoader ..> Competition : construit
```

---

## Notes d'architecture

### Pattern Dispatcher + Registre

Chaque `Loader` applique le même pattern :

```
MatchLoader.register("football", FootballMatchLoader)
MatchLoader.register("basketball", BasketballMatchLoader)
...
MatchLoader().load_all_matches(sport)   ← dispatch automatique
```

Ajouter un nouveau sport revient à créer une classe dans le fichier loader concerné
et à appeler `register` — sans modifier aucune autre classe.

### ResultatManager

Classe utilitaire à méthodes statiques qui persiste les nouveaux résultats dans
`data/resultats/nouveaux_matchs.csv`. Les loaders l'appellent automatiquement
pour intégrer ces résultats aux statistiques et classements existants.
