from dataclasses import dataclass
from typing import List, Dict, Union, NamedTuple
from pathlib import Path

import re
import json

class Word(NamedTuple):
    frequency: int
    stars: int

class FrequencyList(NamedTuple):
    name: str
    words: Dict[str, Word]

def stars_from_frequency(freq: int) -> int:
    """
    Returns the appropriate number of frequency stars
    given the frequency. The rule is as follows:
    1-1500: 5 stars
    1501-5000: 4 stars
    5001-15000: 3 stars
    15001-30000: 2 stars
    30001-60000: 1 star
    60001+: 0 stars
    Arguments:
    frequency: int - The frequency of the word
    """
    if 1 <= freq <= 1500:
        return 5
    elif 1501 <= freq <= 5000:
        return 4
    elif 5001 <= freq <= 15000:
        return 3
    elif 15001 <= freq <= 30000:
        return 2
    elif 30001 <= freq <= 60000:
        return 1
    elif 60001 <= freq:
        return 0
    else:
        raise ValueError(f'''
        Error in stars_from_frequency:
        {freq} is not a postiive integer. You must provide
        a positive integer as the frequency.
        ''')

def get_all_frequency_lists() -> List[FrequencyList]:
    """
    Gets a list of FrequencyList objects for each of the
    frequency list json files in the frequency list directory
    """
    p = Path('frequency-lists').glob('*.json')
    frequency_lists = []
    for path in p:
        frequency_list = process_frequency_list(str(path))
        frequency_lists.append(frequency_list)

    return frequency_lists

def get_overall_frequency(frequencies: Dict[str, Word]) -> Union[Word, str]:
    """
    Given the frequency of a word from several different frequency lists,
    compute an 'overall frequency'. We do this by computing
    the average of 1 / frequency, and then taking the reciprocal of that.
    Arguments:
    frequencies: Dict[str, Word] - A dictionary with the frequencies from
    each frequency list
    """
    frequency_scores = [1 / freq.frequency for freq in frequencies.values()]
    total_score = sum(frequency_scores)
    if total_score == 0:
        return 'N/A'
    overall_frequency = round(1 / sum(frequency_scores) * len(frequency_scores))
    return Word(overall_frequency, stars_from_frequency(overall_frequency))


def get_frequency(word: str, frequency_lists: List[FrequencyList]) -> Dict[str, Word]:
    """
    Returns the frequency of the word for each frequency list
    specified.
    Arguments:
    word: str - The word to get the frequency of
    frequency: List[FrequencyList] - The list of frequency lists to use
    """
    frequencies = {}
    for frequency_list in frequency_lists:
        try:
            frequency = frequency_list.words[word]
            frequencies[frequency_list.name] = frequency
        except KeyError:
            continue

    frequencies['Overall'] = get_overall_frequency(frequencies)

    return frequencies

def process_frequency_list(filename: str) -> FrequencyList:
    """
    Processes a frequency list json file and returns
    a FrequencyList object describing the frequency list
    Arguments:
    filename: str - The path to the json file
    """
    name = filename.split('/')[-1].split('.')[-2]

    with open(filename, 'r') as file:
        data = json.load(file)

    # format used in word, 'freq', *stars* (freq),
    # e.g. 'の', 'freq', '★★★★★ (1)'

    number_regex = r'[0-9]+'
    words = {}

    for word, _, freq_string in data:
        match = re.search(number_regex, freq_string)
        assert match is not None, f'Could not find a frequency for {word} in {filename}'

        freq = int(match[0])
        stars = stars_from_frequency(freq)
        word_object = Word(freq, stars)
        words[word] = word_object

    frequency_list = FrequencyList(name, words)
    return frequency_list



