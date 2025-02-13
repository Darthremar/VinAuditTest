from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

class VehicleStatus(Base):
    __tablename__ = 'vehicle_status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, nullable=False)
    used = Column(Boolean, nullable=False)
    certified = Column(Boolean, nullable=True) 