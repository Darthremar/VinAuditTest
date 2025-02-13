from sqlalchemy.orm import Session
from ..models.car_model import Car
from ..database import SessionLocal
import numpy as np
from sqlalchemy import func
from sklearn.linear_model import LinearRegression

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_car_details(vin):
    db = next(get_db())
    car = db.query(Car).filter(Car.vin == vin).first()
    return car

""" Original query for reference:
SELECT * FROM cars WHERE vin = :vin
"""


def get_sample_listings(year, make, model, limit=100):
    db = next(get_db())
    listings = db.query(Car.year, Car.make, Car.model, Car.listing_price, Car.listing_mileage, Car.dealer_city, Car.dealer_state).filter(
        Car.year == year,
        Car.make.ilike(make),
        Car.model.ilike(model)
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
    market_price = db.query(func.avg(Car.listing_price)).filter(
        Car.year == year,
        Car.make.ilike(make),
        Car.model.ilike(model)
    ).scalar()
    
    return round(market_price, -2) if market_price else None


""" Original query for reference:
SELECT AVG(listing_price) FROM cars
WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
"""

def calculate_price_based_on_mileage(year, make, model, mileage):
    db = next(get_db())
    data = db.query(Car.listing_price, Car.listing_mileage).filter(
        Car.year == year,
        Car.make.ilike(make),
        Car.model.ilike(model)
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
    data = db.query(Car.listing_price, Car.listing_mileage, Car.dealer_state).filter(
        Car.year == year,
        Car.make.ilike(make),
        Car.model.ilike(model),
        Car.dealer_state == state
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

def query_cars(query_params, offset=0, limit=100):
    db = next(get_db())
    query = db.query(Car)
    
    if 'make' in query_params and query_params['make']:
        query = query.filter(Car.make.ilike(query_params['make']))
    if 'model' in query_params and query_params['model']:
        query = query.filter(Car.model.ilike(query_params['model']))
    
    rows = query.offset(offset).limit(limit).all()
    
    if not rows:
        raise ValueError("No results found for the given query parameters.")
    
    return rows

""" Original query for reference:
SELECT * FROM cars
WHERE 1=1
"""

