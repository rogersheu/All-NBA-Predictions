import decimal
import pandas as pd
from dataclasses import dataclass


class PlayerAccolades:
    name : str = ""
    allstar : bool = False
    allnba : bool = False