import json

from flask import Flask, Response, request, redirect, url_for
from flask import render_template

from query import query_data, get_track, get_metadata, METADATA_COLS
from query import choose_random_float

app = Flask(__name__)

@app.route('/')
def index():
    rendered = render_template('top.html')
    return Response(rendered, mimetype='text/html')

@app.route('/query.csv')
def serve_query_csv():
    left = float(request.args.get('left',-180))
    bottom = float(request.args.get('bottom',-90))
    right = float(request.args.get('right',180))
    top = float(request.args.get('top',90))
    low_pressure = float(request.args.get('low_pressure',0))
    high_pressure = float(request.args.get('high_pressure',9999))
    def line_generator():
        for line in query_data(left,bottom,right,top,low_pressure,high_pressure):
            yield line + '\n'
    return Response(line_generator(),mimetype='text/csv')

@app.route('/track/<int:float_id>')
def serve_track(float_id):
    track = get_track(float_id)
    return Response(json.dumps(track),mimetype='application/json')

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
    app.run(host='0.0.0.0',port=8080,debug=True)
