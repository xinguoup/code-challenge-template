import os
import sys
import datetime
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "../"))
from problem4 import db

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

def generate_where_clause(where_condition):
    where_sql = ""
    for c in where_condition:
        if c:
            if where_sql:
                where_sql += "AND"
            where_sql += " {}='{}' ".format(c[0], c[1])
    if where_sql:
        where_sql = "WHERE" + where_sql

    return where_sql
        
def generate_page_clause(limit=10, offset=0):
    page_sql = "limit {} offset {} ".format(limit, offset)
    return page_sql

def get_data_wheather_record_by_station_id_and_date(where_condition, limit=10, offset=0):
    where_sql = generate_where_clause(where_condition)
    page_sql = generate_page_clause(limit, offset)
    sql_str = "SELECT station_id,date,max_temperature,min_temperature,precipitation_amount FROM wheather_record " + where_sql + page_sql
    # print(sql_str)

    conn = db.connect()
    sql_res = conn.execute(sql_str).fetchall()
    # print(sql_res)
    conn.close()
    
    res = []
    for row in sql_res:
        item = {
            "station_id": row[0],
            "date": row[1],
            "max_temperature": row[2],
            "min_temperature": row[3],
            "precipitation_amount": row[4],
        }
        res.append(item)
    return res


def get_data_avg_report_by_station_id_and_year(where_condition, limit, offset):
    where_sql = generate_where_clause(where_condition)
    page_sql = generate_page_clause(limit, offset)

    sql_str = "SELECT station_id,year,avg_max_temperature,avg_min_temperature,precipitation_total FROM avg_report " + where_sql + page_sql
    # print(sql_str)

    conn = db.connect()
    sql_res = conn.execute(sql_str).fetchall()
    # print(sql_res)
    conn.close()

    res = []
    for row in sql_res:
        item = {
            "station_id": row[0],
            "year": row[1],
            "avg_max_temperature": row[2],
            "avg_min_temperature": row[3],
            "precipitation_total": row[4],
        }
        res.append(item)
    return res