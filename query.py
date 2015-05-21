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

DEFAULT_START_DATE='1972-09-28'
DEFAULT_END_DATE='2015-01-01'

def point2csv(p):
    return '%ld,%s,%s,%f,%f,%f,%f,%f,%f,%d,%d,%d,%d,%d' % (
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

def filter_by_params(q,low_pressure=0,high_pressure=9999,start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE,experiment=None):
    if experiment is not None:
        q = q.filter(Float.experiment==experiment)
    q = q.filter(Float.points.any(and_(Point.pressure > low_pressure,
                                       Point.pressure < high_pressure,
                                       Point.date >= start_date,
                                       Point.date <= end_date)))
    return q

def filter_by_geom(q,geom):
    return q.filter(func.ST_Intersects(Float.track, geom))

def query_geom_data(geom,low_pressure=0,high_pressure=9999,start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE,experiment=None):
    """
    Return all floats data in CSV format for any float which
    intersects the given WKT geometry and pressure range
    """
    yield ','.join(DATA_COLS)
    with xa(DATABASE_URL) as session:
        q = session.query(Point).join(Float)
        q = filter_by_params(q,low_pressure,high_pressure,start_date,end_date,experiment)
        q = filter_by_geom(q,geom)
        for p in q:
            yield point2csv(p)

def query_data(low_pressure=0,high_pressure=9999,start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE,experiment=None):
    """
    Return all floats data in CSV format for any float which matches
    """
    yield ','.join(DATA_COLS)
    with xa(DATABASE_URL) as session:
        q = session.query(Point).join(Float)
        q = filter_by_params(q,low_pressure,high_pressure,start_date,end_date,experiment)
        for p in q:
            yield point2csv(p)

def get_track(float_id):
    """
    Return float track in WKT
    """
    with xa(DATABASE_URL) as session:
        for f in session.query(func.ST_AsText(Float.track)).filter(Float.id==float_id):
            return f[0]
    return 'LINESTRING(0 0,0 0)' # dummy geometry if float is not found

def query_floats(low_pressure=0,high_pressure=9999,start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE,experiment=None):
    """
    Return the IDs of all floats that intersect the given bounding box
    and pressure range.
    """
    with xa(DATABASE_URL) as session:
        q = session.query(Float)
        q = filter_by_params(q,low_pressure,high_pressure,start_date,end_date,experiment)
        float_ids = [f.id for f in q]
    return float_ids

def query_geom_floats(geom,low_pressure=0,high_pressure=9999,start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE,experiment=None):
    """
    Return the IDs of all floats that intersect the given WKT geometry
    and pressure range.
    """
    with xa(DATABASE_URL) as session:
        q = session.query(Float)
        q = filter_by_params(q,low_pressure,high_pressure,start_date,end_date,experiment)
        q = filter_by_geom(q,geom)
        float_ids = [f.id for f in q]
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

def all_experiments():
    with xa(DATABASE_URL) as session:
        return [_ for _ in session.query(Float.experiment).\
                    order_by(Float.experiment).\
                    distinct()]

# debug utilities

def count_floats():
    with xa(DATABASE_URL) as session:
        return session.query(Float.id).count()

def choose_random_float():
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).order_by(func.random()).limit(1):
            return f.id
    return None
