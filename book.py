from re import S
import subprocess
import MeCab
import epub_meta
from utils import save_base64_image, convert_epub_to_txt, process_japanese_text, parse_sentence, remove_ruby_text_from_epub

from pathlib import Path
import hashlib
import mmap
import json

from constants import UPLOAD_FOLDER

def sha256sum(filename: str) -> str:
    """
    Computes the sha256 sum of the given file.
    Arguments:
    filename: str - The path to the file to compute the hash of
    """
    h  = hashlib.sha256()
    with open(filename, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
            h.update(mm)
    return h.hexdigest()

def analyse_ebook(filename: str, fallback_title: str = 'Book Title') -> object:
    """
    Analayse a ebook containing japanese text, determining various things
    like the length of the book in words/characters, the number of unique
    words and characters used, and the number of words and characters that
    are used once only. Returns and object containing this information.
    Arguments:
    filename: str - The path to the file to analyse
    fallback_title: str (optional) - Optionally, you can pass a fallback title.
    If function can't figure out what the ebook you passed is called, it
    will use this as the book title
    """
    file_hash = sha256sum(filename)
    book_dir = f'static/books/{file_hash}'
    subprocess.run(f'mkdir -p {book_dir}', shell=True)

    mt = MeCab.Tagger('-r /dev/null -d /usr/lib/mecab/dic/mecab-ipadic-neologd/')

    book_path = filename
    extension = filename.split('.')[-1]

    if extension == 'epub':
        book_path = remove_ruby_text_from_epub(filename, new_filename=f"{book_dir}/no-furigana.epub")

    book = {}
    if extension == 'epub':
        book = epub_meta.get_epub_metadata(book_path)
    elif extension == 'txt':
        book = {
                'title': fallback_title,
                'authors': '',
                'cover_image_content': '',
                }

    title = book['title']
    authors = book['authors']
    cover_image = book['cover_image_content']
    image_path = ''

    txt_file = ''

    if extension == 'epub':
        image_path = save_base64_image(cover_image, f'{book_dir}/musume.jpg')
        txt_file = convert_epub_to_txt(book_path, process_text=True)

    elif extension == 'txt':
        image_path = ''
        txt_file = filename

    with open(txt_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Analysing characters
    chars = list(text)
    unique_chars = set(text)
    chars_with_uses = sorted([(char, chars.count(char)) for char in unique_chars], key=lambda tup: tup[1], reverse=True)
    chars_used_once = [char for char, count in chars_with_uses if count == 1]

    # analysing words
    words = parse_sentence(text, mt)
    unique_words = set(words)
    words_with_uses = sorted([(word, words.count(word)) for word in unique_words], key=lambda tup: tup[1], reverse=True)
    used_once = [word for word, uses in words_with_uses if uses == 1]

    word_list = [{"word": word, "ocurrences": occurences} for word, occurences in words_with_uses]
    char_list = [{"character": char, "occurences": occurences} for char, occurences in chars_with_uses]

    book_data = {
        'title': title,
        'authors': authors,
        'image': image_path,
        'n_words': len(words),
        'n_words_unique': len(unique_words),
        'n_words_used_once': len(used_once),
        'n_chars': len(chars),
        'n_chars_unique': len(unique_chars),
        'n_chars_used_once': len(chars_used_once),
        'words': word_list,
        'chars': char_list,
        'file_hash': file_hash
    }

    json_filename = f'{book_dir}/book_data.json'
    with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(book_data, file)
    print(f'wrote data to {json_filename}')

    clean_dir(book_dir, keep_extensions=['.json', '.jpg', '.png'])
    clean_dir(UPLOAD_FOLDER)

    return book_data

def clean_dir(directory: str, keep_extensions: list = None) -> None:
    """
    Delete all the files in the given directory, keeping
    the files that have one of the extesnsions given in
    keep_extensions. Returns None
    Arguments:
    directory: str - Path to the directory you want to clean
    keep_extensions: list - List of the extensions you want to keep.
    For example, ['.json', '.jpg', '.png']
    """
    if not keep_extensions:
        keep_extensions = []
    for f in Path(directory).glob("*"):
        if f.is_file():
            extension = f.suffix
            if not extension in keep_extensions:
                f.unlink()
