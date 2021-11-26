from re import A
from typing import List, Set, Tuple, Dict, NamedTuple, Union, Any
class CharAnalysis(NamedTuple):
    all: List[str]
    unique: Set[str]
    with_uses: List[Dict[str, Union[str, int]]]
    used_once: Set[str]

class WordAnalysis(NamedTuple):
    all: List[str]
    unique: Set[str]
    with_uses: List[Tuple[str, int]]
    use_once = Set[str]
    known = Set[str]

def analyse_chars(text: str) -> CharAnalysis:
    """
    Analyses the given text and returns a
    CharAnalysis instance describing it.
    Arguments:
    text: str - The text to analyse
    """
    chars = list(text)
    unique_chars = set(text)
    chars_with_uses = sorted(
        [{
        "character": char,
        "occurences": chars.count(char)
        } for char in unique_chars],
        key=lambda e: e["occurences"], reverse=True
        )
    chars_used_once = {str(char['character']) for char in chars_with_uses}

    return CharAnalysis(all=chars,
            unique=unique_chars,
            with_uses=chars_with_uses,
            used_once=chars_used_once
            )

def analyse_words(text: str) -> WordAnalysis:
    """
    Analyses the given text and returns a
    WordAnalysis instance describing it.
    Arguments:
    text: str - The text to analyse
    """
    raise NotImplementedError
