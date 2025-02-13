from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.car_basic_info import CarBasicInfo
from ..models.listing_details import ListingDetails

class ICarRepository(ABC):
    @abstractmethod
    def get_by_vin(self, vin: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_with_filters(self, make: str, model: str, year: int, offset: int) -> List[Any]:
        pass
    
    @abstractmethod
    def get_sample_listings(self, year: int, make: str, model: str, limit: int) -> List[Any]:
        pass
    
    @abstractmethod
    def get_market_data(self, year: int, make: str, model: str) -> List[Any]:
        pass
    
    @abstractmethod
    def get_mileage_data(self, year: int, make: str, model: str, state: Optional[str] = None) -> List[Any]:
        pass 