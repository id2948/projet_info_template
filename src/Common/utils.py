import time
from typing import Union


def print_timings(func):
    """Décorateur qui mesure et affiche le temps d'exécution d'une fonction.

    Parameters
    ----------
    func : callable
        Fonction à décorer.

    Returns
    -------
    callable
        Fonction décorée affichant sa durée d'exécution après chaque appel.
    """
    def wrap_func(*args, **kwargs):
        start_time = time.process_time()
        result = func(*args, **kwargs)
        end_time = time.process_time()
        print(f'Function {func.__name__!r} executed in {(end_time-start_time):.4f}s')
        return result
    return wrap_func


def parse_boolean(input: Union[str, bool]) -> bool:
    """Convertit une valeur en booléen.

    Les chaînes "true" et "vrai" (insensible à la casse) sont considérées
    vraies ; toute autre valeur est considérée fausse.

    Parameters
    ----------
    input : str | bool
        Valeur à convertir.

    Returns
    -------
    bool
        Résultat de la conversion.
    """
    if isinstance(input, bool):
        return input

    if str(input).lower() in ["true", "vrai"]:
        return True
    return False
