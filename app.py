#!/usr/bin/env python3
import os

from flask import Flask, flash, request, redirect, url_for, jsonify
from flask.templating import render_template
from werkzeug.utils import secure_filename

from book import analyse_ebook
from utils import get_books, get_book

from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def upload_file():
    return render_template('upload_file.html')

@app.route('/books', methods=['GET'])
def show_books():
    books = get_books()
    return render_template('books.html', books=books)

@app.route('/books/<string:hash>', methods=['GET'])
def show_book(hash: str):
    book_data = get_book(hash)
    return render_template('books.html', books=[book_data])

@app.route('/api/books/<string:hash>', methods=['GET'])
def return_json(hash: str):
   book_data = get_book(hash)
   return jsonify(book_data)


@app.route('/upload', methods=['POST'])
def upload_ebook():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']

    if file.filename == '':
                flash('No selected file')
                return redirect('/')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        book_data = analyse_ebook(save_path, fallback_title=filename)
        file_hash = book_data['file_hash']
        return redirect(f'/books/{file_hash}')

if __name__ == '__main__':
    app.run(debug=True)
