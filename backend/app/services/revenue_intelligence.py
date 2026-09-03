from collections import defaultdict
from decimal import Decimal
from typing import Any

from app.ml.predict import predict_reactivation_probability
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Cart,
    Customer,
    Order,
    Payment,
    Product,
)


def clamp(value: float, minimum: float = 0.05, maximum: float = 0.95) -> float:
    """Keep a probability within a sensible range."""
    return max(minimum, min(maximum, value))


def priority_from_score(score: float) -> str:
    if score >= 0.70:
        return "HIGH"
    if score >= 0.40:
        return "MEDIUM"
    return "LOW"


def abandoned_cart_probability(cart: Cart, customer: Customer) -> float:
    """
    Estimate the probability that an abandoned cart can be recovered.

    Higher engagement and discount sensitivity increase recovery probability.
    Very recent carts are also easier to recover.
    """
    score = 0.25

    score += float(customer.engagement_score) * 0.35
    score += float(customer.discount_sensitivity) * 0.20

    return clamp(score)


def failed_payment_probability(payment: Payment, customer: Customer) -> float:
    """Estimate the probability of successfully recovering a failed payment."""
    probabilities = {
        "GATEWAY_ERROR": 0.75,
        "TIMEOUT": 0.70,
        "USER_CANCELLED": 0.45,
        "INSUFFICIENT_FUNDS": 0.30,
    }

    score = probabilities.get(payment.failure_reason or "", 0.40)

    # Repeat customers are generally more recoverable.
    if float(customer.lifetime_value) > 10000:
        score += 0.10

    if payment.attempt_number <= 1:
        score += 0.05

    return clamp(score)


def dormant_reactivation_probability(customer: Customer) -> float:
    """Estimate the probability of reactivating an inactive customer."""
    days = customer.days_since_last_purchase

    if days < 60:
        base = 0.55
    elif days < 120:
        base = 0.40
    elif days < 240:
        base = 0.28
    else:
        base = 0.18

    base += float(customer.engagement_score) * 0.20
    base += float(customer.discount_sensitivity) * 0.10

    return clamp(base)


def cross_sell_probability(customer: Customer) -> float:
    """Estimate cross-sell probability from customer engagement."""
    score = 0.20
    score += float(customer.engagement_score) * 0.45
    score += float(customer.purchase_frequency) * 0.15

    return clamp(score)


