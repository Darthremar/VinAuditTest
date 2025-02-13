from sqlalchemy import Column, Integer, String
from ..database import Base

class CarBasicInfo(Base):
    __tablename__ = 'car_basic_info'
    
    vin = Column(String, primary_key=True)
    year = Column(Integer, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    trim = Column(String, nullable=True) 