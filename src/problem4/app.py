import json
import datetime
import db_utils
from flask import Flask, request, abort, jsonify

# from utils import generate_where_clause, get_data

app = Flask(__name__)

WX_SCHEMA = 'wx_schema'
YLD_SCHEMA = 'yld_schema'
WX_TABLE = 'wx_data'
YLD_TABLE = 'yld_data'
AVG_TABLE = 'avg_table'


@app.route('/')
def index():
    data = {
        "introduce": "this is Rest API",
        "apis": {
            "GET":[
                {"/api/weather": "Get all weather data"},
                {"/api/yield": "Get all weather data"}
            ]
        }
    }
    return json.dumps(data)


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """
    Gets paginated weather from wx_table
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
    
    offset = args.get('offset', 0)
    limit = args.get('limit', 10)
    
    # get date from db
    data = db_utils.get_data_wheather_record_by_station_id_and_date([station_id, date], limit, offset)
    rep['data'] = data
    
    return json.dumps(rep)


if __name__ == '__main__':
    app.run()