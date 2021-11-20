import pandas as pd
from dataclasses import dataclass


@dataclass
class Player(object):
    name : str = ""
    ID : str = ""
    year : int = 0