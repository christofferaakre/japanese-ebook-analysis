import base64
import subprocess
import re
import json
from pathlib import Path
from MecabNode import MecabNode

from frequency_lists import FrequencyList

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

def get_book(hash: str) -> dict:
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
    parse_results = mt.parse(sentence).split("\n")
    words = []

    for line in parse_results:
        # ignore mecab's EOS outputs and line without tabs
        if line.startswith("EOS") or not "\t" in line:
            continue

        node = MecabNode(line)
        word = re.sub(r'\s+', '', node.surface)
        for char in filter_str:
            word = word.replace(char, '')
        if len(word) >= 1:
            words.append(word)
    return words
