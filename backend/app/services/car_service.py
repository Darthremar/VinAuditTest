from ..models.models import Car

def calculate_market_price(cars):
    if not cars:
        return 0
    total_price = sum(car.listing_price for car in cars)
    return total_price / len(cars) 