from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship
from geoalchemy2 import Geometry

"""
Object-relational model of floats database.
See etl.py for extract/transform/load procedure
"""

Base = declarative_base()

class Float(Base):
    """
    Represents a single NOAA float from the database.
    """
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
    track = Column(Geometry('LINESTRING')) # track geometry

    def __repr__(self):
        return '<Float #%d>' % (self.id)

    def get_metadata(self):
        """
        Return float metadata as dict
        """
        return {
            'ID': self.id,
            'PRINCIPAL_INVESTIGATOR': self.pi,
            'ORGANIZATION': self.organization,
            'EXPERIMENT': self.experiment,
            '1st_DATE': self.start_date,
            '1st_LAT': self.start_lat,
            '1st_LON': self.start_lon,
            'END_DATE': self.end_date,
            'END_LAT': self.end_lat,
            'END_LON': self.end_lon,
            'TYPE': self.type,
            'FILENAME': self.filename
        }


class Point(Base):
    """
    Represents a single point along a float track
    """
    __tablename__ = 'points'

    id = Column(BigInteger, primary_key=True)
    float_id = Column(BigInteger, ForeignKey('floats.id'))
    date = Column(DateTime) # DATE, TIME
    lat = Column(Numeric) # latitude
    lon = Column(Numeric) # longitude
    pressure = Column(Numeric) # pressure
    u = Column(Numeric) # velocity u component
    v = Column(Numeric) # velocity v component
    temperature = Column(Numeric) # temperature
    q_time = Column(Integer) # quality annotation on date/time
    q_pos = Column(Integer) # quality annotation on lat/lon
    q_press = Column(Integer) # quality annotation on pressure
    q_vel = Column(Integer) # quality annotation on u/v
    q_temp = Column(Integer) # quality annotation on temperature

    # establish Float.points relationship
    float = relationship('Float',
                         backref=backref('points', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Point %.4f %.4f %.2f>' % (self.lat, self.lon, self.pressure)
