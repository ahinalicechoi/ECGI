# Imports
import flask
from werkzeug.utils import secure_filename
import hashlib
from random import randint
import json

# Flask configurations
app = Flask(__name__)
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
