import datetime
from sqlalchemy import String, Float, Boolean, ForeignKey, DateTime, Time, JSON, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Index to accelerate querying historical price trends for a menu item
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    menu_item = relationship("MenuItem", back_populates="price_history")


class PartnerPreference(Base):
    __tablename__ = "partner_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,  # 1-to-1 relationship with delivery partner user
        nullable=False,
        index=True
    )
    no_delivery_after: Mapped[datetime.time | None] = mapped_column(Time, nullable=True)
    avoid_areas: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)

    # Relationships
    user = relationship("User", back_populates="partner_preference")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Index to fetch user's notifications sorted by date
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # price_drop, order_update, etc.
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="notifications")
