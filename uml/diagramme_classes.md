# Diagramme de classes

Ce diagramme peut être rendu :
- **En ligne** : copier le bloc `@startuml` dans [plantuml.com/plantuml](https://www.plantuml.com/plantuml/uml)
- **VS Code** : extension *PlantUML*
- **GitHub** : via le bloc Mermaid ci-dessous (rendu natif)

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
        +season : str
        +winner : str
        +run_menu(sport)$
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
        +main : str
        +run_menu(sport)$
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
        +dragons : int
        +difference_score() float
        +winrate() float
        +ajouter_match(s1, s2, nul)
        +run_menu(sport)$
    }

    class Competition {
        +nom : str
        +sport : str
        +equipes : dict
        +ajouter_equipe(cle, equipe)
        +classement_par(*criteres) list
        +run_menu(sport)$
    }

    %% ── Chargeurs ─────────────────────────────────────

    class MatchLoader {
        -_loaders : dict
        +register(sport, loader)$
        +load_all_matches(sport) list
    }

    class JoueurLoader {
        -_loaders : dict
        +register(sport, loader)$
        +load_all_joueurs(sport) list
        +afficher_stats(joueurs, sport)
    }

    class EquipeLoader {
        -_loaders : dict
        +register(sport, loader)$
        +run(sport)
    }

    class CompetitionLoader {
        -_loaders : dict
        +register(sport, loader)$
        +run(sport)
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

    Match ..> MatchLoader : délègue à
    Joueur ..> JoueurLoader : délègue à
    Equipe ..> EquipeLoader : délègue à
    Competition ..> CompetitionLoader : délègue à

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

Chaque `Loader` (MatchLoader, JoueurLoader, EquipeLoader, CompetitionLoader) applique le même
pattern :

```
Loader.register("football", FootballLoader)   ← à l'import du module
Loader.register("basketball", BasketballLoader)
...
Loader().run(sport)   ← dispatch automatique selon le sport
```

Ajouter un sport revient à créer une classe dans le fichier loader concerné
et à appeler `register` — sans modifier aucune autre classe.

### ResultatManager

Classe utilitaire (méthodes statiques) qui gère la persistance des nouveaux
résultats dans `data/resultats/nouveaux_matchs.csv`. Les loaders l'appellent
automatiquement pour intégrer les résultats ajoutés manuellement aux
statistiques et classements existants.
