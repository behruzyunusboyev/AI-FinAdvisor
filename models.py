"""Database models. JSONB keeps original requests and deterministic results intact."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


JsonData = JSON().with_variant(JSONB, "postgresql")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    business_type: Mapped[str] = mapped_column(String(120), nullable=False)
    request_data: Mapped[dict] = mapped_column(JsonData, nullable=False)
    financial_data: Mapped[dict] = mapped_column(JsonData, nullable=False)
    ai_analysis: Mapped[dict] = mapped_column(JsonData, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    daily_logs: Mapped[list["DailyLog"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    daily_revenue: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    daily_expense: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    result_data: Mapped[dict] = mapped_column(JsonData, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    project: Mapped[Project] = relationship(back_populates="daily_logs")
