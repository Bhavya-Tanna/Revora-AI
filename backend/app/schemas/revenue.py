from decimal import Decimal

from pydantic import BaseModel, Field


class RevenueOpportunity(BaseModel):
    opportunity_type: str
    merchant_id: int | None
    customer_id: int | None
    source_id: int | None
    title: str
    description: str
    estimated_revenue: Decimal
    confidence: float = Field(ge=0, le=1)
    priority: str
    recommended_action: str


class RevenueOverview(BaseModel):
    total_current_revenue: Decimal
    total_estimated_opportunity: Decimal
    opportunity_breakdown: dict[str, Decimal]
    high_priority_count: int
    top_opportunities: list[RevenueOpportunity]