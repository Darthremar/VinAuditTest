from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..interfaces.repository import ICarRepository
from ..models.car_basic_info import CarBasicInfo
from ..models.listing_details import ListingDetails
from ..models.dealer_info import DealerInfo
from ..models.vehicle_specs import VehicleSpecs
from ..models.vehicle_status import VehicleStatus
from ..models.seller_info import SellerInfo

class CarRepository(ICarRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_vin(self, vin: str) -> Optional[Dict[str, Any]]:
        car_info = self.db.query(CarBasicInfo).filter(CarBasicInfo.vin == vin).first()
        if not car_info:
            return None
            
        return {
            "car_info": car_info,
            "dealer_info": self.db.query(DealerInfo).filter(DealerInfo.vin == vin).first(),
            "listing_details": self.db.query(ListingDetails).filter(ListingDetails.vin == vin).first(),
            "vehicle_specs": self.db.query(VehicleSpecs).filter(VehicleSpecs.vin == vin).first(),
            "vehicle_status": self.db.query(VehicleStatus).filter(VehicleStatus.vin == vin).first(),
            "seller_info": self.db.query(SellerInfo).filter(SellerInfo.vin == vin).first()
        }

    def get_with_filters(self, make: str = '', model: str = '', year: Optional[int] = None, offset: int = 0, limit: int = 100) -> List[Any]:
        query = self.db.query(
            CarBasicInfo,
            ListingDetails,
            DealerInfo
        ).join(
            ListingDetails,
            CarBasicInfo.vin == ListingDetails.vin
        ).join(
            DealerInfo,
            CarBasicInfo.vin == DealerInfo.vin
        )
        
        if make:
            query = query.filter(CarBasicInfo.make.ilike(make))
        if model:
            query = query.filter(CarBasicInfo.model.ilike(model))
        if year:
            query = query.filter(CarBasicInfo.year == year)
        
        return query.offset(offset).limit(limit).all()

    def get_sample_listings(self, year: int, make: str, model: str, limit: int = 100) -> List[Any]:
        return self.db.query(
            CarBasicInfo.year, 
            CarBasicInfo.make, 
            CarBasicInfo.model, 
            ListingDetails.listing_price, 
            ListingDetails.listing_mileage, 
            DealerInfo.dealer_city, 
            DealerInfo.dealer_state
        ).join(
            ListingDetails, CarBasicInfo.vin == ListingDetails.vin
        ).join(
            DealerInfo, CarBasicInfo.vin == DealerInfo.vin
        ).filter(
            CarBasicInfo.year == year,
            CarBasicInfo.make.ilike(make),
            CarBasicInfo.model.ilike(model)
        ).limit(limit).all()

    def get_market_data(self, year: int, make: str, model: str) -> float:
        return self.db.query(
            func.avg(ListingDetails.listing_price)
        ).join(
            CarBasicInfo, CarBasicInfo.vin == ListingDetails.vin
        ).filter(
            CarBasicInfo.year == year,
            CarBasicInfo.make.ilike(make),
            CarBasicInfo.model.ilike(model)
        ).scalar()

    def get_mileage_data(self, year: int, make: str, model: str, state: Optional[str] = None) -> List[Any]:
        query = self.db.query(
            ListingDetails.listing_price,
            ListingDetails.listing_mileage
        ).join(
            CarBasicInfo, CarBasicInfo.vin == ListingDetails.vin
        ).filter(
            CarBasicInfo.year == year,
            CarBasicInfo.make.ilike(make),
            CarBasicInfo.model.ilike(model)
        )
        
        if state:
            query = query.join(
                DealerInfo, CarBasicInfo.vin == DealerInfo.vin
            ).filter(DealerInfo.dealer_state == state)
            
        return query.all()

    def get_distinct_makes(self) -> List[str]:
        return [make[0] for make in self.db.query(CarBasicInfo.make).distinct().all()]

    def get_distinct_models(self) -> List[str]:
        return [model[0] for model in self.db.query(CarBasicInfo.model).distinct().all()]

    def get_distinct_years(self) -> List[int]:
        return [year[0] for year in self.db.query(CarBasicInfo.year).distinct().order_by(CarBasicInfo.year.desc()).all()]

    def get_total_count(self, filters: Dict) -> int:
        query = self.db.query(CarBasicInfo)
        
        if filters.get('make'):
            query = query.filter(CarBasicInfo.make.ilike(filters['make']))
        if filters.get('model'):
            query = query.filter(CarBasicInfo.model.ilike(filters['model']))
        if filters.get('year'):
            query = query.filter(CarBasicInfo.year == filters['year'])
        
        return query.count() 