from typing import List
from dataclasses import dataclass

@dataclass
class Book:
    path: str
    title: str
    authors: List[str]
    image: str
    file_hash: str
    book_dir: str

