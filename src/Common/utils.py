def parse_boolean(input: str | bool) -> bool:
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
