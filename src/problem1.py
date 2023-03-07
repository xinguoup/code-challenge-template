import os
import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))

# For Problem 1, I will choose to use SQLite to create our database

# create our database if it does not exist
db_path = os.path.join(basedir, "../", "Wheather.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# create station_info table in our database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS station_info (
        id INTEGER PRIMARY KEY,
        station_name TEXT,
        state_loc TEXT
    )
''')

# create wheather_record table in our database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wheather_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER NOT NULL,
        date DATE,
        max_temperature REAL NOT NULL,
        min_temperature REAL NOT NULL,
        precipitation_amount REAL NOT NULL,
        FOREIGN KEY (station_id) REFERENCES station_info (id)
    )
''')

conn.commit()
conn.close()


