from sqlalchemy import Column, Integer, String
from ..database import Base

class VehicleSpecs(Base):
    __tablename__ = 'vehicle_specs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, nullable=False)
    style = Column(String, nullable=True)
    driven_wheels = Column(String, nullable=True)
    engine = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
    exterior_color = Column(String, nullable=True)
    interior_color = Column(String, nullable=True) 