from contextlib import contextmanager
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

def parse_date_time(date, time):
    dt = '%s %s' % (date, time)
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

@contextmanager
def xa(db_url, metadata=None):
    """Provide a transactional scope around a series of operations."""
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
