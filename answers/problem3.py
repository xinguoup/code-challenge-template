import sqlite3

conn = sqlite3.connect('Wheather.db')
cursor = conn.cursor()
cursor.execute('''DROP TABLE IF EXISTS avg_report''')

# create data analysis report table in our database

# Design a new data model to store the results
cursor.execute('''
        CREATE TABLE IF NOT EXISTS avg_report(
        year INTEGER NOT NULL,
        station_id INTEGER NOT NULL,
        avg_max_temperature NUMERIC(10, 2),
        avg_min_temperature NUMERIC(10, 2),
        precipitation_total NUMERIC(10, 2),
        PRIMARY KEY (station_id, year))
''')

# insert the analysis result to this table
cursor.execute('''
    INSERT INTO avg_report(year, station_id, avg_max_temperature, avg_min_temperature, precipitation_total)
    SELECT strftime('%Y', date), 
           station_id,
           ROUND(AVG(max_temperature), 2), 
           ROUND(AVG(min_temperature), 2), 
           ROUND(SUM(precipitation_amount) / 10, 2)
    FROM wheather_record
    WHERE max_temperature <> -9999 AND min_temperature <> -9999
    GROUP BY strftime('%Y', date), station_id   
''')

conn.commit()
conn.close()



# sql_str = "SELECT * FROM avg_report LIMIT 10"
# cur_res = cursor.execute(sql_str).fetchall()
# print(cur_res)