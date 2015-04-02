from pandas import read_csv

CHUNK_SIZE=1000

COLS='ID DATE TIME LAT LON PRESS U V TEMP Q_TIME Q_POS Q_PRESS Q_VEL Q_TEMP'.split(' ')

def query_data(left=-180,bottom=-90,right=180,top=90,low_pressure=0,high_pressure=9999):
    yield ','.join(COLS)
    for chunk in read_csv('./data/floats.dat',sep='\s+',iterator=True,chunksize=CHUNK_SIZE):
        df = chunk[(chunk.LON > left) &
                   (chunk.LON < right) &
                   (chunk.LAT > bottom) &
                   (chunk.LAT < top) &
                   (chunk.PRESS > low_pressure) &
                   (chunk.PRESS < high_pressure)]
        if len(df.index) > 0:
            for index, row in df.iterrows():
                yield ','.join(map(str,[row[c] for c in COLS]))
