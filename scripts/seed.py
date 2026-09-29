"""
scripts/seed.py
Idempotent database seeder for PriceBite.
Populates realistic Chennai restaurants, varied dishes (veg/non-veg/keto/diabetic-friendly),
and menu items with realistic pricing, portion sizes, and discounts.
Safe to run multiple times without creating duplicates.
"""
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy import select
from app.database import SessionLocal, engine, Base
from app.models.restaurant import Restaurant
from app.models.dish import Dish
from app.models.menu_item import MenuItem


def seed_database():
    print("Starting database seeding...")
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Restaurants (Chennai hotspots)
        restaurants_data = [
            {
                "name": "Dindigul Thalappakatti",
                "area": "T. Nagar",
                "city": "Chennai",
                "lat": 13.0418,
                "lng": 80.2341,
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600",
                "food_rating": 4.4,
                "delivery_rating": 4.2,
                "delivery_fee": 40.0,
                "is_active": True
            },
            {
                "name": "Junior Kuppanna",
                "area": "Nungambakkam",
                "city": "Chennai",
                "lat": 13.0607,
                "lng": 80.2435,
                "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600",
                "food_rating": 4.3,
                "delivery_rating": 4.1,
                "delivery_fee": 35.0,
                "is_active": True
            },
            {
                "name": "A2B - Adyar Ananda Bhavan",
                "area": "Adyar",
                "city": "Chennai",
                "lat": 13.0064,
                "lng": 80.2575,
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600",
                "food_rating": 4.5,
                "delivery_rating": 4.4,
                "delivery_fee": 25.0,
                "is_active": True
            },
            {
                "name": "Sangeetha Veg Restaurant",
                "area": "Mylapore",
                "city": "Chennai",
                "lat": 13.0336,
                "lng": 80.2687,
                "image_url": "https://images.unsplash.com/photo-1590846406792-0adc7f938f1d?w=600",
                "food_rating": 4.6,
                "delivery_rating": 4.5,
                "delivery_fee": 30.0,
                "is_active": True
            },
            {
                "name": "Buhari Hotel",
                "area": "Anna Nagar",
                "city": "Chennai",
                "lat": 13.0850,
                "lng": 80.2101,
                "image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600",
                "food_rating": 4.2,
                "delivery_rating": 3.9,
                "delivery_fee": 45.0,
                "is_active": True
            },
            {
                "name": "Anjappar Chettinad Restaurant",
                "area": "Velachery",
                "city": "Chennai",
                "lat": 12.9759,
                "lng": 80.2212,
                "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=600",
                "food_rating": 4.1,
                "delivery_rating": 4.0,
                "delivery_fee": 35.0,
                "is_active": True
            },
            {
                "name": "Murugan Idli Shop",
                "area": "Besant Nagar",
                "city": "Chennai",
                "lat": 12.9982,
                "lng": 80.2691,
                "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600",
                "food_rating": 4.7,
                "delivery_rating": 4.3,
                "delivery_fee": 20.0,
                "is_active": True
            },
            {
                "name": "Copper Chimney",
                "area": "Gopalapuram",
                "city": "Chennai",
                "lat": 13.0489,
                "lng": 80.2586,
                "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=600",
                "food_rating": 4.5,
                "delivery_rating": 4.2,
                "delivery_fee": 50.0,
                "is_active": True
            }
        ]

        restaurant_map = {}
        for r_data in restaurants_data:
            stmt = select(Restaurant).where(Restaurant.name == r_data["name"])
            existing = db.execute(stmt).scalar_one_or_none()
            if not existing:
                existing = Restaurant(**r_data)
                db.add(existing)
                db.flush()
                print(f"  + Added restaurant: {existing.name}")
            restaurant_map[existing.name] = existing

        # 2. Seed Dishes (~15 dishes: Biryani, Lassi, Gulab Jamun, Veg/Non-Veg/Keto/Diabetic-Friendly)
        dishes_data = [
            {
                "name": "Chicken Biryani",
                "category": "Main Course",
                "diet_type": "non-veg",
                "calories": 750,
                "protein_g": 38.0,
                "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600"
            },
            {
                "name": "Mutton Biryani",
                "category": "Main Course",
                "diet_type": "non-veg",
                "calories": 880,
                "protein_g": 42.0,
                "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600"
            },
            {
                "name": "Vegetable Biryani",
                "category": "Main Course",
                "diet_type": "veg",
                "calories": 520,
                "protein_g": 14.0,
                "image_url": "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=600"
            },
            {
                "name": "Sweet Lassi",
                "category": "Beverages",
                "diet_type": "veg",
                "calories": 240,
                "protein_g": 7.0,
                "image_url": "https://images.unsplash.com/photo-1571006687077-d6c568ecfa31?w=600"
            },
            {
                "name": "Mango Lassi",
                "category": "Beverages",
                "diet_type": "veg",
                "calories": 290,
                "protein_g": 6.5,
                "image_url": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600"
            },
            {
                "name": "Gulab Jamun (2 pcs)",
                "category": "Dessert",
                "diet_type": "veg",
                "calories": 320,
                "protein_g": 5.0,
                "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600"
            },
            {
                "name": "Paneer Butter Masala",
                "category": "Curry",
                "diet_type": "veg",
                "calories": 480,
                "protein_g": 18.0,
                "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600"
            },
            {
                "name": "Masala Dosa",
                "category": "South Indian",
                "diet_type": "veg",
                "calories": 360,
                "protein_g": 8.0,
                "image_url": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=600"
            },
            {
                "name": "Ghee Podi Idli (4 pcs)",
                "category": "South Indian",
                "diet_type": "veg",
                "calories": 310,
                "protein_g": 9.0,
                "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600"
            },
            {
                "name": "Chettinad Pepper Chicken",
                "category": "Starters",
                "diet_type": "non-veg",
                "calories": 420,
                "protein_g": 36.0,
                "image_url": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=600"
            },
            {
                "name": "Keto Grilled Herb Chicken",
                "category": "Healthy",
                "diet_type": "keto",
                "calories": 340,
                "protein_g": 44.0,
                "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600"
            },
            {
                "name": "Keto Paneer Tikka Salad",
                "category": "Healthy",
                "diet_type": "keto",
                "calories": 310,
                "protein_g": 22.0,
                "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600"
            },
            {
                "name": "Diabetic-Friendly Foxtail Millet Khichdi",
                "category": "Healthy",
                "diet_type": "diabetic-friendly",
                "calories": 280,
                "protein_g": 11.0,
                "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600"
            },
            {
                "name": "Diabetic-Friendly Oats Idli & Sambar",
                "category": "Healthy",
                "diet_type": "diabetic-friendly",
                "calories": 220,
                "protein_g": 10.0,
                "image_url": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=600"
            },
            {
                "name": "Authentic Madras Filter Coffee",
                "category": "Beverages",
                "diet_type": "veg",
                "calories": 110,
                "protein_g": 3.0,
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600"
            }
        ]

        dish_map = {}
        for d_data in dishes_data:
            stmt = select(Dish).where(Dish.name == d_data["name"])
            existing = db.execute(stmt).scalar_one_or_none()
            if not existing:
                existing = Dish(**d_data)
                db.add(existing)
                db.flush()
                print(f"  + Added dish: {existing.name}")
            dish_map[existing.name] = existing

        # 3. Seed Menu Items (~60 items across restaurants with varied pricing, portions, discounts)
        # Pricing matrix: [Restaurant, Dish, Price, Portion, Discount%]
        menu_matrix = [
            # Chicken Biryani
            ("Dindigul Thalappakatti", "Chicken Biryani", 320.0, "Regular (1 person)", 15.0),
            ("Junior Kuppanna", "Chicken Biryani", 310.0, "Regular (1 person)", 10.0),
            ("Buhari Hotel", "Chicken Biryani", 290.0, "Regular (1 person)", 20.0),
            ("Anjappar Chettinad Restaurant", "Chicken Biryani", 300.0, "Regular (1 person)", 5.0),
            ("Copper Chimney", "Chicken Biryani", 380.0, "Large (1-2 persons)", 10.0),

            # Mutton Biryani
            ("Dindigul Thalappakatti", "Mutton Biryani", 450.0, "Regular (1 person)", 10.0),
            ("Junior Kuppanna", "Mutton Biryani", 440.0, "Regular (1 person)", 15.0),
            ("Buhari Hotel", "Mutton Biryani", 420.0, "Regular (1 person)", 10.0),
            ("Anjappar Chettinad Restaurant", "Mutton Biryani", 430.0, "Regular (1 person)", 0.0),
            ("Copper Chimney", "Mutton Biryani", 520.0, "Large (1-2 persons)", 20.0),

            # Vegetable Biryani
            ("A2B - Adyar Ananda Bhavan", "Vegetable Biryani", 190.0, "Regular (1 person)", 10.0),
            ("Sangeetha Veg Restaurant", "Vegetable Biryani", 210.0, "Regular (1 person)", 15.0),
            ("Dindigul Thalappakatti", "Vegetable Biryani", 220.0, "Regular (1 person)", 0.0),
            ("Copper Chimney", "Vegetable Biryani", 280.0, "Regular (1 person)", 10.0),

            # Sweet Lassi
            ("A2B - Adyar Ananda Bhavan", "Sweet Lassi", 80.0, "300 ml", 0.0),
            ("Sangeetha Veg Restaurant", "Sweet Lassi", 85.0, "300 ml", 10.0),
            ("Copper Chimney", "Sweet Lassi", 120.0, "350 ml", 15.0),
            ("Junior Kuppanna", "Sweet Lassi", 90.0, "300 ml", 5.0),

            # Mango Lassi
            ("A2B - Adyar Ananda Bhavan", "Mango Lassi", 100.0, "300 ml", 5.0),
            ("Sangeetha Veg Restaurant", "Mango Lassi", 110.0, "300 ml", 10.0),
            ("Copper Chimney", "Mango Lassi", 150.0, "350 ml", 20.0),

            # Gulab Jamun
            ("A2B - Adyar Ananda Bhavan", "Gulab Jamun (2 pcs)", 60.0, "2 pieces", 0.0),
            ("Sangeetha Veg Restaurant", "Gulab Jamun (2 pcs)", 65.0, "2 pieces", 5.0),
            ("Dindigul Thalappakatti", "Gulab Jamun (2 pcs)", 75.0, "2 pieces", 10.0),
            ("Copper Chimney", "Gulab Jamun (2 pcs)", 95.0, "2 pieces", 15.0),
            ("Buhari Hotel", "Gulab Jamun (2 pcs)", 70.0, "2 pieces", 0.0),

            # Paneer Butter Masala
            ("A2B - Adyar Ananda Bhavan", "Paneer Butter Masala", 240.0, "Serves 2", 10.0),
            ("Sangeetha Veg Restaurant", "Paneer Butter Masala", 260.0, "Serves 2", 15.0),
            ("Copper Chimney", "Paneer Butter Masala", 340.0, "Serves 2", 20.0),
            ("Junior Kuppanna", "Paneer Butter Masala", 250.0, "Serves 2", 0.0),

            # Masala Dosa
            ("Murugan Idli Shop", "Masala Dosa", 110.0, "1 piece with 3 chutneys", 0.0),
            ("Sangeetha Veg Restaurant", "Masala Dosa", 125.0, "1 piece with sambar", 10.0),
            ("A2B - Adyar Ananda Bhavan", "Masala Dosa", 120.0, "1 piece with sambar", 5.0),

            # Ghee Podi Idli
            ("Murugan Idli Shop", "Ghee Podi Idli (4 pcs)", 130.0, "4 pieces tossed in pure ghee podi", 0.0),
            ("Sangeetha Veg Restaurant", "Ghee Podi Idli (4 pcs)", 140.0, "4 pieces with podi", 10.0),
            ("A2B - Adyar Ananda Bhavan", "Ghee Podi Idli (4 pcs)", 135.0, "4 pieces with podi", 5.0),

            # Chettinad Pepper Chicken
            ("Anjappar Chettinad Restaurant", "Chettinad Pepper Chicken", 290.0, "Quarter Plate", 10.0),
            ("Junior Kuppanna", "Chettinad Pepper Chicken", 280.0, "Quarter Plate", 5.0),
            ("Dindigul Thalappakatti", "Chettinad Pepper Chicken", 310.0, "Quarter Plate", 15.0),
            ("Buhari Hotel", "Chettinad Pepper Chicken", 270.0, "Quarter Plate", 0.0),

            # Keto Grilled Herb Chicken
            ("Junior Kuppanna", "Keto Grilled Herb Chicken", 330.0, "300g boneless chicken breast", 10.0),
            ("Copper Chimney", "Keto Grilled Herb Chicken", 410.0, "350g grilled chicken", 20.0),
            ("Buhari Hotel", "Keto Grilled Herb Chicken", 320.0, "300g herb chicken", 0.0),

            # Keto Paneer Tikka Salad
            ("Sangeetha Veg Restaurant", "Keto Paneer Tikka Salad", 280.0, "250g grilled paneer with lettuce", 15.0),
            ("Copper Chimney", "Keto Paneer Tikka Salad", 350.0, "300g paneer cubes with olive oil", 10.0),
            ("A2B - Adyar Ananda Bhavan", "Keto Paneer Tikka Salad", 270.0, "250g grilled paneer salad", 5.0),

            # Diabetic-Friendly Foxtail Millet Khichdi
            ("Sangeetha Veg Restaurant", "Diabetic-Friendly Foxtail Millet Khichdi", 180.0, "Bowl (350g)", 10.0),
            ("A2B - Adyar Ananda Bhavan", "Diabetic-Friendly Foxtail Millet Khichdi", 170.0, "Bowl (350g)", 0.0),
            ("Murugan Idli Shop", "Diabetic-Friendly Foxtail Millet Khichdi", 160.0, "Bowl (350g)", 5.0),

            # Diabetic-Friendly Oats Idli & Sambar
            ("Murugan Idli Shop", "Diabetic-Friendly Oats Idli & Sambar", 120.0, "3 pieces with low-GI sambar", 0.0),
            ("Sangeetha Veg Restaurant", "Diabetic-Friendly Oats Idli & Sambar", 130.0, "3 pieces with sambar", 10.0),
            ("A2B - Adyar Ananda Bhavan", "Diabetic-Friendly Oats Idli & Sambar", 125.0, "3 pieces with sambar", 5.0),

            # Authentic Madras Filter Coffee
            ("Murugan Idli Shop", "Authentic Madras Filter Coffee", 40.0, "1 Dabarah Set (120 ml)", 0.0),
            ("Sangeetha Veg Restaurant", "Authentic Madras Filter Coffee", 45.0, "1 Dabarah Set (120 ml)", 0.0),
            ("A2B - Adyar Ananda Bhavan", "Authentic Madras Filter Coffee", 45.0, "1 Dabarah Set (120 ml)", 0.0),
            ("Junior Kuppanna", "Authentic Madras Filter Coffee", 50.0, "1 Dabarah Set (120 ml)", 10.0)
        ]

        inserted_count = 0
        for rest_name, dish_name, price, portion, discount in menu_matrix:
            restaurant = restaurant_map.get(rest_name)
            dish = dish_map.get(dish_name)

            if not restaurant or not dish:
                continue

            # Idempotency check on unique constraint (restaurant_id, dish_id)
            stmt = select(MenuItem).where(
                MenuItem.restaurant_id == restaurant.id,
                MenuItem.dish_id == dish.id
            )
            existing_item = db.execute(stmt).scalar_one_or_none()
            if not existing_item:
                new_item = MenuItem(
                    restaurant_id=restaurant.id,
                    dish_id=dish.id,
                    price=price,
                    portion_size=portion,
                    discount_percent=discount,
                    is_available=True
                )
                db.add(new_item)
                inserted_count += 1

        db.commit()
        print(f"Seeding completed successfully! Inserted {inserted_count} new menu items.")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