def calculate_revenue_opportunities(
    db: Session,
    merchant_id: int | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Analyze commerce activity and return revenue opportunities.

    All monetary estimates originate from the database.
    No LLM is used for financial calculations.
    """

    customers = db.scalars(
        select(Customer).where(
            Customer.merchant_id == merchant_id
        )
        if merchant_id is not None
        else select(Customer)
    ).all()

    customer_map = {customer.id: customer for customer in customers}

    opportunities: list[dict[str, Any]] = []

    # ---------------------------------------------------------
    # 1. ABANDONED CART RECOVERY
    # ---------------------------------------------------------
    cart_query = select(Cart).where(Cart.abandoned.is_(True))

    if merchant_id is not None:
        cart_query = cart_query.where(Cart.merchant_id == merchant_id)

    carts = db.scalars(cart_query).all()

    for cart in carts:
        customer = customer_map.get(cart.customer_id)

        if customer is None or cart.total_value <= 0:
            continue

        probability = abandoned_cart_probability(cart, customer)

        estimated = Decimal(str(
            float(cart.total_value) * probability
        )).quantize(Decimal("0.01"))

        if estimated <= 0:
            continue

        score = probability * min(float(cart.total_value) / 5000, 1.0)

        opportunities.append(
            {
                "opportunity_type": "ABANDONED_CART_RECOVERY",
                "merchant_id": cart.merchant_id,
                "customer_id": cart.customer_id,
                "source_id": cart.id,
                "title": "Recover abandoned cart",
                "description": (
                    f"Customer has an abandoned cart worth "
                    f"₹{float(cart.total_value):,.2f}."
                ),
                "estimated_revenue": estimated,
                "confidence": round(probability, 2),
                "priority": priority_from_score(score),
                "recommended_action": "SEND_CART_RECOVERY_OFFER",
            }
        )

    # ---------------------------------------------------------
    # 2. FAILED PAYMENT RECOVERY
    # ---------------------------------------------------------
    payment_query = select(Payment).where(
        Payment.status == "FAILED"
    )

    if merchant_id is not None:
        payment_query = payment_query.join(
            Order,
            Payment.order_id == Order.id,
        ).where(Order.merchant_id == merchant_id)

    payments = db.scalars(payment_query).all()

    for payment in payments:
        customer = customer_map.get(payment.customer_id)

        if customer is None or payment.amount <= 0:
            continue

        probability = failed_payment_probability(payment, customer)

        estimated = Decimal(str(
            float(payment.amount) * probability
        )).quantize(Decimal("0.01"))

        score = probability * min(float(payment.amount) / 5000, 1.0)

        opportunities.append(
            {
                "opportunity_type": "FAILED_PAYMENT_RECOVERY",
                "merchant_id": (
                    merchant_id
                    if merchant_id is not None
                    else None
                ),
                "customer_id": payment.customer_id,
                "source_id": payment.id,
                "title": "Recover failed payment",
                "description": (
                    f"Failed payment of ₹{float(payment.amount):,.2f} "
                    f"with reason {payment.failure_reason or 'UNKNOWN'}."
                ),
                "estimated_revenue": estimated,
                "confidence": round(probability, 2),
                "priority": priority_from_score(score),
                "recommended_action": "RETRY_PAYMENT",
            }
        )

    # ---------------------------------------------------------
    # 3. DORMANT CUSTOMER REACTIVATION
    # ---------------------------------------------------------
    for customer in customers:
        if customer.days_since_last_purchase < 90:
            continue

        if customer.average_order_value <= 0:
            continue

        probability = predict_reactivation_probability(
    db,
    customer,
)

        estimated = Decimal(str(
            float(customer.average_order_value) * probability
        )).quantize(Decimal("0.01"))

        score = probability * min(
            float(customer.lifetime_value) / 25000,
            1.0,
        )

        opportunities.append(
            {
                "opportunity_type": "DORMANT_CUSTOMER_REACTIVATION",
                "merchant_id": customer.merchant_id,
                "customer_id": customer.id,
                "source_id": customer.id,
                "title": "Reactivate dormant customer",
                "description": (
                    f"Customer has been inactive for "
                    f"{customer.days_since_last_purchase} days."
                ),
                "estimated_revenue": estimated,
                "confidence": round(probability, 2),
                "priority": priority_from_score(score),
                "recommended_action": "SEND_REACTIVATION_OFFER",
            }
        )

    # ---------------------------------------------------------
    # 4. CROSS-SELL OPPORTUNITIES
    # ---------------------------------------------------------
    orders_query = select(Order)

    if merchant_id is not None:
        orders_query = orders_query.where(
            Order.merchant_id == merchant_id
        )

    orders = db.scalars(orders_query).all()

    order_customer_ids = {order.customer_id for order in orders}

    for customer_id in order_customer_ids:
        customer = customer_map.get(customer_id)

        if customer is None:
            continue

        if customer.purchase_frequency <= 0:
            continue

        probability = cross_sell_probability(customer)

        expected_value = (
            float(customer.average_order_value)
            if customer.average_order_value > 0
            else 0
        )

        estimated = Decimal(str(
            expected_value * probability
        )).quantize(Decimal("0.01"))

        if estimated <= 0:
            continue

        score = probability * min(
            expected_value / 5000,
            1.0,
        )

        opportunities.append(
            {
                "opportunity_type": "CROSS_SELL",
                "merchant_id": customer.merchant_id,
                "customer_id": customer.id,
                "source_id": customer.id,
                "title": "Cross-sell to existing customer",
                "description": (
                    "Customer shows sufficient engagement and "
                    "purchase activity for a cross-sell recommendation."
                ),
                "estimated_revenue": estimated,
                "confidence": round(probability, 2),
                "priority": priority_from_score(score),
                "recommended_action": "RECOMMEND_CROSS_SELL",
            }
        )

    opportunities.sort(
        key=lambda item: (
            {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[item["priority"]],
            float(item["estimated_revenue"]),
        ),
        reverse=True,
    )

    return opportunities[:limit]


def get_revenue_overview(
    db: Session,
    merchant_id: int | None = None,
) -> dict[str, Any]:
    """Return an aggregate revenue opportunity overview."""

    opportunities = calculate_revenue_opportunities(
        db=db,
        merchant_id=merchant_id,
        limit=500,
    )

    order_query = select(Order)

    if merchant_id is not None:
        order_query = order_query.where(
            Order.merchant_id == merchant_id
        )

    orders = db.scalars(order_query).all()

    total_current_revenue = sum(
        (order.total_amount for order in orders),
        Decimal("0"),
    )

    total_opportunity = sum(
        (item["estimated_revenue"] for item in opportunities),
        Decimal("0"),
    )

    breakdown: dict[str, Decimal] = defaultdict(
        lambda: Decimal("0")
    )

    for opportunity in opportunities:
        breakdown[
            opportunity["opportunity_type"]
        ] += opportunity["estimated_revenue"]

    high_priority = sum(
        1
        for item in opportunities
        if item["priority"] == "HIGH"
    )

    return {
        "total_current_revenue": total_current_revenue,
        "total_estimated_opportunity": total_opportunity,
        "opportunity_breakdown": dict(breakdown),
        "high_priority_count": high_priority,
        "top_opportunities": opportunities[:10],
    }