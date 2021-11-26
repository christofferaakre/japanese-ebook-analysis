from typing import List, Set, Tuple, Dict, NamedTuple, Union, Any
from utils import parse_sentence
from frequency_lists import get_frequency, FrequencyList, Word

class CharAnalysis(NamedTuple):
    all: List[str]
    unique: Set[str]
    with_uses: List[Dict[str, Union[str, int]]]
    used_once: Set[str]

class WordAnalysis(NamedTuple):
    all: List[str]
    unique: Set[str]
    with_uses: List[Tuple[str, int]]
    used_once: Set[str]
    known_unique: int
    known_total: int

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

    chars_used_once = {str(char['character']) for char in chars_with_uses if char['occurences'] == 1}

    return CharAnalysis(all=chars,
            unique=unique_chars,
            with_uses=chars_with_uses,
            used_once=chars_used_once
            )

def analyse_words(text: str, mt, frequency_lists: List[FrequencyList]) -> WordAnalysis:
    """
    Analyses the given text and returns a
    WordAnalysis instance describing it.
    Arguments:
    text: str - The text to analyse
    mt - A Mecab Tagger. Create using Mecab.Tagger
    frequency_lists: List[FrequencyList] - A list of the frequency
    lists you want to use for analysis
    """
    words = parse_sentence(text, mt)
    unique_words = set(words)

    words_with_uses = sorted(
        [{
        "word": word,
        "frequency": get_frequency(word, frequency_lists),
        "occurences": words.count(word),
        } for word in unique_words],
        key=lambda e: e['occurences'], reverse=True
        )

    used_once = {word['word'] for word in words_with_uses if word['occurences'] == 1}

    known = analyse_known_words(unique_words, words)

    return WordAnalysis(all=words,
            unique=unique_words,
            with_uses=words_with_uses,
            used_once=used_once,
            known_unique=known['unique'],
            known_total=known['total']
            )

def analyse_known_words(unique_words: Set[str], words: List[str]) -> Dict[str, int]:
    """
    Given a set of unique words present in a text, and a list of all the words
    that appear (including repeats), performs some simple known words analysis
    and return the number of unique known words, as well as the total number of
    (non-unique) words in the text that are known
    Arguments:
    unique_words: Set[str] - The set of unique words in the text
    words: List[str] - The list of all (non-unique) words in the text
    """
    known_words = process_wordlist('word-list.txt')
    n_known_words = len(unique_words.intersection(known_words))
    total_known_words = sum(1 if word in known_words else 0 for word in words)
    return {
            "unique": n_known_words,
            "total": total_known_words
           }

def process_wordlist(filename: str) -> Set[str]:
    """
    Process the given word-list (in .txt format) and
    returns a list of all the words in the file.
    The file must be a .txt file with words separated
    by newline characters.
    Arguments:
    filename: str - The path to the .txt file containing the words
    """
    with open(filename, 'r') as file:
        words = set([line.replace('\n', '') for line in file.readlines()])

    return words
