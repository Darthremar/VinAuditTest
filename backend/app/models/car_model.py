from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from ..database import Base

class Car(Base):
    __tablename__ = 'cars'
    
    vin = Column(String, primary_key=True)
    year = Column(Integer, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    trim = Column(String, nullable=True)
    dealer_name = Column(String, nullable=True)
    dealer_street = Column(String, nullable=True)
    dealer_city = Column(String, nullable=True)
    dealer_state = Column(String, nullable=True)
    dealer_zip = Column(String, nullable=True)
    listing_price = Column(Numeric, nullable=True)
    listing_mileage = Column(Integer, nullable=True)
    used = Column(Boolean, nullable=False)
    certified = Column(Boolean, nullable=True)
    style = Column(String, nullable=True)
    driven_wheels = Column(String, nullable=True)
    engine = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
    exterior_color = Column(String, nullable=True)
    interior_color = Column(String, nullable=True)
    seller_website = Column(String, nullable=True)
    first_seen_date = Column(Date, nullable=True)
    last_seen_date = Column(Date, nullable=True)
    dealer_vdp_last_seen_date = Column(Date, nullable=True)
    listing_status = Column(String, nullable=True)
    