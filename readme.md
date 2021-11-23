# japanese-ebook-analysis
This aim of this project is to make analysing the contents
of a japanese ebook easy and streamline the process
for non-technical users. You can analyse an ebook, and see the
following information:
* The length of the book in words
* The length of the book in characters
* The number of unique words used in the book
* The number of unique words that are only used once in the book
* The percentage of unique words that are only used once
* The number of unique characters used
* The number of unique characters that are only used once
* The percentage of unique characters that are only used once
* A list of all the words used in the book as well as how often they
are used
* A list of all the characters used in the book as well as how often
they are used

For text processing, we use [MeCab](https://taku910.github.io/mecab/)

## Usage
Currently, the project is not deployed anywhere, so to use the service,
you will need to follow the steps below in the development section to
get the server running.
1. Upload a file containing japanese text to the server. Currently allowed
file formats:
* `.epub`
* `.txt` with utf-8 encoding. If you have a `.txt` file with different encoding,
there are many ways to change the encoding. I use this: https://github.com/Frederick-S/aozora-bunko-utf8
2. The server will redirect you to a page showing you information about the ebook.
You can then also click the 'See more details' button to see all the generated
data, including a list of all the words used together with how many occurences there
are for each word, and the same for the characters as well.

## Development
1. Clone repository: `git clone https://github.com/christofferaakre/japanese-ebook-analysis.git`
2. Make sure you have `mecab` and `mecab-ipadic-neologd` set up on your system. See
[http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/](http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/)
<br>(Only required if you will actually upload ebooks or run the `analyse_epub.py` script),
which you will not need to do to contribute to other parts of the app.
for a good guide on how to set it up.
3. Install python dependencies: `pip install -r requirements.txt`
4. Install other dependencies (these all need to be in your system path):
    * `pandoc`
5. Run `./app.py` to start the flask dev server

## Contributing
I'm very happy for any happy contributions! Before contributing, please
have a look at
[CONTRIBUTING.md](https://github.com/christofferaakre/japanese-ebook-analysis/blob/master/CONTRIBUTING.md).<br>

To see what needs work on, have a look at the repo's
[Issues](https://github.com/christofferaakre/japanese-ebook-analysis/issues)
and its
[Pull requests](https://github.com/christofferaakre/japanese-ebook-analysis/pulls).<br>

Feel free to submit your own issue or pull request about a new feature or anything
else. When submitting a pull request, don't be afraid to modify any of the files;
I'm not very attached to the coding style used in the repo.
