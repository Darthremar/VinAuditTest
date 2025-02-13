from sqlalchemy import Column, Integer, String
from ..database import Base

class SellerInfo(Base):
    __tablename__ = 'seller_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, nullable=False)
    seller_website = Column(String, nullable=True) 