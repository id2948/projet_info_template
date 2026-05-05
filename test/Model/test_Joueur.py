from src.Model.Joueur import Joueur


def test_init_champs_obligatoires():
    j = Joueur("Mbappé", "football")
    assert j.nom == "Mbappé"
    assert j.sport == "football"


def test_init_optionnels_none_par_defaut():
    j = Joueur("Mbappé", "football")
    assert j.prenom is None
    assert j.pseudo is None
    assert j.equipe is None
    assert j.position is None
    assert j.taille is None
    assert j.poids is None
    assert j.pays is None
    assert j.main is None


def test_init_tous_les_champs():
    j = Joueur("Mbappé", "football", prenom="Kylian", equipe="PSG",
               position="Attaquant", pays="France", taille=178.0, poids=73.0)
    assert j.prenom == "Kylian"
    assert j.equipe == "PSG"
    assert j.taille == 178.0


def test_str_avec_prenom():
    j = Joueur("Mbappé", "football", prenom="Kylian")
    s = str(j)
    assert "Kylian" in s
    assert "Mbappé" in s
    assert "football" in s


def test_str_avec_pseudo_sans_prenom():
    j = Joueur("Lee Sang-hyeok", "LOL", pseudo="Faker")
    s = str(j)
    assert "Faker" in s
    assert "Lee Sang-hyeok" in s


def test_str_sans_prenom_ni_pseudo():
    j = Joueur("Nadal", "tennis")
    s = str(j)
    assert "Nadal" in s


def test_str_affiche_equipe_si_presente():
    j = Joueur("James", "basketball", prenom="LeBron", equipe="Lakers")
    s = str(j)
    assert "Lakers" in s


def test_str_affiche_pays_si_present():
    j = Joueur("Zverev", "tennis", prenom="Alexander", pays="GER")
    s = str(j)
    assert "GER" in s
