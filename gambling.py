import random
from abc import ABC, abstractmethod

class Gambling(ABC):
    bet: int
    multilplier: int