from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Journeys(Base):
    __tablename__ = 'journeys'
    deviceID = Column(Integer)
    lat = Column(Integer)
    lon = Column(Integer)
    timestamp = Column(DateTime())
    type = Column(String(10))
    galileo_auth = Column(Integer)
