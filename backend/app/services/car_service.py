from sqlalchemy.orm import Session
from ..models.car_basic_info import CarBasicInfo
from ..models.dealer_info import DealerInfo
from ..models.listing_details import ListingDetails
from ..models.vehicle_specs import VehicleSpecs
from ..models.vehicle_status import VehicleStatus
from ..models.seller_info import SellerInfo
from ..database import SessionLocal
import numpy as np
from sqlalchemy import func
from sklearn.linear_model import LinearRegression
from typing import List, Optional, Dict, Any
from ..repositories.car_repository import CarRepository
from .price_prediction_service import PricePredictionService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_car_details(vin):
    db = next(get_db())
    car_info = db.query(CarBasicInfo).filter(CarBasicInfo.vin == vin).first()
    dealer_info = db.query(DealerInfo).filter(DealerInfo.vin == vin).first()
    listing_details = db.query(ListingDetails).filter(ListingDetails.vin == vin).first()
    vehicle_specs = db.query(VehicleSpecs).filter(VehicleSpecs.vin == vin).first()
    vehicle_status = db.query(VehicleStatus).filter(VehicleStatus.vin == vin).first()
    seller_info = db.query(SellerInfo).filter(SellerInfo.vin == vin).first()
    return {
        "car_info": car_info,
        "dealer_info": dealer_info,
        "listing_details": listing_details,
        "vehicle_specs": vehicle_specs,
        "vehicle_status": vehicle_status,
        "seller_info": seller_info
    }

""" Original query for reference:
SELECT * FROM cars WHERE vin = :vin
"""


def get_sample_listings(year, make, model, limit=100):
    db = next(get_db())
    listings = db.query(CarBasicInfo.year, CarBasicInfo.make, CarBasicInfo.model, ListingDetails.listing_price, ListingDetails.listing_mileage, DealerInfo.dealer_city, DealerInfo.dealer_state).join(ListingDetails, CarBasicInfo.vin == ListingDetails.vin).join(DealerInfo, CarBasicInfo.vin == DealerInfo.vin).filter(
        CarBasicInfo.year == year,
        CarBasicInfo.make.ilike(make),
        CarBasicInfo.model.ilike(model)
    ).limit(limit).all()
    return listings

""" Original query for reference:
SELECT year, make, model, listing_price, listing_mileage, dealer_city, dealer_state
FROM cars
WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
LIMIT :limit
"""

def calculate_market_price(year, make, model):
    db = next(get_db())
    market_price = db.query(func.avg(ListingDetails.listing_price)).join(CarBasicInfo, CarBasicInfo.vin == ListingDetails.vin).filter(
        CarBasicInfo.year == year,
        CarBasicInfo.make.ilike(make),
        CarBasicInfo.model.ilike(model)
    ).scalar()
    
    return round(market_price, -2) if market_price else None


""" Original query for reference:
SELECT AVG(listing_price) FROM cars
WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
"""

def calculate_price_based_on_mileage(year, make, model, mileage):
    db = next(get_db())
    data = db.query(ListingDetails.listing_price, ListingDetails.listing_mileage).join(CarBasicInfo, CarBasicInfo.vin == ListingDetails.vin).filter(
        CarBasicInfo.year == year,
        CarBasicInfo.make.ilike(make),
        CarBasicInfo.model.ilike(model)
    ).all()
    
    if not data or not mileage:
        return None
    
    # Convert to numpy arrays and handle conversion errors
    prices, mileages = zip(*data)
    try:
        prices = np.array(prices, dtype=float)
        mileages = np.array(mileages, dtype=float)
    except ValueError:
        return None
    
    # Filter out NaN values
    valid_indices = ~np.isnan(prices) & ~np.isnan(mileages)
    prices = prices[valid_indices]
    mileages = mileages[valid_indices].reshape(-1, 1)
    
    if len(prices) == 0 or len(mileages) == 0:
        return None
    
    # Perform linear regression
    model = LinearRegression().fit(mileages, prices)
    predicted_price = model.predict(np.array([[int(mileage)]]))
    return round(predicted_price[0], -2)

""" Original query for reference:
SELECT listing_price, listing_mileage FROM cars
WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
"""

def calculate_price_based_on_mileage_and_state(year, make, model, mileage, state):
    db = next(get_db())
    data = db.query(CarBasicInfo.listing_price, CarBasicInfo.listing_mileage, CarBasicInfo.dealer_state).filter(
        CarBasicInfo.year == year,
        CarBasicInfo.make.ilike(make),
        CarBasicInfo.model.ilike(model),
        CarBasicInfo.dealer_state == state
    ).all()

    if not data or not mileage:
        return None
    
    # Convert to numpy arrays and handle conversion errors
    prices, mileages = zip(*data)
    try:
        prices = np.array(prices, dtype=float)
        mileages = np.array(mileages, dtype=float)
        states = np.array(states, dtype=str)
    except ValueError:
        return None
    
    # Filter out NaN values
    valid_indices = ~np.isnan(prices) & ~np.isnan(mileages) & ~np.isnan(states)
    prices = prices[valid_indices]
    mileages = mileages[valid_indices].reshape(-1, 1)
    states = states[valid_indices]

    if len(prices) == 0 or len(mileages) == 0 or len(states) == 0:
        return None
    
    # Perform linear regression for each state
    models = {}
    for state in np.unique(states):
        state_mask = states == state
        model = LinearRegression().fit(mileages[state_mask], prices[state_mask])
        models[state] = model
    
    # Predict price for the given state
    predicted_price = models[state].predict(np.array([[int(mileage)]]))
    return round(predicted_price[0], -2)

""" Original query for reference:
SELECT listing_price, listing_mileage, dealer_state FROM cars
WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model) AND dealer_state = :state
"""

class CarService:
    def __init__(self, car_repository: CarRepository):
        self.repository = car_repository
        self.price_predictor = PricePredictionService(car_repository)

    def get_car_details(self, vin: str) -> Optional[Dict[str, Any]]:
        return self.repository.get_by_vin(vin)

    def get_cars_with_filters(self, make: str = '', model: str = '', year: Optional[int] = None, offset: int = 0, limit: int = 100) -> List[Any]:
        return self.repository.get_with_filters(make, model, year, offset, limit)

    def get_sample_listings(self, year: int, make: str, model: str, limit: int = 100) -> List[Any]:
        return self.repository.get_sample_listings(year, make, model, limit)

    def calculate_market_price(self, year: int, make: str, model: str) -> Optional[float]:
        return self.price_predictor.calculate_market_price(year, make, model)

    def calculate_price_based_on_mileage(self, year: int, make: str, model: str, mileage: int) -> Optional[float]:
        return self.price_predictor.calculate_price_based_on_mileage(year, make, model, mileage)

    def calculate_price_based_on_mileage_and_state(self, year: int, make: str, model: str, mileage: int, state: str) -> Optional[float]:
        return self.price_predictor.calculate_price_based_on_mileage_and_state(year, make, model, mileage, state)

    def query_cars(self, query_params: Dict, offset: int = 0) -> List[CarBasicInfo]:
        return self.get_cars_with_filters(
            make=query_params.get('make', ''),
            model=query_params.get('model', ''),
            year=query_params.get('year'),
            offset=offset
        )

    def get_distinct_makes(self) -> List[str]:
        return self.repository.get_distinct_makes()

    def get_distinct_models(self) -> List[str]:
        return self.repository.get_distinct_models()

    def get_distinct_years(self) -> List[int]:
        return self.repository.get_distinct_years()

    def get_total_count(self, filters: Dict) -> int:
        return self.repository.get_total_count(filters)

    
