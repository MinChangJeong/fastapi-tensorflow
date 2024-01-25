from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WaterUsage(Base):
    __tablename__ = "water_usage"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    date = Column(DateTime)
    amount = Column(Float)
    time = Column(Integer)
    tax = Column(Float)
