from src.Common.utils import print_timings


@print_timings
def parse_players_csv(filepath: str, sep: str = ";") -> list:
    players = []

    with open(filepath, "r", encoding="utf-8") as f:
        headers = f.readline().strip().split(sep)

        for line in f:
            values = line.strip().split(sep)
            player = dict(zip(headers, values))
            players.append(player)

    return players
