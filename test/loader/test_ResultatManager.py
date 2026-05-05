import pytest
import src.loader.ResultatManager as rm_module
from src.loader.ResultatManager import ResultatManager
from src.Model.Equipe import Equipe
from src.Model.Competition import Competition


@pytest.fixture(autouse=True)
def fichier_temp(tmp_path, monkeypatch):
    """Redirige FICHIER_RESULTATS vers un fichier temporaire pour chaque test."""
    fichier = str(tmp_path / "nouveaux_matchs.csv")
    monkeypatch.setattr(rm_module, "FICHIER_RESULTATS", fichier)
    return fichier


# ──────────────────────────────────────────────────────
# sauvegarder / charger
# ──────────────────────────────────────────────────────

def test_sauvegarder_cree_le_fichier(fichier_temp):
    import os
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    assert os.path.exists(fichier_temp)


def test_charger_renvoie_liste_vide_si_fichier_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(rm_module, "FICHIER_RESULTATS", str(tmp_path / "inexistant.csv"))
    assert ResultatManager.charger("football") == []


def test_sauvegarder_et_charger_un_resultat():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    matchs = ResultatManager.charger("football")
    assert len(matchs) == 1
    m = matchs[0]
    assert m.equipe_1 == "PSG"
    assert m.equipe_2 == "Lyon"
    assert m.score_1 == 2.0
    assert m.score_2 == 1.0
    assert m.sport == "football"


def test_charger_filtre_par_sport():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    ResultatManager.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    assert len(ResultatManager.charger("football")) == 1
    assert len(ResultatManager.charger("LOL")) == 1
    assert len(ResultatManager.charger("tennis")) == 0


def test_plusieurs_resultats_cumules():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    ResultatManager.sauvegarder("football", "2025-01-08", "Lyon", "PSG", 0, 3)
    matchs = ResultatManager.charger("football")
    assert len(matchs) == 2


# ──────────────────────────────────────────────────────
# _correspond
# ──────────────────────────────────────────────────────

def test_correspond_sous_chaine_directe():
    assert ResultatManager._correspond("Arsenal", "Arsenal FC")


def test_correspond_sous_chaine_inverse():
    assert ResultatManager._correspond("Arsenal FC", "Arsenal")


def test_correspond_egalite_exacte():
    assert ResultatManager._correspond("PSG", "PSG")


def test_correspond_insensible_casse():
    assert ResultatManager._correspond("psg", "PSG")


def test_correspond_faux_si_aucun_rapport():
    assert not ResultatManager._correspond("Lyon", "PSG")


# ──────────────────────────────────────────────────────
# appliquer_a_equipe
# ──────────────────────────────────────────────────────

def test_appliquer_a_equipe_victoire():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    e = Equipe("PSG", "football")
    nb = ResultatManager.appliquer_a_equipe(e, "PSG")
    assert nb == 1
    assert e.victoires == 1
    assert e.defaites == 0
    assert e.score_pour == 2.0
    assert e.score_contre == 1.0


def test_appliquer_a_equipe_defaite():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 0, 2)
    e = Equipe("Lyon", "football")
    nb = ResultatManager.appliquer_a_equipe(e, "Lyon")
    assert nb == 1
    assert e.victoires == 1
    assert e.score_pour == 2.0


def test_appliquer_a_equipe_plusieurs_matchs():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    ResultatManager.sauvegarder("football", "2025-01-08", "Marseille", "PSG", 0, 3)
    e = Equipe("PSG", "football")
    nb = ResultatManager.appliquer_a_equipe(e, "PSG")
    assert nb == 2
    assert e.victoires == 2
    assert e.matchs_joues == 2


def test_appliquer_a_equipe_aucun_match():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    e = Equipe("Marseille", "football")
    nb = ResultatManager.appliquer_a_equipe(e, "Marseille")
    assert nb == 0
    assert e.matchs_joues == 0


def test_appliquer_a_equipe_nul_impossible():
    ResultatManager.sauvegarder("basketball", "2025-01-01", "Lakers", "Bulls", 110, 95)
    e = Equipe("Lakers", "basketball")
    ResultatManager.appliquer_a_equipe(e, "Lakers", nul_possible=False)
    assert e.victoires == 1
    assert e.points == 1


# ──────────────────────────────────────────────────────
# appliquer_a_competition
# ──────────────────────────────────────────────────────

def test_appliquer_a_competition_cree_equipes():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    nb = ResultatManager.appliquer_a_competition(comp)
    assert nb == 1
    assert len(comp.equipes) == 2


def test_appliquer_a_competition_met_a_jour_stats():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    ResultatManager.appliquer_a_competition(comp)
    assert comp.equipes["PSG"].victoires == 1
    assert comp.equipes["Lyon"].defaites == 1


def test_appliquer_a_competition_equipe_existante():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    comp = Competition("Test", "football")
    equipe_psg = Equipe("PSG", "football")
    comp.ajouter_equipe("PSG", equipe_psg)
    ResultatManager.appliquer_a_competition(comp)
    assert comp.equipes["PSG"].victoires == 1


# ──────────────────────────────────────────────────────
# lister
# ──────────────────────────────────────────────────────

def test_lister_tous_les_sports():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    ResultatManager.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    tous = ResultatManager.lister()
    assert len(tous) == 2


def test_lister_filtre_par_sport():
    ResultatManager.sauvegarder("football", "2025-01-01", "PSG", "Lyon", 2, 1)
    ResultatManager.sauvegarder("LOL", "2025-01-02", "T1", "G2", 1, 0)
    assert len(ResultatManager.lister("football")) == 1
    assert len(ResultatManager.lister("LOL")) == 1


def test_lister_fichier_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(rm_module, "FICHIER_RESULTATS", str(tmp_path / "inexistant.csv"))
    assert ResultatManager.lister() == []
