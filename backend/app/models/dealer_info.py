from sqlalchemy import Column, Integer, String
from ..database import Base

class DealerInfo(Base):
    __tablename__ = 'dealer_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, nullable=False)
    dealer_name = Column(String, nullable=True)
    dealer_street = Column(String, nullable=True)
    dealer_city = Column(String, nullable=True)
    dealer_state = Column(String, nullable=True)
    dealer_zip = Column(String, nullable=True) 