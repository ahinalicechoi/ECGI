# Imports
import flask
from werkzeug.utils import secure_filename
import hashlib
from random import randint
import json
import os
import sys
import sqlite3
# SMTP stuff
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
    category INTEGER NOT NULL,
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


def submit_to_db(author, email, title, abstract, category, pdf):
    # Generate filename
    pdf_filepath = 'static/uploads/submissions/' + secure_filename((author + \
        '_' + title + '_' + str(randint(1000, 9999)) + '.pdf'))
    # Save file
    pdf.save(pdf_filepath)
    # Add to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO submissions (author, email, title, abstract, category, path) VALUES (?,?,?,?,?,?)',
                (author, email, title, abstract, int(category), pdf_filepath))
    conn.commit()
    conn.close()
    return pdf_filepath

def notify_email(title, abstract, name, address, category, link):
    # Convert category from int to string
    if category == 1:
        category = "Year 4-6"
    elif category == 2:
        category = "Year 7-9"
    elif category == 3:
        category = "Year 10-13"
    else:
        category = "Invalid"

    # Email testing
    SMTPserver = 'smtp.gmail.com'
    sender = 'ecgi@youthgenerations.org'
    destinations = [address, 'youthgenerations2022@gmail.com', 'ecgi@youthgenerations.org', 'acheong@student.dalat.org']

    username = 'youthgenerations.dev@gmail.com'
    password = 'HIDDEN'
    text_subtype = 'plain'

    subject = 'Your ECGI entry'

    content = \
    "Hello " + name + ",\n" + \
    "We have received your submission. The upload is accessible at: " + str(link) + \
    "\n\nTitle: " + title + \
    "\nAbstract: \n" + abstract + \
    "\n\nYear group: " + category +\
    """\n\n
    Sincerely,
    Youth Generations Bot
    """

    try:
        # Make a MIMETEXT msg and set Subject, From, To
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(destinations)
        # Make SMTP connection to SMTPserver at port 587 with tls. then login
        # with username and password
        s = SMTP(SMTPserver, 587)
        # Set debug true
        s.debuglevel = True
        s.starttls()
        s.login(username, password)
        try:
            # Send the message from the sender to destinations with message
            s.sendmail(sender, destinations, msg.as_string())
            print("Mail sent")
        except:
            print("Sending failed")
    except:
        print("Connection failed")


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
    category = int(flask.request.form['category'])
    pdf = flask.request.files['pdf']
    # Proc
    pdf_filepath = submit_to_db(author, email, title, abstract, category, pdf)
    full_filepath = 'https://youthgenerations.org/' + pdf_filepath
    notify_email(title, abstract, author, email, category, full_filepath)
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
