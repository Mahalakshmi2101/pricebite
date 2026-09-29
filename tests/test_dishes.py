import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant
from app.models.dish import Dish
from app.models.menu_item import MenuItem


@pytest.fixture(autouse=True)
def populate_sample_data(db_session: Session):
    """
    Populate a controlled set of restaurants, dishes, and menu items in the test DB.
    """
    # Active Restaurant 1
    r1 = Restaurant(
        name="Thalappakatti Test",
        area="T. Nagar",
        city="Chennai",
        lat=13.04,
        lng=80.23,
        food_rating=4.5,
        delivery_rating=4.2,
        delivery_fee=40.0,
        is_active=True
    )
    # Active Restaurant 2
    r2 = Restaurant(
        name="A2B Test",
        area="Adyar",
        city="Chennai",
        lat=13.00,
        lng=80.25,
        food_rating=4.6,
        delivery_rating=4.4,
        delivery_fee=25.0,
        is_active=True
    )
    # Inactive Restaurant (should never appear in search results)
    r3 = Restaurant(
        name="Closed Restaurant",
        area="Mylapore",
        city="Chennai",
        lat=13.03,
        lng=80.26,
        food_rating=3.0,
        delivery_rating=3.0,
        delivery_fee=50.0,
        is_active=False
    )
    db_session.add_all([r1, r2, r3])
    db_session.flush()

    # Dishes
    d1 = Dish(
        name="Special Chicken Biryani",
        category="Main Course",
        diet_type="non-veg",
        calories=750,
        protein_g=38.0
    )
    d2 = Dish(
        name="Authentic Mango Lassi",
        category="Beverages",
        diet_type="veg",
        calories=250,
        protein_g=6.0
    )
    db_session.add_all([d1, d2])
    db_session.flush()

    # Menu Items
    # Item 1: Biryani at Thalappakatti: Price 300, 10% discount -> final_price 270.0, delivery 40.0, tax 13.5 (5%), total 323.5
    m1 = MenuItem(
        restaurant_id=r1.id,
        dish_id=d1.id,
        price=300.0,
        portion_size="Regular",
        discount_percent=10.0,
        is_available=True
    )
    # Item 2: Biryani at A2B (more expensive): Price 350, 0% discount -> final_price 350.0, delivery 25.0, tax 17.5 (5%), total 392.5
    m2 = MenuItem(
        restaurant_id=r2.id,
        dish_id=d1.id,
        price=350.0,
        portion_size="Regular",
        discount_percent=0.0,
        is_available=True
    )
    # Item 3: Biryani at Closed Restaurant (must be excluded)
    m3 = MenuItem(
        restaurant_id=r3.id,
        dish_id=d1.id,
        price=200.0,
        portion_size="Regular",
        discount_percent=0.0,
        is_available=True
    )
    # Item 4: Mango Lassi at A2B: Price 100, 20% discount -> final_price 80.0, delivery 25.0, tax 4.0, total 109.0
    m4 = MenuItem(
        restaurant_id=r2.id,
        dish_id=d2.id,
        price=100.0,
        portion_size="300 ml",
        discount_percent=20.0,
        is_available=True
    )
    # Item 5: Unavailable item (is_available=False) -> must be excluded
    m5 = MenuItem(
        restaurant_id=r1.id,
        dish_id=d2.id,
        price=90.0,
        portion_size="300 ml",
        discount_percent=0.0,
        is_available=False
    )
    db_session.add_all([m1, m2, m3, m4, m5])
    db_session.commit()


def test_search_match_found(client: TestClient):
    """
    Test 1: Match found for partial query 'biryani'. Returns active and available entries.
    """
    response = client.get("/dishes/search?q=biryani")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

    # Check required fields
    first = data["items"][0]
    assert "Chicken Biryani" in first["dish_name"]
    assert "restaurant_name" in first
    assert "food_rating" in first
    assert "delivery_rating" in first
    assert "price" in first
    assert "portion_size" in first
    assert "discount_percent" in first
    assert "final_price" in first
    assert "delivery_fee" in first
    assert "tax" in first
    assert "total_cost" in first


def test_search_no_match(client: TestClient):
    """
    Test 2: Search returns total=0 and empty items list when no dish matches.
    """
    response = client.get("/dishes/search?q=NonExistentExoticDishXYZ")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_search_sort_order(client: TestClient):
    """
    Test 3: Default sort order is total_cost ascending.
    """
    response = client.get("/dishes/search")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    assert len(items) >= 2

    # Verify monotonic increasing total_cost
    costs = [item["total_cost"] for item in items]
    assert costs == sorted(costs)


def test_search_discount_applied_correctly(client: TestClient):
    """
    Test 4: Mathematical verification of discount, 5% tax, and total_cost.
    """
    response = client.get("/dishes/search?q=Special Chicken Biryani")
    assert response.status_code == 200
    items = response.json()["items"]
    
    # Locate Thalappakatti item (Price: 300, Discount: 10%, Delivery: 40)
    thalappakatti_item = next(i for i in items if i["restaurant_name"] == "Thalappakatti Test")
    
    expected_final_price = round(300.0 * 0.90, 2)  # 270.00
    expected_tax = round(expected_final_price * 0.05, 2)  # 13.50
    expected_total = round(expected_final_price + 40.0 + expected_tax, 2)  # 323.50

    assert thalappakatti_item["price"] == 300.0
    assert thalappakatti_item["discount_percent"] == 10.0
    assert thalappakatti_item["final_price"] == expected_final_price
    assert thalappakatti_item["tax"] == expected_tax
    assert thalappakatti_item["total_cost"] == expected_total
