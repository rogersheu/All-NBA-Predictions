from dataclasses import dataclass

import pandas as pd


@dataclass
class PlayerTotals:
    games: int = 0
    mins: int = 0
    Tot_FG: int = 0
    Tot_FGA: int = 0
    Tot_3P: int = 0
    Tot_3PA: int = 0
    Tot_2P: int = 0
    Tot_2PA: int = 0
    Tot_FT: int = 0
    Tot_FTA: int = 0
    Tot_OREB: int = 0
    Tot_DREB: int = 0
    Tot_TREB: int = 0
    Tot_AST: int = 0
    Tot_STL: int = 0
    Tot_BLK: int = 0
    Tot_TOV: int = 0
    Tot_PTS: int = 0


# Calculate TS%, 3PAr, FTr
