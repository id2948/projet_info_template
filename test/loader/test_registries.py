"""Vérifie que tous les loaders sont correctement enregistrés pour les 5 sports."""
import main  # déclenche l'enregistrement de tous les loaders

from src.loader.MatchLoader import MatchLoader
from src.loader.JoueurLoader import JoueurLoader
from src.loader.EquipeMenuLoader import EquipeMenuLoader
from src.loader.CompetitionMenuLoader import CompetitionMenuLoader
from src.loader.JoueurStatsLoader import JoueurStatsLoader

SPORTS = {"basketball", "football", "LOL", "tennis", "volley"}


def test_match_loaders_tous_enregistres():
    assert set(MatchLoader._loaders.keys()) == SPORTS


def test_joueur_loaders_tous_enregistres():
    assert set(JoueurLoader._loaders.keys()) == SPORTS


def test_equipe_loaders_tous_enregistres():
    assert set(EquipeMenuLoader._loaders.keys()) == SPORTS


def test_competition_loaders_tous_enregistres():
    assert set(CompetitionMenuLoader._loaders.keys()) == SPORTS


def test_joueur_stats_loaders_tous_enregistres():
    assert set(JoueurStatsLoader._loaders.keys()) == SPORTS
