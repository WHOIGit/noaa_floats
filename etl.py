from pandas import read_csv

from orm import Base, Float, Point
from utils import parse_date_time, xa

DATA_COLS='ID,DATE,TIME,LAT,LON,PRESS,U,V,TEMP,Q_TIME,Q_POS,Q_PRESS,Q_VEL,Q_TEMP'.split(',')
METADATA_COLS='ID,PRINCIPAL_INVESTIGATOR,ORGANIZATION,EXPERIMENT,1st_DATE,1st_LAT,1st_LON,END_DATE,END_LAT,END_LON,TYPE,FILENAME'.split(',')

DATA_SEPARATOR=r'\s+'
METADATA_SEPARATOR=r'(?:\b|\))(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])'

CHUNK_SIZE=10000

DATABASE_URL='postgresql://floats:floats@localhost/floats'

def etl_data():
    # read CSV containing all point data from all floats
    n = 0
    for chunk in read_csv('./data/floats.dat',sep=DATA_SEPARATOR,iterator=True,chunksize=CHUNK_SIZE):
        chunk.fillna(0,inplace=True) # FIXME handle NA's better, e.g., with NULLs
        with xa(DATABASE_URL) as session:
            for index, row in chunk.iterrows():
                pt = Point(**{
                    'float_id': row.ID,
                    'date': parse_date_time(row.DATE, row.TIME),
                    'lat': row.LAT,
                    'lon': row.LON,
                    'pressure': row.PRESS,
                    'u': row.U,
                    'v': row.V,
                    'temperature': row.TEMP,
                    'q_time': row.Q_TIME,
                    'q_pos': row.Q_POS,
                    'q_press': row.Q_PRESS,
                    'q_vel': row.Q_VEL,
                    'q_temp': row.Q_TEMP
                })
                session.add(pt)
        n += len(chunk.index)
        print 'added %d point(s)...' % n


def etl_metadata():
   df = read_csv('./data/floats_dirfl.dat',sep=METADATA_SEPARATOR,index_col=False)
   print 'adding %s float(s)...' % len(df.index)
   with xa(DATABASE_URL, Base.metadata) as session:
       for index, row in df.iterrows():
           flt = Float(**{
               'id': row.ID,
               'pi': row.PRINCIPAL_INVESTIGATOR,
               'organization': row.ORGANIZATION,
               'experiment': row.EXPERIMENT,
               'start_date': row['1st_DATE'],
               'start_lat': row['1st_LAT'],
               'start_lon': row['1st_LON'],
               'end_date': row.END_DATE,
               'end_lat': row.END_LAT,
               'end_lon': row.END_LON,
               'type': row.TYPE,
               'filename': row.FILENAME
           })
           session.add(flt)

def etl_tracks():
    with xa(DATABASE_URL) as session:
        n = 0
        for f in session.query(Float).order_by(Float.id):
            lon_adj = 0
            prev_lon = 0
            ps = []
            for p in f.points:
                if p.lon != -999 and p.lat != -99: # exclude noninformative points
                    lat, lon = float(p.lat), float(p.lon)
                    # what if float just crossed the int'l date line
                    if prev_lon < -90 and lon > 90: # going west?
                        lon_adj -= 360
                    elif prev_lon > 90 and lon < -90: # going east?
                        lon_adj += 360
                    ps.append('%.6f %.6f' % (lon + lon_adj, lat))
                    prev_lon = lon
            if len(ps) == 1: # need more than one point
                ps = ps + ps
            ls = 'LINESTRING(%s)' % (','.join(ps))
            print '%d: Float %ld %d points' % (n, f.id, len(ps))
            f.track = ls
            n += 1
            if n % 100 == 0:
                session.commit()

def etl():
    etl_metadata()
    etl_data()
    etl_tracks()

if __name__=='__main__':
    etl()
