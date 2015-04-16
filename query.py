import numpy as np
from pandas import read_csv
from sqlalchemy.sql.expression import func

from utils import xa
from orm import Float
from etl import DATABASE_URL

CHUNK_SIZE=10000

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE,1st_LAT,1st_LON,END_DATE,END_LAT,END_LON,TYPE,FILENAME'.split(',')

DATA_SEPARATOR=r'\s+'
METADATA_SEPARATOR=r'(?:\b|\))(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])'

def query_data(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    yield ','.join(DATA_COLS)
    for chunk in read_csv('./data/floats.dat',sep=DATA_SEPARATOR,iterator=True,chunksize=CHUNK_SIZE):
        df = chunk[(chunk.LON > left) &
                   (chunk.LON < right) &
                   (chunk.LAT > bottom) &
                   (chunk.LAT < top) &
                   (chunk.PRESS > low_pressure) &
                   (chunk.PRESS < high_pressure)]
        if len(df.index) > 0:
            for index, row in df.iterrows():
                yield ','.join(map(str,[row[c] for c in DATA_COLS]))

def get_track(float_id):
    track = []
    float_id = int(float_id)
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).filter(Float.id==float_id):
            for p in f.points:
                track.append((float(p.lon), float(p.lat)))
        return track
    return None

def get_metadata(float_id):
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).filter(Float.id==float_id):
            return {
                'ID': f.id,
                'PRINCIPAL_INVESTIGATOR': f.pi,
                'ORGANIZATION': f.organization,
                'EXPERIMENT': f.experiment,
                '1st_DATE': f.start_date,
                '1st_LAT': f.start_lat,
                '1st_LON': f.start_lon,
                'END_DATE': f.end_date,
                'END_LAT': f.end_lat,
                'END_LON': f.end_lon,
                'TYPE': f.type,
                'FILENAME': f.filename
            }
    return {}

# debug utilities

def choose_random_float():
    with xa(DATABASE_URL) as session:
        for f in session.query(Float).order_by(func.random()).limit(1):
            return f.id
    return None


