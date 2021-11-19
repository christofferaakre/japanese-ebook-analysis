#!/usr/bin/env python3
import os

from flask import Flask, flash, request, redirect, url_for, jsonify
from flask.templating import render_template
from werkzeug.utils import secure_filename

from utils import get_books, get_book

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'epub'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


x = 3
y = 5
z = x + y

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''

# @app.route('/books', methods=['GET'])
@app.route('/books', methods=['GET', 'POST'])
def show_books():
    if request.method != 'GET':
     return redirect('/')

    books = get_books()
    return render_template('books.html', books=books)

@app.route('/api/books/<string:text>', methods=['GET'])
def return_json(text):
   book_data = get_book(text)
   return jsonify(book_data)

if __name__ == '__main__':
    app.run(debug=True)
