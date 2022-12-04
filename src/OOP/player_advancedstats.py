import decimal
from dataclasses import dataclass
from decimal import *

import pandas as pd


@dataclass
class PlayerAdvanced:
    name: str = ""
    ID: str = ""
    year: int = 0
    OREBperc: float = 0
    DREBperc: decimal = 0
    TREBperc: decimal = 0
    ASTperc: decimal = 0
    STLperc: decimal = 0
    BLKperc: decimal = 0
    TOVperc: decimal = 0
    USGperc: decimal = 0
    OWS: decimal = 0
    DWS: decimal = 0
    WS: decimal = 0
    WSper48: decimal = 0
    OBPM: decimal = 0
    DBPM: decimal = 0
    BPM: decimal = 0
    VORP: decimal = 0
