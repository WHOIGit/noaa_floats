import json

from flask import Flask, Response, request

from query import query_data, get_track

app = Flask(__name__)

@app.route('/')
def index():
    return Response('<h1>Hello, world.</h1>',mimetype='text/html')

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

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
