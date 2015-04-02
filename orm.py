from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

class Float(Base):
    __tablename__ = 'floats'

    id = Column(Integer, primary_key=True) # ID
    pi = Column(String) # PRINCIPAL_INVESTIGATOR
    experiment = Column(String) # EXPERIMENT
    start_date = Column(DateTime) # 1st_DATE
    start_lat = Column(Numeric) # 1st_LAT
    start_lon = Column(Numeric) # 1st_LON
    end_date = Column(DateTime) # END_DATE
    end_lat = Column(Numeric) # END_LAT
    end_lon = Column(Numeric) # END_LON
    type = Column(String) # TYPE
    filename = Column(String) # FILENAME

class Point(Base):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime) # DATE, TIME
    lat = Column(Numeric)
    lon = Column(Numeric)
    pressure = Column(Numeric)
    u = Column(Numeric) # velocity
    v = Column(Numeric) # velocity
    temperature = Column(Numeric)
    q_time = Column(Integer)
    q_pos = Column(Integer)
    q_press = Column(Integer)
    q_vel = Column(Integer)
    q_temp = Column(Integer)

    float = relationship('Float',
                         backref=backref('points', cascade='all, delete-orphan'))
