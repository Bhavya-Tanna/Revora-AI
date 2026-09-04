from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.revenue import (
    RevenueOpportunity,
    RevenueOverview,
)
from app.services.revenue_intelligence import (
    calculate_revenue_opportunities,
    get_revenue_overview,
)


router = APIRouter(
    prefix="/api/revenue",
    tags=["Revenue Intelligence"],
)


@router.get(
    "/overview",
    response_model=RevenueOverview,
)
def revenue_overview(
    merchant_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_revenue_overview(
        db=db,
        merchant_id=merchant_id,
    )


@router.get(
    "/opportunities",
    response_model=list[RevenueOpportunity],
)
def revenue_opportunities(
    merchant_id: int | None = None,
    opportunity_type: str | None = None,
    priority: str | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    opportunities = calculate_revenue_opportunities(
        db=db,
        merchant_id=merchant_id,
        limit=limit,
    )

    if opportunity_type:
        opportunities = [
            item
            for item in opportunities
            if item["opportunity_type"] == opportunity_type
        ]

    if priority:
        opportunities = [
            item
            for item in opportunities
            if item["priority"] == priority
        ]

    return opportunities[:limit]


@router.get("/merchants")
def list_merchants(
    db: Session = Depends(get_db),
):
    from app.models.merchant import Merchant
    merchants = db.query(Merchant).order_by(Merchant.id).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "monthly_revenue": float(m.monthly_revenue),
            "conversion_rate": float(m.conversion_rate),
            "average_order_value": float(m.average_order_value),
            "cart_abandonment_rate": float(m.cart_abandonment_rate),
            "repeat_purchase_rate": float(m.repeat_purchase_rate),
        }
        for m in merchants
    ]


@router.get(
    "/merchants/{merchant_id}",
    response_model=RevenueOverview,
)
def merchant_revenue_overview(
    merchant_id: int,
    db: Session = Depends(get_db),
):
    return get_revenue_overview(
        db=db,
        merchant_id=merchant_id,
    )