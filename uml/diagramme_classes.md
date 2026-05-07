# Diagramme de classes

Ce diagramme peut être rendu :
- **GitHub / GitLab** : rendu natif du bloc Mermaid ci-dessous
- **En ligne** : [mermaid.live](https://mermaid.live)
- **VS Code** : extension *Mermaid Preview*

Note : les attributs optionnels de `Match` (`season`, `winner`, `patch`, `surface`, `round`, `tourney_name`) sont omis pour la lisibilité.

---

## Version Mermaid

```mermaid
classDiagram

    %% ── Modèle ────────────────────────────────────────────────────────────────

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
        +passes : float
        +kills : int
        +dragons : int
        +barons : int
        +gold : float
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
        +classement_par(critere : str) list
        +run_menu(sport : Sport)$
    }

    %% ── Chargeurs ─────────────────────────────────────────────────────────────

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

    class GestionResultats {
        +sauvegarder(sport, date, eq1, eq2, s1, s2)$
        +charger(sport) list$
        +appliquer_a_equipe(equipe, nom) int$
        +appliquer_a_competition(comp) int$
        +lister(sport) list$
    }

    %% ── Visualisation ─────────────────────────────────────────────────────────

    class ClassementVisualizer {
        +visualiser_football(league_id, saison) str$
        +visualiser_basketball(season_type) str$
        +visualiser_lol() str$
        +visualiser_tennis(circuit, tournoi) str$
        +visualiser_volley(genre) str$
        +run_menu(sport_nom : str)$
    }

    class GraphiquesSport {
        +graph_foot_buts_journee(league_id, saison) str$
        +graph_foot_attaque_defense(league_id, saison) str$
        +graph_basket_dist_scores(season_type) str$
        +graph_basket_top_rebondeurs(season_type) str$
        +graph_lol_barres_groupees() str$
        +graph_lol_gold_winrate() str$
        +graph_lol_camembert_roles() str$
        +graph_tennis_top10(circuit) str$
        +graph_tennis_surface(circuit) str$
        +graph_tennis_atp_wta_taille() str$
        +graph_volley_sets_pays() str$
        +graph_volley_taille_pays() str$
        +graph_radar_equipe(sport, equipe_nom) str$
        +graph_comparaison_equipes(sport, nom1, nom2) str$
        +run_menu(sport_nom : str)$
    }

    %% ── Relations Modèle ──────────────────────────────────────────────────────

    Competition "1" *-- "0..*" Equipe : contient

    Sport ..> Match : paramètre run_menu
    Sport ..> Joueur : paramètre run_menu
    Sport ..> Equipe : paramètre run_menu
    Sport ..> Competition : paramètre run_menu
    Sport ..> MatchLoader : paramètre load_all_matches
    Sport ..> JoueurLoader : paramètre load_all_joueurs

    Match ..> MatchLoader : délègue run_menu à
    Joueur ..> JoueurLoader : délègue run_menu à
    Equipe ..> EquipeLoader : délègue run_menu à
    Competition ..> CompetitionLoader : délègue run_menu à

    %% ── Relations Chargeurs ───────────────────────────────────────────────────

    MatchLoader ..> GestionResultats : enrichit avec
    EquipeLoader ..> GestionResultats : enrichit avec
    CompetitionLoader ..> GestionResultats : enrichit avec

    MatchLoader ..> Match : crée
    JoueurLoader ..> Joueur : crée
    EquipeLoader ..> Equipe : met à jour
    CompetitionLoader ..> Competition : construit

    %% ── Relations Visualisation ───────────────────────────────────────────────

    GraphiquesSport ..> Competition : construit via _construire_competition_generique
    GraphiquesSport ..> Equipe : lit les statistiques
    GraphiquesSport ..> GestionResultats : appliquer_a_competition
    GraphiquesSport ..> ClassementVisualizer : délègue classement PNG à

    ClassementVisualizer ..> Competition : construit
    ClassementVisualizer ..> Equipe : lit les statistiques
    ClassementVisualizer ..> GestionResultats : appliquer_a_competition
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

### GestionResultats

Classe utilitaire à méthodes statiques qui persiste les nouveaux résultats dans
`data/resultats/nouveaux_matchs.csv`. Les loaders l'appellent automatiquement
pour intégrer ces résultats aux statistiques, classements et graphiques.

### GraphiquesSport & ClassementVisualizer

Deux classes du module `src/visualizer/` qui génèrent des fichiers PNG dans `output/` :
- `ClassementVisualizer` : tableaux de classement stylisés (style Ligue 1)
- `GraphiquesSport` : 26 graphiques statistiques (histogrammes, scatter, camemberts, radar…)

Toutes deux accèdent directement aux CSV via pandas et utilisent
`GestionResultats` pour intégrer les résultats manuels.
