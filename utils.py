from contextlib import contextmanager
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

"""
Utilities supporting the NOAA floats app
"""

# date/time roundtripping
def parse_date_time(date, time):
    """
    Parse the date and time from in the data file's format
    """
    dt = '%s %s' % (date, time)
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

def render_date(dt):
    """
    Format the date given a datetime
    """
    return dt.strftime('%Y-%m-%d')

def render_time(dt):
    """
    Format the time given a datetime
    """
    return dt.strftime('%H:%M:%S')

@contextmanager
def xa(db_url, metadata=None):
    """
    Provide a transactional scope around a series of database operations,
    that commits on success and rolls back on error.
    """
    if db_url.startswith('sqlite:'):
        engine = sqlalchemy.create_engine(db_url, isolation_level='SERIALIZABLE')
    else:
        engine = sqlalchemy.create_engine(db_url)
    if metadata is not None:
        metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
