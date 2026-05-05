def parse_csv(filepath: str, sep: str = ";") -> list:
    """Parse un fichier CSV et retourne une liste de dictionnaires.

    Parameters
    ----------
    filepath : str
        Chemin vers le fichier CSV.
    sep : str, optional
        Séparateur de colonnes (par défaut ";").

    Returns
    -------
    list
        Liste de dict, un par ligne du fichier, avec les en-têtes comme clés.
    """
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        headers = f.readline().strip().split(sep)
        for line in f:
            values = line.strip().split(sep)
            row = {}
            for i, header in enumerate(headers):
                row[header] = values[i]
            rows.append(row)
    return rows
