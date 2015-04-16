import numpy as np
from pandas import read_csv
from sqlalchemy.sql.expression import func

from utils import xa, render_date, render_time
from orm import Float, Point
from etl import DATABASE_URL

CHUNK_SIZE=10000

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE,1st_LAT,1st_LON,END_DATE,END_LAT,END_LON,TYPE,FILENAME'.split(',')

DATA_SEPARATOR=r'\s+'
METADATA_SEPARATOR=r'(?:\b|\))(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])'

def query_data(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    yield ','.join(DATA_COLS)
    with xa(DATABASE_URL) as session:
        for p in session.query(Point).\
            filter(Point.lon > left).\
            filter(Point.lon < right).\
            filter(Point.lat > bottom).\
            filter(Point.lat < top).\
            filter(Point.pressure > low_pressure).\
            filter(Point.pressure < high_pressure):
            yield '%ld,%s,%s,%f,%f,%f,%f,%f,%f,%d,%d,%d,%d,%d' % (
                p.id,
                render_date(p.date),
                render_time(p.date),
                p.lat,
                p.lon,
                p.pressure,
                p.u,
                p.v,
                p.temperature,
                p.q_time,
                p.q_pos,
                p.q_press,
                p.q_vel,
                p.q_temp
                )

def get_track(float_id):
    track = []
    float_id = int(float_id)
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).filter(Float.id==float_id):
            for p in f.points:
                lon = float(p.lon)
                lat = float(p.lat)
                track.append((lon, lat))
        return track
    return None

def get_metadata(float_id):
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).filter(Float.id==float_id):
            return f.get_metadata()
    return {}

# debug utilities

def choose_random_float():
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).order_by(func.random()).limit(1):
            return f.id
    return None


