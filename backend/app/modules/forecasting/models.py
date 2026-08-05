from sqlalchemy import ForeignKey, Index, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class MLModel(Base):
    __tablename__ = "ml_models"
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50))
    algorithm: Mapped[str] = mapped_column(String(100))
    hyperparameters: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(50))

class ForecastRun(Base):
    __tablename__ = "forecast_runs"
    model_id: Mapped[UUID] = mapped_column(ForeignKey("ml_models.id", ondelete="CASCADE"))
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    
    training_start: Mapped[datetime]
    training_end: Mapped[datetime]
    forecast_horizon_days: Mapped[int]
    
    mape: Mapped[float | None]
    rmse: Mapped[float | None]
    mae: Mapped[float | None]
    
    status: Mapped[str] = mapped_column(String(50))

class Forecast(Base, SoftDeleteMixin):
    __tablename__ = "forecasts"
    run_id: Mapped[UUID] = mapped_column(ForeignKey("forecast_runs.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    
    forecast_date: Mapped[datetime]
    predicted_demand: Mapped[float]
    lower_bound: Mapped[float | None]
    upper_bound: Mapped[float | None]
    
    __table_args__ = (
        Index("ix_forecast_product_date", "product_id", "forecast_date"),
    )
