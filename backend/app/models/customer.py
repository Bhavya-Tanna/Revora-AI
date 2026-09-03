from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.agent_action import AgentAction
    from app.models.cart import Cart
    from app.models.merchant import Merchant
    from app.models.offer import Offer
    from app.models.order import Order


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("merchants.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    age: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    customer_segment: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    lifetime_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    purchase_frequency: Mapped[Decimal] = mapped_column(Numeric(8, 4), default=0)
    average_order_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    days_since_last_purchase: Mapped[int] = mapped_column(default=0)
    discount_sensitivity: Mapped[Decimal] = mapped_column(Numeric(6, 4), default=0)
    engagement_score: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    merchant: Mapped[Merchant] = relationship(back_populates="customers")
    carts: Mapped[list[Cart]] = relationship(back_populates="customer")
    orders: Mapped[list[Order]] = relationship(back_populates="customer")
    offers: Mapped[list[Offer]] = relationship(back_populates="customer")
    agent_actions: Mapped[list[AgentAction]] = relationship(back_populates="customer")
