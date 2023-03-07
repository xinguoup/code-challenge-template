import os
import sys
import json
import datetime
from flask import Flask, request

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)
import db_utils

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "introduce": "this is Rest API",
        "apis": {
            "GET":[
                {"/api/weather": "Get Weather Data"},
                {"/api/weather/stats": "Get Analysis Data"}
            ]
        }
    }
    return json.dumps(data)


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """
    Gets paginated weather from wheather_record
    Returns: JSON object
    """
    args = request.args
    rep = {
        "code": 0,
        "err_msg": "",
        "data": []
    }

    station_id = date = None
    if args.get('station_id'):
        station_id = ('station_id', args.get('station_id'))
    if args.get('date'):
        date = ('date(date)', datetime.datetime.strptime(args.get('date'), "%Y%m%d").date())
    
    # request check
    if not station_id and not date:
        rep["code"] = 1
        rep["err_msg"] = "station_id or date must set one"
        return json.dumps(rep)

    limit = args.get('limit', 10)
    offset = args.get('offset', 0)

    # get date from db
    data = db_utils.get_data_wheather_record_by_station_id_and_date([station_id, date], limit, offset)
    rep['data'] = data
    
    return json.dumps(rep)


@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    """
    Gets paginated weather stats from avg_report
    Returns: JSON object
    """
    args = request.args
    rep = {
        "code": 0,
        "err_msg": "",
        "data": []
    }
    station_id = year = None
    if args.get('station_id'):
        station_id = ('station_id', args.get('station_id'))
    if args.get('year'):
        year = ('year', args.get('year'))

    # request check
    if not station_id and not date:
        rep["code"] = 1
        rep["err_msg"] = "station_id or year must set one"
        return json.dumps(rep)

    limit = args.get('limit', 10)
    offset = args.get('offset', 0)

    # get date from db
    data = db_utils.get_data_avg_report_by_station_id_and_year([station_id, year], limit, offset)
    rep['data'] = data

    return json.dumps(rep)


def create_app():
    app.run()


if __name__ == '__main__':
    app.run()