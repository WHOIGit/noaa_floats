from pandas import read_csv

left,bottom,right,top=[-69.73895843749992, 37.59310012248169, -62.5319271874999, 41.52151087392275]

CHUNK_SIZE=1000

cols='ID DATE TIME LAT LON PRESS U V TEMP Q_TIME Q_POS Q_PRESS Q_VEL Q_TEMP'.split(' ')

print ','.join(cols)

for chunk in read_csv('./data/floats.dat',sep='\s+',iterator=True,chunksize=CHUNK_SIZE):
    df = chunk[(chunk.LON > left) & (chunk.LON < right) & (chunk.LAT > bottom) & (chunk.LAT < top)]
    if len(df.index) > 0:
        for index, row in df.iterrows():
            print ','.join(map(str,[row[c] for c in cols]))
