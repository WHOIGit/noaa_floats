from pandas import read_csv

CHUNK_SIZE=10000

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE  1st_LAT  1st_LON ,END_DATE  END_LAT  END_LON,TYPE,FILENAME'.split(',')

def query_data(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    yield ','.join(DATA_COLS)
    for chunk in read_csv('./data/floats.dat',sep='\s+',iterator=True,chunksize=CHUNK_SIZE):
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
    for chunk in read_csv('./data/floats.dat',sep='\s+',iterator=True,chunksize=CHUNK_SIZE):
        df = chunk[chunk.ID == float_id]
        if len(df.index) > 0:
            for index, row in df.iterrows():
                track.append((float(row.LON),float(row.LAT)));
    return track

def split_key(d,key,regex,new_keys=None):
    if new_keys is None:
        new_keys = key.split(regex)
    for k,v in zip(new_keys,d[key].split(regex)):
        d[k] = v
    del d[key]

# \b(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])
def get_metadata(float_id):
    df = read_csv('data/floats_dirfl.dat',sep='\t\s*',index_col=False)
    for index, row in df[df.ID == int(float_id)].iterrows():
        d = dict((c,row[c]) for c in METADATA_COLS)
        # deal with funky keys
        split_key(d,'1st_DATE  1st_LAT  1st_LON ','  ',['START_DATE','START_LAT','START_LON'])
        split_key(d,'END_DATE  END_LAT  END_LON','  ')
        for k in ['START_LAT','END_LAT','START_LON','END_LON']:
            d[k] = float(d[k])
        return d
