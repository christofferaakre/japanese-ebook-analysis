from dataclasses import dataclass
from typing import Dict

@dataclass
class Word:
    frequency: int
    stars: int

@dataclass
class FrequencyList:
    name: str
    words: Dict[str, Word]


