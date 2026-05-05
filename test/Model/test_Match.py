from src.Model.Match import Match


def test_init_champs_obligatoires():
    m = Match("2024-01-15", "Arsenal", "Chelsea", 2.0, 1.0, "football")
    assert m.date == "2024-01-15"
    assert m.equipe_1 == "Arsenal"
    assert m.equipe_2 == "Chelsea"
    assert m.score_1 == 2.0
    assert m.score_2 == 1.0
    assert m.sport == "football"


def test_init_champs_optionnels_none_par_defaut():
    m = Match("2024-01-15", "Arsenal", "Chelsea", 2.0, 1.0, "football")
    assert m.season is None
    assert m.season_type is None
    assert m.league_id is None
    assert m.stage is None
    assert m.patch is None
    assert m.week is None
    assert m.winner is None
    assert m.tourney_name is None
    assert m.surface is None
    assert m.round is None


def test_init_champs_optionnels_lol():
    m = Match("2025-01-10", "T1", "G2", 15, 12, "LOL",
              patch="15.1", week=3, winner="T1")
    assert m.patch == "15.1"
    assert m.week == 3
    assert m.winner == "T1"


def test_init_champs_optionnels_tennis():
    m = Match("20240128", "Sinner", "Medvedev", 1.0, 0.0, "tennis",
              tourney_name="Australian Open", surface="Hard", round="F")
    assert m.tourney_name == "Australian Open"
    assert m.surface == "Hard"
    assert m.round == "F"


def test_str_contient_les_equipes_et_le_sport():
    m = Match("2024-01-15", "Arsenal", "Chelsea", 2.0, 1.0, "football")
    s = str(m)
    assert "Arsenal" in s
    assert "Chelsea" in s
    assert "football" in s


def test_str_contient_les_scores():
    m = Match("2024-01-15", "Arsenal", "Chelsea", 3.0, 0.0, "football")
    s = str(m)
    assert "3.0" in s
    assert "0.0" in s
