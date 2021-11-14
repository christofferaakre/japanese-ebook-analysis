#!/usr/bin/env python3
import sys
from book import analyse_epub

print(sys.argv)
assert len(sys.argv) == 2, "Usage: ./analyse_ebook.py filename"
filename = sys.argv[1]

book_data = analyse_epub(filename)
print(book_data)
