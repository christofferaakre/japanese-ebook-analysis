import base64
import subprocess
import re
import json
from pathlib import Path

from FrequencyList import FrequencyList, Word

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
        {freq} is not a postiive integer. You must provide
        a positive integer as the frequency.
        ''')

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





def get_all_subdirs(path: str) -> list:
    """
    Returns a list of all the subdirectories that exist
    in the given directory
    Arguments:
    path: str - Path of directory to search in
    """
    p = Path(path)
    return [x for x in p.iterdir() if x.is_dir()]

def get_books() -> list:
    """
    Returns a list of the data for all the
    analysed ebooks
    """
    book_dirs = get_all_subdirs('static/books')
    books = []
    for book_dir in book_dirs:
        filename = f'{book_dir}/book_data.json'
        with open(filename) as file:
            book_data = json.load(file)
        books.append(book_data)
    return books

def get_book(hash: str) -> object:
    """
    Returns the data for the book with the given hash.
    Arguments:
    hash: str - The sha256 sum hash for the epub file
    """

    with open(f'static/books/{hash}/book_data.json') as file:
        book_data = json.load(file)
        return book_data

def save_base64_image(base64string: str, filename: str) -> str:
    """
    Decodes the given base64 string and saves it as an image with the specified
    filename. Returns the filename.
    Arguments:
    base64string: str - The base64 string encoded string
    filename: str - The filename you want to save the image to
    """
    image_data = base64.b64decode(base64string)
    with open(filename, 'wb') as file:
        file.write(image_data)
    return filename

def remove_ruby_text_from_epub(
        filename:  str,
        new_filename: str = None
        ) -> str:
    """
    Removes all ruby text from the given .epub file.
    Requires furigana4epub to be installed and in system path
    Returns the path of the new file
    (pip install furigana4epub).
    Arguments:
    filename: str - The filename for the epub file to remove ruby text
    from
    """
    if not new_filename:
        new_filename = filename

    name = filename.replace('.epub', '')
    subprocess.run(f'furigana4epub -d {filename}', shell=True)
    subprocess.run(f'mv {name}_no_furigana.epub {new_filename}', shell=True)
    return new_filename

def convert_epub_to_txt(filename: str,
                        process_text: bool = False
                        ) -> str:
    """
    NOTE: requires pandoc to be in system path.
    Converts the given epub file to a .txt file with
    the same filename (minus extension) in the same directory.
    Returns the filename of the .txt file
    Arguments:
    filename : str - The filename of the .epub file you want to convert
    process_text: bool (optional, default = False) - Process
    the text to filter out any non-japanese text using a regex
    """

    txt_filename = filename.replace('.epub', '.txt')
    subprocess.run(f'./convert_epub_to_txt {filename}', shell=True)


    if process_text:
        with open(txt_filename, 'r', encoding='utf-8') as file:
            text = file.read()
        with open(txt_filename, 'w', encoding='utf-8') as file:
            file.write(process_japanese_text(text))

    return txt_filename

def process_japanese_text(text: str) -> str:
    """
    Filters out any text that is not japanese using a regex,
    and returns the processed text
    Arguments:
    text: str - The text to process
    """
    regex = r"[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B"
    processed = ''.join(re.findall(regex, text)).replace('\u3000', '')
    return processed

def parse_sentence(sentence: str, mt) -> list:
    """
    Parses the given sentence into a list of words using mecab.
    Arguments:
    sentence: str - The sentence you want to parse
    mt - A mecab tagger. Create using MeCab.Tagger
    """
    filter_str = r'()./,!:?\uksa0123456789\t\r\s .'
    parsed = mt.parseToNode(sentence)
    words = []
    while parsed:
        word = re.sub(r'\s+', '', parsed.surface)
        for char in filter_str:
            word = word.replace(char, '')
        if len(word) >= 1:
            words.append(word)
        parsed = parsed.next
    return words
