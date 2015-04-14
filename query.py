import numpy as np
from pandas import read_csv

CHUNK_SIZE=10000

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE,1st_LAT,1st_LON,END_DATE,END_LAT,END_LON,TYPE,FILENAME'.split(',')

DATA_SEPARATOR=r'\s+'
METADATA_SEPARATOR=r'\b(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])'

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
    for chunk in read_csv('./data/floats.dat',sep=DATA_SEPARATOR,iterator=True,chunksize=CHUNK_SIZE):
        df = chunk[chunk.ID == float_id]
        if len(df.index) > 0:
            for index, row in df.iterrows():
                track.append((float(row.LON),float(row.LAT)));
    return track

def get_metadata(float_id):
    df = read_csv('./data/floats_dirfl.dat',sep=METADATA_SEPARATOR,index_col=False)
    for index, row in df[df.ID == int(float_id)].iterrows():
        r = dict((c,row[c]) for c in METADATA_COLS)
        return r

# debug utilities

def choose_random_float():
    df = read_csv('./data/floats_dirfl.dat',sep=METADATA_SEPARATOR,index_col=False)
    return df.ix[np.random.choice(df.index)].ID


