# Imports
import flask
from werkzeug.utils import secure_filename
import hashlib
from random import randint
import json
import os
import sqlite3

# Flask configurations
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'c40a650584b50cb7d928f44d58dcaffc'

# My configurations
submission_schema = '''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    author INTEGER NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    path TEXT NOT NULL
  );
'''
db_path = 'Data/submissions.db'

# Initiate Database if not exists
def __init__():
    if os.path.isfile(db_path):
        pass
    else:
        connection = sqlite3.connect(db_path)
        connection.executescript(submission_schema)
        connection.commit()
        connection.close()

# Back end handlers
def getMD5(plaintext):
    m = md5()
    m.update(plaintext.encode('utf-8'))
    hash = str(m.hexdigest())
    return hash
def submit_to_db(author, title, abstract, pdf):
    try:
        # Generate filename
        pdf_filepath = 'static/uploads/submissions/' + author + '_' + title + '_' + str(randint(1000, 9999)) + '.pdf'
        # Save file
        pdf.save(pdf_filepath)
        # Add to database
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('INSERT INTO submissions (author, title, abstract, path) VALUES (?,?,?,?)',
        (author, title, abstract, pdf_filepath))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

# API handlers (POST)
@app.route('/api/submit', methods=('POST',))
def submit_handler():
    author = flask.request.form['author']
    title = flask.request.form['title']
    abstract = flask.request.form['abstract']
    pdf = flask.request.files['pdf']
    submit_to_db(author, title, abstract, pdf)
    return flask.redirect('/ty.html')

#Run app
if __name__=="__main__":
    app.run(debug=True, port=3003, host="127.0.0.1")
