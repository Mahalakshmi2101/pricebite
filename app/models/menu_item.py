from typing import List
from sqlalchemy import String, Float, Boolean, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Index to accelerate joins: JOIN restaurants ON menu_items.restaurant_id = restaurants.id
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey("dishes.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Index to accelerate joins: JOIN dishes ON menu_items.dish_id = dishes.id
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    portion_size: Mapped[str] = mapped_column(String(100), nullable=False)
    discount_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        # A restaurant cannot have duplicate entries for the exact same dish
        UniqueConstraint("restaurant_id", "dish_id", name="uq_restaurant_dish"),
        # Composite index for filtering active availability per restaurant efficiently
        Index("ix_menu_items_available", "is_available"),
    )

    # Relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")
    dish = relationship("Dish", back_populates="menu_items")
    price_history = relationship("PriceHistory", back_populates="menu_item", cascade="all, delete-orphan")
