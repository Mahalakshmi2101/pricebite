"""
app/routers/dishes.py
Dishes and cross-restaurant price comparison search router.
Executes an optimized, single-query relational JOIN to prevent the N+1 problem.
Computes total_cost in SQL for deterministic database-level sorting and pagination.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.dish import Dish
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.schemas.comparison import DishSearchResponse, DishSearchResultItem

router = APIRouter(prefix="/dishes", tags=["Dishes & Comparison"])


@router.get("/search", response_model=DishSearchResponse)
def search_dishes(
    q: Optional[str] = Query(None, description="Case-insensitive dish name search term"),
    diet: Optional[str] = Query(None, description="Dietary filter: veg, non-veg, keto, diabetic-friendly"),
    max_calories: Optional[int] = Query(None, description="Maximum calorie threshold"),
    min_food_rating: Optional[float] = Query(None, description="Minimum restaurant food rating"),
    sort: Optional[str] = Query("total_cost", description="Sort order: total_cost, -total_cost, price, -price, food_rating, -food_rating"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search and compare food prices across restaurants in Chennai.
    - Joins Dish -> MenuItem -> Restaurant in a single query (O(1) database roundtrip).
    - Computes final_price, 5% GST, and total_cost directly in SQL to enable database-level ordering.
    - Filters only available items from currently active restaurants.
    """
    # SQL Expressions for Price & Cost Calculation:
    # 1. final_price = price * (1.0 - discount_percent / 100.0)
    final_price_expr = func.round(
        MenuItem.price * (1.0 - (MenuItem.discount_percent / 100.0)), 2
    )

    # 2. tax: Indian GST on restaurant food services is flat 5% (CGST 2.5% + SGST 2.5%)
    # Assumption: Flat 5% GST calculated on the discounted final_price
    tax_expr = func.round(final_price_expr * 0.05, 2)

    # 3. total_cost = final_price + delivery_fee + tax
    total_cost_expr = func.round(
        final_price_expr + Restaurant.delivery_fee + tax_expr, 2
    )

    # Build primary query with projections
    query = select(
        Dish.id.label("dish_id"),
        Dish.name.label("dish_name"),
        Dish.category.label("category"),
        Dish.diet_type.label("diet_type"),
        Dish.calories.label("calories"),
        Dish.protein_g.label("protein_g"),
        Dish.image_url.label("dish_image_url"),
        Restaurant.id.label("restaurant_id"),
        Restaurant.name.label("restaurant_name"),
        Restaurant.area.label("restaurant_area"),
        Restaurant.food_rating.label("food_rating"),
        Restaurant.delivery_rating.label("delivery_rating"),
        MenuItem.price.label("price"),
        MenuItem.portion_size.label("portion_size"),
        MenuItem.discount_percent.label("discount_percent"),
        final_price_expr.label("final_price"),
        Restaurant.delivery_fee.label("delivery_fee"),
        tax_expr.label("tax"),
        total_cost_expr.label("total_cost")
    ).select_from(Dish).join(
        MenuItem, Dish.id == MenuItem.dish_id
    ).join(
        Restaurant, MenuItem.restaurant_id == Restaurant.id
    ).where(
        MenuItem.is_available.is_(True),
        Restaurant.is_active.is_(True)
    )

    # Filters
    if q and q.strip():
        search_term = f"%{q.strip().lower()}%"
        query = query.where(func.lower(Dish.name).like(search_term))

    if diet and diet.strip():
        query = query.where(Dish.diet_type == diet.strip().lower())

    if max_calories is not None:
        query = query.where(Dish.calories <= max_calories)

    if min_food_rating is not None:
        query = query.where(Restaurant.food_rating >= min_food_rating)

    # Count total matching rows (for pagination)
    count_subquery = query.with_only_columns(func.count()).order_by(None)
    total_count = db.execute(count_subquery).scalar() or 0

    # Sorting
    if sort == "-total_cost":
        query = query.order_by(desc(total_cost_expr))
    elif sort == "price":
        query = query.order_by(asc(MenuItem.price))
    elif sort == "-price":
        query = query.order_by(desc(MenuItem.price))
    elif sort == "food_rating":
        query = query.order_by(asc(Restaurant.food_rating))
    elif sort == "-food_rating":
        query = query.order_by(desc(Restaurant.food_rating))
    else:  # default: total_cost ascending
        query = query.order_by(asc(total_cost_expr))

    # Pagination
    query = query.limit(limit).offset(offset)

    # Execute
    rows = db.execute(query).mappings().all()

    items = [DishSearchResultItem(**row) for row in rows]
    return DishSearchResponse(
        total=total_count,
        items=items,
        limit=limit,
        offset=offset
    )
