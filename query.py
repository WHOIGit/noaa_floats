import numpy as np
from pandas import read_csv
from sqlalchemy import and_
from sqlalchemy.sql.expression import func

from utils import xa, render_date, render_time
from orm import Float, Point
from etl import DATABASE_URL

CHUNK_SIZE=10000

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE,1st_LAT,1st_LON,END_DATE,END_LAT,END_LON,TYPE,FILENAME'.split(',')

DATA_SEPARATOR=r'\s+'
METADATA_SEPARATOR=r'(?:\b|\))(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])'

def query_geom_data(geom,low_pressure=0,high_pressure=9999,start_date='1972-09-28',end_date='2015-01-01'):
    """
    Return all floats data in CSV format for any float which
    intersects the given WKT geometry and pressure range
    """
    yield ','.join(DATA_COLS)
    with xa(DATABASE_URL) as session:
        for p in session.query(Point).join(Float).\
            filter(func.ST_Intersects(Float.track, geom)).\
            filter(Float.points.any(and_(Point.pressure > low_pressure,
                                         Point.pressure < high_pressure,
                                         Point.date >= start_date,
                                         Point.date <= end_date))):
            yield '%ld,%s,%s,%f,%f,%f,%f,%f,%f,%d,%d,%d,%d,%d' % (
                p.float_id,
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
                p.q_temp)

def query_data(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    """
    Return all floats data in CSV format for any float which
    intersects the given bounding box and pressure range
    """
    for line in query_geom_data(func.ST_MakeEnvelope(left, bottom, right, top),low_pressure,high_pressure):
        yield line

def get_track(float_id):
    """
    Return float track in WKT
    """
    with xa(DATABASE_URL) as session:
        for f in session.query(func.ST_AsText(Float.track)).filter(Float.id==float_id):
            return f[0]
    return 'LINESTRING(0 0,0 0)' # dummy geometry if float is not found

def query_floats(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    """
    Return the IDs of all floats that intersect the given bounding box
    and pressure range.
    """
    with xa(DATABASE_URL) as session:
        float_ids = [f.id for f in session.query(Float).\
            filter(func.ST_Intersects(Float.track,
                                      func.ST_MakeEnvelope(left, bottom, right, top))).\
            filter(Float.points.any(and_(Point.pressure > low_pressure,
                                         Point.pressure < high_pressure)))]
    return float_ids

def query_geom_floats(geom,low_pressure=0,high_pressure=9999,start_date='1972-09-28',end_date='2015-01-01'):
    """
    Return the IDs of all floats that intersect the given WKT geometry
    and pressure range.
    """
    with xa(DATABASE_URL) as session:
        float_ids = [f.id for f in session.query(Float).\
            filter(func.ST_Intersects(Float.track, geom)).\
            filter(Float.points.any(and_(Point.pressure > low_pressure,
                                         Point.pressure < high_pressure,
                                         Point.date >= start_date,
                                         Point.date <= end_date)))]
    return float_ids

def all_floats():
    with xa(DATABASE_URL) as session:
        float_ids = [f.id for f in session.query(Float)]
    return float_ids

def get_metadata(float_id):
    """
    Return all metadata for the given float, as a dict
    """
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).filter(Float.id==float_id):
            return f.get_metadata()
    return {}

# debug utilities

def count_floats():
    with xa(DATABASE_URL) as session:
        return session.query(Float.id).count()

def choose_random_float():
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).order_by(func.random()).limit(1):
            return f.id
    return None
