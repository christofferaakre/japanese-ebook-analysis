#!/usr/bin/env python3
import sys
from book_utils import analyse_ebook
from book_utils import gethistogram #what tarran added
print(sys.argv)
assert len(sys.argv) == 2, "Usage: ./analyse_ebook.py filename"
filename = sys.argv[1]

book_data = analyse_ebook(filename)
print(book_data)
