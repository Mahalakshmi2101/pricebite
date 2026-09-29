from typing import List
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Index on name accelerates case-insensitive prefix and exact text searches
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    diet_type: Mapped[str] = mapped_column(String(50), nullable=False)  # veg, non-veg, keto, diabetic-friendly
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    menu_items: Mapped[List["MenuItem"]] = relationship("MenuItem", back_populates="dish", cascade="all, delete-orphan")
