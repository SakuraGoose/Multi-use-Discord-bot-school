import random
from abc import ABC

class Gambling(ABC):
    multiplier: int
    bet_amount: int