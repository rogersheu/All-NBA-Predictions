from dataclasses import dataclass

import pandas as pd


@dataclass
class Player(object):
    name: str = ""
    ID: str = ""
    year: int = 0
