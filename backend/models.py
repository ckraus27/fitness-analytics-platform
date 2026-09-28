from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    calories: Mapped[float] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=False)
    carbs: Mapped[float] = mapped_column(nullable=False)
    fat: Mapped[float] = mapped_column(nullable=False)

class FoodEntry(Base):
    __tablename__ = "food_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), nullable=False)
    amount_grams: Mapped[float] = mapped_column(nullable=False)
    consumed_at: Mapped[datetime] = mapped_column(nullable=False)

