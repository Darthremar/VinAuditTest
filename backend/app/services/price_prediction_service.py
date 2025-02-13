from typing import Optional
import numpy as np
from sklearn.linear_model import LinearRegression
from ..repositories.car_repository import CarRepository

class PricePredictionService:
    def __init__(self, repository: CarRepository):
        self.repository = repository

    def calculate_market_price(self, year: int, make: str, model: str) -> Optional[float]:
        market_price = self.repository.get_market_data(year, make, model)
        return round(market_price, -2) if market_price else None

    def calculate_price_based_on_mileage(self, year: int, make: str, model: str, mileage: int) -> Optional[float]:
        data = self.repository.get_mileage_data(year, make, model)
        return self._predict_price(data, mileage)

    def calculate_price_based_on_mileage_and_state(self, year: int, make: str, model: str, mileage: int, state: str) -> Optional[float]:
        data = self.repository.get_mileage_data(year, make, model, state)
        return self._predict_price(data, mileage)

    def _predict_price(self, data: list, mileage: int) -> Optional[float]:
        if not data or not mileage:
            return None

        prices, mileages = zip(*data)
        try:
            prices = np.array(prices, dtype=float)
            mileages = np.array(mileages, dtype=float).reshape(-1, 1)
        except ValueError:
            return None

        valid_indices = ~np.isnan(prices) & ~np.isnan(mileages.flatten())
        prices = prices[valid_indices]
        mileages = mileages[valid_indices]

        if len(prices) == 0 or len(mileages) == 0:
            return None

        model = LinearRegression().fit(mileages, prices)
        predicted_price = model.predict(np.array([[int(mileage)]]))
        return round(predicted_price[0], -2) 