# Imports
import flask
from werkzeug.utils import secure_filename
import hashlib
from random import randint
import json
import os
import sys
import sqlite3
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

# Flask configurations
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'c40a650584b50cb7d928f44d58dcaffc'

# My configurations
schema = '''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    email TEXT NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    path TEXT NOT NULL
  );
'''
db_path = 'Data/submissions.db'

# Initiate Database if not exists
if os.path.isfile(db_path):
    pass
else:
    connection = sqlite3.connect(db_path)
    connection.executescript(schema)
    connection.commit()
    connection.close()

# Back end handlers


def getMD5(plaintext):
    m = md5()
    m.update(plaintext.encode('utf-8'))
    hash = str(m.hexdigest())
    return hash


def submit_to_db(author, email, title, abstract, pdf):
    # Generate filename
    pdf_filepath = 'static/uploads/submissions/' + author + \
        '_' + title + '_' + str(randint(1000, 9999)) + '.pdf'
    # Save file
    pdf.save(pdf_filepath)
    # Add to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO submissions (author, email, title, abstract, path) VALUES (?,?,?,?,?)',
                (author, email, title, abstract, pdf_filepath))
    conn.commit()
    conn.close()
    return pdf_filepath

def notify_email(name, address, link):
    SMTPserver = 'us2.smtp.mailhostbox.com'
    sender = 'no-reply.ecgi@duti.tech'
    destination = [address, 'youthgenerations2022@gmail.com']

    username = 'no-reply.ecgi@duti.tech'
    password = 'CYLyeLtq7'

    text_subtype = 'plain'

    content = """
    Hello """ + name + """,\n

    We have received your submission. The upload is accessible at: 
    """ + str(link) + """\n
    Sincerely,
    Youth Generations Bot
    """

    subject = 'Your ECGI entry'

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(True)
        conn.login(username, password)
        try:
            conn.sendmail(sender, destination, msg)
        finally:
            conn.quit()
    except:
        sys.exit("Mail failed")


# API handlers (POST)
@app.route('/api/submit', methods=('POST',))
def submit_handler():
    # Initiate Database if not exists
    if os.path.isfile(db_path):
        pass
    else:
        connection = sqlite3.connect(db_path)
        connection.executescript(schema)
        connection.commit()
        connection.close()
    # Get forms
    author = flask.request.form['author']
    email = flask.request.form['email']
    title = flask.request.form['title']
    abstract = flask.request.form['abstract']
    pdf = flask.request.files['pdf']
    # Proc
    pdf_filepath = 'https://youthgenerations.org/' + str(submit_to_db(author, email, title, abstract, pdf))
    notify_email(author, email, pdf_filepath)
    return flask.redirect('/ty.html')


@app.route('/api/subscribe', methods=('POST',))
def subscribe_handler():
    email = flask.request.form['email']
    email_list_path = 'Data/subscriptions.txt'
    # Just in case deleted by accident
    if os.path.isfile(email_list_path):
        pass
    else:
        open(email_list_path, 'w').write('')
    # Put info
    open(email_list_path, 'a').write(email)
    return flask.redirect('/ty.html')


# Run app
if __name__ == "__main__":
    app.run(debug=True, port=3003, host="127.0.0.1")
