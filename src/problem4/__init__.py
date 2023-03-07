import os
import sqlalchemy
from flask import Flask
from sqlalchemy.pool import SingletonThreadPool

basedir = os.path.abspath(os.path.dirname(__file__))

# init db connection
def init_connect_engine():
    db_url = 'sqlite:///' + os.path.join(basedir, "../", 'Wheather.db')
    engine = sqlalchemy.create_engine(db_url, poolclass=SingletonThreadPool)
    return engine

app = Flask(__name__)
db = init_connect_engine()

