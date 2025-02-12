from ..models.models import Car
from sqlalchemy import create_engine, text
import numpy as np
from sklearn.linear_model import LinearRegression

def get_db_connection():
    return create_engine('postgresql://postgres:Condor92!@localhost:5432/autos_db')

def calculate_market_price(year, make, model):
    engine = get_db_connection()
    with engine.connect() as connection:
        query = """
        SELECT AVG(listing_price) FROM cars
        WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
        """
        result = connection.execute(text(query), {'year': year, 'make': make, 'model': model})
        market_price = result.scalar()
        return round(market_price, -2) if market_price else None

def get_sample_listings(year, make, model, limit=100):
    engine = get_db_connection()
    with engine.connect() as connection:
        query = """
        SELECT year, make, model, listing_price, listing_mileage, dealer_city, dealer_state
        FROM cars
        WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
        LIMIT :limit
        """
        result = connection.execute(text(query), {'year': year, 'make': make, 'model': model, 'limit': limit})
        return result.fetchall()

def calculate_price_based_on_mileage(year, make, model, mileage):
    engine = get_db_connection()
    with engine.connect() as connection:
        query = """
        SELECT listing_price, listing_mileage FROM cars
        WHERE year = :year AND LOWER(make) = LOWER(:make) AND LOWER(model) = LOWER(:model)
        """
        result = connection.execute(text(query), {'year': year, 'make': make, 'model': model})
        data = result.fetchall()
        
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
    
def query_cars(query_params, offset=0, limit=100):
    engine = get_db_connection()
    with engine.connect() as connection:
        query = """
        SELECT * FROM cars
        WHERE 1=1
        """
        if 'make' in query_params and query_params['make']:
            query += " AND LOWER(make) = LOWER(:make)"
        if 'model' in query_params and query_params['model']:
            query += " AND LOWER(model) = LOWER(:model)"
        query += " LIMIT :limit OFFSET :offset"
        result = connection.execute(text(query), {**query_params, 'limit': limit, 'offset': offset})
        rows = result.fetchall()
        
        if not rows:
            raise ValueError("No results found for the given query parameters.")
        
        return rows
