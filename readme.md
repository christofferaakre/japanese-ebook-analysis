# japanese-ebook-analysis
This aim of this project is to make analysing the contents
of a japanese ebook easy and streamline the process
for non-technical users.
For text processing, we use [MeCab](https://taku910.github.io/mecab/)

## How to run the code
1. Clone repository: `git clone https://github.com/christofferaakre/japanese-ebook-analysis.git`
2. Make sure you have `mecab` set up on your system. See
[http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/](http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/)
for a good guide on how to set it up.
3. Install python dependencies: `pip install -r requirements.txt`
4. Install other dependencies (these all need to be in your system path):
    * `pandoc`
5. Run the `analyse_ebook.py` script. Syntax: `./analyse_ebook.py epub_file.epub`
