from datetime import date
from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    farm_size_acres: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="farmer", nullable=False)
class MarketPrice(Base):
    __tablename__ = "market_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crop_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    market: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    price_per_quintal: Mapped[float] = mapped_column(Float, nullable=False)
