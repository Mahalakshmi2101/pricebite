from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DishSearchResultItem(BaseModel):
    dish_id: int
    dish_name: str
    category: str
    diet_type: str
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    dish_image_url: Optional[str] = None
    
    restaurant_id: int
    restaurant_name: str
    restaurant_area: str
    food_rating: float
    delivery_rating: float
    
    price: float
    portion_size: str
    discount_percent: float
    final_price: float
    delivery_fee: float
    tax: float  # Assumption: Flat 5% GST on food services in India
    total_cost: float

    model_config = ConfigDict(from_attributes=True)


class DishSearchResponse(BaseModel):
    total: int
    items: List[DishSearchResultItem]
    limit: int
    offset: int
