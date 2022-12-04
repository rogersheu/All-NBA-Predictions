import decimal
from dataclasses import dataclass

import pandas as pd


class PlayerAccolades:
    name: str = ""
    allstar: bool = False
    allnba: bool = False
