import subprocess
import MeCab
import epub_meta
from utils import save_base64_image, convert_epub_to_txt, process_japanese_text, parse_sentence, remove_ruby_text_from_epub
from frequency_lists import get_all_frequency_lists, get_frequency
from analysis import analyse_chars, analyse_words, WordAnalysis
from plots import get_histogram

from Book import Book

from pathlib import Path
import hashlib
import mmap
import simplejson
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

def process_file(filename: str) -> Book:
    """
    Process the given ebook file and returns a Book
    object describing it. The Book object contains various
    fields like the author, title, cover image, etc. as well
    as the path to a generated .txt file (regardless of input extension)
    that has been processed to allow for easy analysis
    Arguments:
    filename: str - The path to the file
    """
    allowed_extensions = ['epub', 'txt']
    extension = filename.split('.')[-1]

    file_hash = sha256sum(filename)
    book_dir = f'static/books/{file_hash}'
    subprocess.run(f'mkdir -p {book_dir}', shell=True)

    if extension == 'epub':
        return process_epub(filename, book_dir=book_dir, file_hash=file_hash)
    elif extension == 'txt':
        return process_txt(filename, book_dir=book_dir, file_hash=file_hash)
    else:
        raise ValueError(f'Filename extension must be one of {",".join(allowed_extensions)}')

def process_epub(filename: str, book_dir: str, file_hash: str) -> Book:
    """
    Takes an epub file and returns a Book object.
    Arguments:
    filename: str - The path to the epub file
    book_dir: str - The directory the book is in
    file_hash: str - The sha256sum hash of the file
    """
    book_path = remove_ruby_text_from_epub(filename,
                                            new_filename=f"{book_dir}/no-furigana.epub")
    book_metadata = epub_meta.get_epub_metadata(book_path)
    title = book_metadata['title']
    authors = book_metadata['authors']
    image = book_metadata['cover_image_content']

    image_path = save_base64_image(image, f'{book_dir}/cover-image.jpg')
    txt_file = convert_epub_to_txt(book_path, process_text=True)

    book = Book(path=txt_file,
            title=title,
            authors=authors,
            image=image_path,
            file_hash=file_hash,
            book_dir=book_dir
            )
    return book

def process_txt(filename: str, book_dir: str, file_hash: str) -> Book:
    """
    Takes a .txt file and returns a Book object.
    Arguments:
    filename: str - The path to the .txt file
    book_dir: str - The directory the book is in
    file_hash: str - The sha256sum hash of the file
    """
    extension = '.' + filename.split('.')[-1]
    title = filename.split('/')[-1].replace(extension, '')
    book = Book(path=filename,
            title=title,
            authors=[],
            image='',
            file_hash=file_hash,
            book_dir=book_dir
            )
    return book

def analyse_ebook(filename: str) -> object:
    """
    Analayse a ebook containing japanese text, determining various things
    like the length of the book in words/characters, the number of unique
    words and characters used, and the number of words and characters that
    are used once only. Returns and object containing this information.
    Arguments:
    filename: str - The path to the file to analyse
    """

    mt = MeCab.Tagger('-r /dev/null -d /usr/lib/mecab/dic/mecab-ipadic-neologd/')
    book = process_file(filename)

    with open(book.path, 'r', encoding='utf-8') as file:
        text = file.read()

    frequency_lists = get_all_frequency_lists()
    chars = analyse_chars(text)
    words = analyse_words(text, mt, frequency_lists)

    histogram_path = get_histogram(words, f'{book.book_dir}/histogram.html')

    book_data = {
    'title': book.title,
    'authors': book.authors,
    'image': book.image,
    'histogram': histogram_path,
    'n_words': len(words.all),
    'n_words_unique': len(words.unique),
    'n_words_used_once': len(words.used_once),
    'n_known_words_unique': words.known_unique,
    'n_known_words_total': words.known_total,
    'n_chars': len(chars.all),
    'n_chars_unique': len(chars.unique),
    'n_chars_used_once': len(chars.used_once),
    'words': words.with_uses,
    'chars': chars.with_uses,
    'file_hash': book.file_hash
}

    json_filename = f'{book.book_dir}/book_data.json'
    with open(json_filename, 'w', encoding='utf-8') as file:
            simplejson.dump(book_data, file)
            #json.dump(book_data, file)
    print(f'wrote data to {json_filename}')


    clean_dir(book.book_dir, keep_extensions=['.json', '.jpg', '.png', '.html'])
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
