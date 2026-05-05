"""Vérifie que tous les loaders sont correctement enregistrés pour les 5 sports."""
import src.loader.MatchLoader
import src.loader.JoueurLoader
import src.loader.EquipeLoader
import src.loader.CompetitionLoader

from src.loader.MatchLoader import MatchLoader
from src.loader.JoueurLoader import JoueurLoader
from src.loader.EquipeLoader import EquipeLoader
from src.loader.CompetitionLoader import CompetitionLoader

SPORTS = {"basketball", "football", "LOL", "tennis", "volley"}


def test_match_loaders_tous_enregistres():
    assert set(MatchLoader._loaders.keys()) == SPORTS


def test_joueur_loaders_tous_enregistres():
    assert set(JoueurLoader._loaders.keys()) == SPORTS


def test_equipe_loaders_tous_enregistres():
    assert set(EquipeLoader._loaders.keys()) == SPORTS


def test_competition_loaders_tous_enregistres():
    assert set(CompetitionLoader._loaders.keys()) == SPORTS


def test_joueur_loaders_ont_afficher_stats():
    """Vérifie que chaque loader joueur expose bien la méthode afficher_stats."""
    for sport, loader_cls in JoueurLoader._loaders.items():
        assert hasattr(loader_cls(), "afficher_stats"), f"{sport}: afficher_stats manquante"
