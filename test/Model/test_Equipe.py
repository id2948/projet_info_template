import pytest
from src.Model.Equipe import Equipe


def test_init_valeurs_par_defaut():
    e = Equipe("PSG", "football")
    assert e.nom == "PSG"
    assert e.sport == "football"
    assert e.abreviation is None
    assert e.matchs_joues == 0
    assert e.victoires == 0
    assert e.defaites == 0
    assert e.nuls == 0
    assert e.points == 0
    assert e.score_pour == 0.0
    assert e.score_contre == 0.0


def test_init_avec_abreviation():
    e = Equipe("Paris Saint-Germain", "football", "PSG")
    assert e.abreviation == "PSG"


def test_ajouter_match_victoire_football():
    e = Equipe("PSG", "football")
    e.ajouter_match(3, 1)
    assert e.matchs_joues == 1
    assert e.victoires == 1
    assert e.defaites == 0
    assert e.nuls == 0
    assert e.points == 3
    assert e.score_pour == 3.0
    assert e.score_contre == 1.0


def test_ajouter_match_defaite():
    e = Equipe("PSG", "football")
    e.ajouter_match(0, 2)
    assert e.defaites == 1
    assert e.victoires == 0
    assert e.points == 0


def test_ajouter_match_nul():
    e = Equipe("PSG", "football")
    e.ajouter_match(1, 1)
    assert e.nuls == 1
    assert e.victoires == 0
    assert e.defaites == 0
    assert e.points == 1


def test_ajouter_match_sans_nul_victoire():
    e = Equipe("Lakers", "basketball")
    e.ajouter_match(110, 95, nul_possible=False)
    assert e.victoires == 1
    assert e.points == 1


def test_ajouter_match_sans_nul_defaite():
    e = Equipe("Lakers", "basketball")
    e.ajouter_match(80, 100, nul_possible=False)
    assert e.defaites == 1
    assert e.nuls == 0
    assert e.points == 0


def test_cumul_plusieurs_matchs():
    e = Equipe("PSG", "football")
    e.ajouter_match(2, 0)
    e.ajouter_match(1, 1)
    e.ajouter_match(0, 3)
    assert e.matchs_joues == 3
    assert e.victoires == 1
    assert e.nuls == 1
    assert e.defaites == 1
    assert e.points == 4
    assert e.score_pour == 3.0
    assert e.score_contre == 4.0


def test_difference_score_positive():
    e = Equipe("PSG", "football")
    e.ajouter_match(3, 1)
    e.ajouter_match(2, 2)
    assert e.difference_score == 2.0


def test_difference_score_negative():
    e = Equipe("PSG", "football")
    e.ajouter_match(0, 3)
    assert e.difference_score == -3.0


def test_winrate_normal():
    e = Equipe("PSG", "football")
    e.ajouter_match(1, 0)  # victoire
    e.ajouter_match(0, 0)  # nul
    e.ajouter_match(0, 1)  # défaite
    assert e.winrate == pytest.approx(100 / 3, rel=1e-3)


def test_winrate_100_pourcent():
    e = Equipe("PSG", "football")
    e.ajouter_match(1, 0)
    e.ajouter_match(2, 0)
    assert e.winrate == 100.0


def test_winrate_zero_matchs():
    e = Equipe("PSG", "football")
    assert e.winrate == 0.0


def test_str_contient_nom_et_stats():
    e = Equipe("PSG", "football")
    e.ajouter_match(2, 0)
    s = str(e)
    assert "PSG" in s
    assert "1" in s


def test_repr_contient_nom_et_sport():
    e = Equipe("PSG", "football")
    r = repr(e)
    assert "PSG" in r
    assert "football" in r
