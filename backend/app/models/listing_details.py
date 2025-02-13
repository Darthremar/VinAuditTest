from sqlalchemy import Column, Integer, String, Numeric, Date
from ..database import Base

class ListingDetails(Base):
    __tablename__ = 'listing_details'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, nullable=False)
    listing_price = Column(Numeric, nullable=True)
    listing_mileage = Column(Integer, nullable=True)
    listing_status = Column(String, nullable=True)
    first_seen_date = Column(Date, nullable=True)
    last_seen_date = Column(Date, nullable=True)
    dealer_vdp_last_seen_date = Column(Date, nullable=True) 