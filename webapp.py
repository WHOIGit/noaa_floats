import json

from flask import Flask, Response, request, redirect, url_for
from flask import render_template

from query import query_data, query_geom_data, query_floats, all_floats, query_geom_floats, get_track, get_metadata, METADATA_COLS
from query import choose_random_float

app = Flask(__name__)

@app.route('/')
def index():
    rendered = render_template('top.html')
    return Response(rendered, mimetype='text/html')

def get_request_args():
    low_pressure = request.args.get('low_pressure',0)
    high_pressure = request.args.get('high_pressure',9999)
    start_date = request.args.get('start_date','1972-09-28')
    end_date = request.args.get('end_date','2015-01-01')
    return low_pressure, high_pressure, start_date, end_date

# simple queries

@app.route('/all_floats.json')
def all_floats_json():
    float_ids = all_floats()
    return Response(json.dumps(float_ids),mimetype='application/json')

@app.route('/query_floats.json')
def query_floats_json():
    low_pressure, high_pressure, start_date, end_date = get_request_args()
    float_ids = query_floats(low_pressure,high_pressure,start_date,end_date)
    return Response(json.dumps(float_ids),mimetype='application/json')

@app.route('/query.csv')
def serve_query_csv():
    low_pressure, high_pressure, start_date, end_date = get_request_args()
    def line_generator():
        for line in query_data(low_pressure, high_pressure, start_date, end_date):
            yield line + '\n'
    return Response(line_generator(),mimetype='text/csv')

# geospatial queries

def get_geom_request_args():
    low_pressure, high_pressure, start_date, end_date = get_request_args()
    geom = request.args.get('geometry',None)
    return geom, low_pressure, high_pressure, start_date, end_date

@app.route('/query_geom.csv')
def serve_query_geom_csv():
    geom, low_pressure, high_pressure, start_date, end_date = get_geom_request_args()
    def line_generator():
        for line in query_geom_data(geom, low_pressure, high_pressure, start_date, end_date):
            yield line + '\n'
    return Response(line_generator(),mimetype='text/csv')

@app.route('/query_geom_floats.json')
def serve_geom_floats_json():
    geom, low_pressure, high_pressure, start_date, end_date = get_geom_request_args()
    float_ids = query_geom_floats(geom,low_pressure,high_pressure,start_date,end_date)
    return Response(json.dumps(float_ids),mimetype='application/json')

@app.route('/track/<int:float_id>')
def serve_track(float_id):
    track = get_track(float_id) # wkt
    return Response(json.dumps({
        'track': track
    }),mimetype='application/json')

@app.route('/metadata/<int:float_id>')
def serve_metadata(float_id):
    d = get_metadata(float_id)
    return Response(json.dumps(d),mimetype='application/json')

@app.route('/float/<int:float_id>')
def float_page(float_id):
    context = {
        'float_id': float_id,
        'metadata_cols': METADATA_COLS,
        'metadata': get_metadata(float_id)
    }
    rendered = render_template('float.html',**context)
    return Response(rendered, mimetype='text/html')

@app.route('/random_float')
def random_float_page():
    float_id = choose_random_float()
    return redirect(url_for('float_page',float_id=float_id))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True,processes=12)
