from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.campaign import Campaign
    from app.models.customer import Customer
    from app.models.product import Product


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    monthly_revenue: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        default=0,
    )

    conversion_rate: Mapped[Decimal] = mapped_column(
        Numeric(6, 4),
        default=0,
    )

    average_order_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    cart_abandonment_rate: Mapped[Decimal] = mapped_column(
        Numeric(6, 4),
        default=0,
    )

    repeat_purchase_rate: Mapped[Decimal] = mapped_column(
        Numeric(6, 4),
        default=0,
    )

    customers: Mapped[list[Customer]] = relationship(
        back_populates="merchant",
    )
    products: Mapped[list[Product]] = relationship(
        back_populates="merchant",
    )
    campaigns: Mapped[list[Campaign]] = relationship(
        back_populates="merchant",
    )