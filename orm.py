from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

class Float(Base):
    __tablename__ = 'floats'

    id = Column(BigInteger, primary_key=True) # ID
    pi = Column(String) # PRINCIPAL_INVESTIGATOR
    organization = Column(String) # ORGANIZATION
    experiment = Column(String) # EXPERIMENT
    start_date = Column(DateTime) # 1st_DATE
    start_lat = Column(Numeric) # 1st_LAT
    start_lon = Column(Numeric) # 1st_LON
    end_date = Column(DateTime) # END_DATE
    end_lat = Column(Numeric) # END_LAT
    end_lon = Column(Numeric) # END_LON
    type = Column(String) # TYPE
    filename = Column(String) # FILENAME

    def __repr__(self):
        return '<Float #%d>' % (self.id)

class Point(Base):
    __tablename__ = 'points'

    id = Column(BigInteger, primary_key=True)
    float_id = Column(BigInteger, ForeignKey('floats.id'))
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

    def __repr__(self):
        return '<Point %.4f %.4f %.2f>' % (self.lat, self.lon, self.pressure)
