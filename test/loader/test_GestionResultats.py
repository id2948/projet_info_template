import os
import pytest
import src.loader.GestionResultats as gr_module
from src.loader.GestionResultats import GestionResultats
from src.Model.Equipe import Equipe
from src.Model.Competition import Competition

FICHIER_TEST = "test/loader/test_resultats_temp.csv"


@pytest.fixture
def fichier_temp():
    """Redirige FICHIER_RESULTATS vers un fichier temporaire pour chaque test."""
    ancien = gr_module.FICHIER_RESULTATS
    gr_module.FICHIER_RESULTATS = FICHIER_TEST
    yield
    gr_module.FICHIER_RESULTATS = ancien
    if os.path.exists(FICHIER_TEST):
        os.remove(FICHIER_TEST)


# ──────────────────────────────────────────────────────
# sauvegarder / charger
# ──────────────────────────────────────────────────────

def test_sauvegarder_cree_le_fichier(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    assert os.path.exists(FICHIER_TEST)


def test_charger_renvoie_liste_vide_si_fichier_absent(fichier_temp):
    assert GestionResultats.charger("football") == []


def test_sauvegarder_et_charger_un_resultat(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    matchs = GestionResultats.charger("football")
    assert len(matchs) == 1
    m = matchs[0]
    assert m.equipe_1 == "PSG"
    assert m.equipe_2 == "Lyon"
    assert m.score_1 == 2.0
    assert m.score_2 == 1.0
    assert m.sport == "football"


def test_charger_filtre_par_sport(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    GestionResultats.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    assert len(GestionResultats.charger("football")) == 1
    assert len(GestionResultats.charger("LOL")) == 1
    assert len(GestionResultats.charger("tennis")) == 0


def test_plusieurs_resultats_cumules(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    GestionResultats.sauvegarder("football", "2025-01-08", "Lyon", "PSG", 0, 3)
    assert len(GestionResultats.charger("football")) == 2


# ──────────────────────────────────────────────────────
# _correspond
# ──────────────────────────────────────────────────────

def test_correspond_sous_chaine_directe():
    assert GestionResultats._correspond("Arsenal", "Arsenal FC")


def test_correspond_sous_chaine_inverse():
    assert GestionResultats._correspond("Arsenal FC", "Arsenal")


def test_correspond_egalite_exacte():
    assert GestionResultats._correspond("PSG", "PSG")


def test_correspond_insensible_casse():
    assert GestionResultats._correspond("psg", "PSG")


def test_correspond_faux_si_aucun_rapport():
    assert not GestionResultats._correspond("Lyon", "PSG")


# ──────────────────────────────────────────────────────
# appliquer_a_equipe
# ──────────────────────────────────────────────────────

def test_appliquer_a_equipe_victoire(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    e = Equipe("PSG", "football")
    nb = GestionResultats.appliquer_a_equipe(e, "PSG")
    assert nb == 1
    assert e.victoires == 1
    assert e.defaites == 0
    assert e.score_pour == 2.0
    assert e.score_contre == 1.0


def test_appliquer_a_equipe_defaite(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 0, 2)
    e = Equipe("Lyon", "football")
    nb = GestionResultats.appliquer_a_equipe(e, "Lyon")
    assert nb == 1
    assert e.victoires == 1
    assert e.score_pour == 2.0


def test_appliquer_a_equipe_plusieurs_matchs(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    GestionResultats.sauvegarder("football", "2025-01-08", "Marseille", "PSG", 0, 3)
    e = Equipe("PSG", "football")
    nb = GestionResultats.appliquer_a_equipe(e, "PSG")
    assert nb == 2
    assert e.victoires == 2
    assert e.matchs_joues == 2


def test_appliquer_a_equipe_aucun_match(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    e = Equipe("Marseille", "football")
    nb = GestionResultats.appliquer_a_equipe(e, "Marseille")
    assert nb == 0
    assert e.matchs_joues == 0


def test_appliquer_a_equipe_nul_impossible(fichier_temp):
    GestionResultats.sauvegarder("basketball", "2025-01-01", "Lakers", "Bulls", 110, 95)
    e = Equipe("Lakers", "basketball")
    GestionResultats.appliquer_a_equipe(e, "Lakers", nul_possible=False)
    assert e.victoires == 1
    assert e.points == 1


# ──────────────────────────────────────────────────────
# appliquer_a_competition
# ──────────────────────────────────────────────────────

def test_appliquer_a_competition_cree_equipes(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    nb = GestionResultats.appliquer_a_competition(comp)
    assert nb == 1
    assert len(comp.equipes) == 2


def test_appliquer_a_competition_met_a_jour_stats(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    GestionResultats.appliquer_a_competition(comp)
    assert comp.equipes["PSG"].victoires == 1
    assert comp.equipes["Lyon"].defaites == 1


def test_appliquer_a_competition_equipe_existante(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    comp.ajouter_equipe("PSG", Equipe("PSG", "football"))
    GestionResultats.appliquer_a_competition(comp)
    assert comp.equipes["PSG"].victoires == 1


# ──────────────────────────────────────────────────────
# lister
# ──────────────────────────────────────────────────────

def test_lister_tous_les_sports(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    GestionResultats.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    assert len(GestionResultats.lister()) == 2


def test_lister_filtre_par_sport(fichier_temp):
    GestionResultats.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    GestionResultats.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    assert len(GestionResultats.lister("football")) == 1
    assert len(GestionResultats.lister("LOL")) == 1


def test_lister_fichier_absent(fichier_temp):
    assert GestionResultats.lister() == []
