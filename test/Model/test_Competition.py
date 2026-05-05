from src.Model.Competition import Competition
from src.Model.Equipe import Equipe


def _equipe(nom: str, victoires: int = 0, nuls: int = 0, defaites: int = 0,
            buts_pour: int = 0, buts_contre: int = 0) -> Equipe:
    """Construit une Equipe avec un bilan précis sans lire de fichier."""
    e = Equipe(nom, "football")
    for _ in range(victoires):
        e.ajouter_match(1, 0)
    for _ in range(nuls):
        e.ajouter_match(0, 0)
    for _ in range(defaites):
        e.ajouter_match(0, 1)
    e.score_pour   += buts_pour
    e.score_contre += buts_contre
    return e


def test_init():
    c = Competition("Ligue 1", "football")
    assert c.nom == "Ligue 1"
    assert c.sport == "football"
    assert len(c.equipes) == 0


def test_ajouter_equipe():
    c = Competition("Ligue 1", "football")
    e = Equipe("PSG", "football")
    c.ajouter_equipe("psg", e)
    assert "psg" in c.equipes
    assert c.equipes["psg"].nom == "PSG"


def test_ajouter_equipe_remplace_existante():
    c = Competition("Ligue 1", "football")
    c.ajouter_equipe("psg", Equipe("PSG", "football"))
    c.ajouter_equipe("psg", Equipe("Paris SG", "football"))
    assert c.equipes["psg"].nom == "Paris SG"


def test_classement_par_points():
    c = Competition("Test", "football")
    c.ajouter_equipe("a", _equipe("Team A", victoires=3))          # 9 pts
    c.ajouter_equipe("b", _equipe("Team B", victoires=1, nuls=2))  # 5 pts
    c.ajouter_equipe("c", _equipe("Team C", defaites=3))           # 0 pts
    cl = c.classement_par("points")
    assert cl[0].nom == "Team A"
    assert cl[1].nom == "Team B"
    assert cl[2].nom == "Team C"


def test_classement_par_victoires():
    c = Competition("Test", "basketball")
    c.ajouter_equipe("a", _equipe("Team A", victoires=5))
    c.ajouter_equipe("b", _equipe("Team B", victoires=2))
    c.ajouter_equipe("c", _equipe("Team C", victoires=8))
    cl = c.classement_par("victoires")
    assert cl[0].nom == "Team C"
    assert cl[1].nom == "Team A"
    assert cl[2].nom == "Team B"


def test_classement_liste_vide():
    c = Competition("Vide", "football")
    assert c.classement_par("points") == []


def test_repr_contient_nom_et_sport():
    c = Competition("Ligue 1", "football")
    r = repr(c)
    assert "Ligue 1" in r
    assert "football" in r
