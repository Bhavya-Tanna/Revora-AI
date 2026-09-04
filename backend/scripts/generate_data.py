"""Deterministic synthetic commerce data for local development."""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

SEED = 42
AS_OF = datetime(2026, 9, 1, 12, 0, 0)

MERCHANT_PROFILES: list[tuple[str, str]] = [
    ("NovaWear", "Fashion"),
    ("FreshBasket", "Grocery"),
    ("VoltMart", "Electronics"),
    ("GlowLab", "Beauty"),
    ("Hearth & Co", "Home"),
    ("PeakSport", "Sports"),
    ("PageTurner", "Books"),
    ("MediQuick", "Pharmacy"),
    ("PawStreet", "Pets"),
    ("Lumen Jewels", "Jewelry"),
]

FIRST_NAMES = [
    "Aarav", "Aditi", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Meera",
    "Neha", "Rohan", "Saanvi", "Vikram", "Zara", "Kabir", "Priya", "Rahul",
    "Sneha", "Dev", "Isha", "Nikhil", "Pooja", "Ayaan", "Tara", "Harsh",
    "Nisha", "Omar", "Riya", "Samir", "Leela", "Yash",
]

LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Khan", "Iyer", "Nair", "Gupta", "Das",
    "Mehta", "Joshi", "Kapoor", "Singh", "Rao", "Banerjee", "Chatterjee",
    "Malhotra", "Pillai", "Fernandes", "Dsouza", "Verma",
]

CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Jaipur", "Ahmedabad", "Kochi",
]

SEGMENTS = ("NEW", "REGULAR", "HIGH_VALUE", "AT_RISK", "DORMANT")
SEGMENT_WEIGHTS = (0.18, 0.38, 0.16, 0.16, 0.12)

CAMPAIGN_TYPES = (
    "RETENTION",
    "REACTIVATION",
    "CROSS_SELL",
    "UPSELL",
    "ACQUISITION",
)

CAMPAIGN_SEGMENT = {
    "RETENTION": "REGULAR",
    "REACTIVATION": "DORMANT",
    "CROSS_SELL": "REGULAR",
    "UPSELL": "HIGH_VALUE",
    "ACQUISITION": "NEW",
}

PAYMENT_METHODS = ("UPI", "CARD", "NETBANKING", "WALLET", "COD")
PAYMENT_METHOD_WEIGHTS = (0.45, 0.30, 0.10, 0.10, 0.05)
FAILURE_REASONS = (
    "GATEWAY_ERROR",
    "INSUFFICIENT_FUNDS",
    "TIMEOUT",
    "USER_CANCELLED",
)
FAILURE_WEIGHTS = (0.30, 0.35, 0.20, 0.15)

PRODUCT_TEMPLATES: dict[str, list[str]] = {
    "Fashion": ["Tee", "Jeans", "Sneakers", "Jacket", "Dress", "Hoodie"],
    "Grocery": ["Basmati Rice", "Olive Oil", "Coffee Beans", "Atta", "Spice Mix", "Tea"],
    "Electronics": ["Earbuds", "Power Bank", "Smartwatch", "Charger", "Speaker", "Mouse"],
    "Beauty": ["Serum", "Moisturizer", "Sunscreen", "Lip Tint", "Face Wash", "Perfume"],
    "Home": ["Lamp", "Cushion", "Cookware", "Organizer", "Throw", "Planter"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shorts", "Bottle", "Resistance Band", "Cap"],
    "Books": ["Paperback", "Hardcover", "Workbook", "Journal", "Comics", "Guide"],
    "Pharmacy": ["Vitamins", "Pain Relief", "Sanitizer", "Bandages", "Cough Syrup", "Thermometer"],
    "Pets": ["Dry Food", "Chew Toy", "Litter", "Collar", "Shampoo", "Treats"],
    "Jewelry": ["Studs", "Chain", "Bracelet", "Ring", "Pendant", "Bangle"],
}

PRICE_RANGES: dict[str, tuple[float, float]] = {
    "Fashion": (499, 4999),
    "Grocery": (49, 899),
    "Electronics": (799, 24999),
    "Beauty": (199, 3499),
    "Home": (299, 5999),
    "Sports": (249, 4999),
    "Books": (149, 1299),
    "Pharmacy": (49, 799),
    "Pets": (99, 2499),
    "Jewelry": (999, 34999),
}


def _money(value: float) -> float:
    return round(max(value, 0.0), 2)


def _clip(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _pick_name(rng: random.Random, used: set[str], customer_id: int) -> tuple[str, str]:
    for _ in range(20):
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        email = f"{name.lower().replace(' ', '.')}.{customer_id}@revora.test"
        if email not in used:
            used.add(email)
            return name, email
    email = f"customer.{customer_id}@revora.test"
    used.add(email)
    return f"Customer {customer_id}", email


def _segment_traits(segment: str, rng: random.Random) -> dict[str, Any]:
    if segment == "HIGH_VALUE":
        engagement = rng.uniform(72, 96)
        days = rng.randint(1, 21)
        sensitivity = rng.uniform(0.10, 0.40)
        age = rng.randint(28, 55)
    elif segment == "REGULAR":
        engagement = rng.uniform(42, 78)
        days = rng.randint(7, 45)
        sensitivity = rng.uniform(0.30, 0.65)
        age = rng.randint(22, 50)
    elif segment == "NEW":
        engagement = rng.uniform(50, 82)
        days = rng.randint(1, 18)
        sensitivity = rng.uniform(0.40, 0.80)
        age = rng.randint(18, 40)
    elif segment == "AT_RISK":
        engagement = rng.uniform(18, 48)
        days = rng.randint(45, 95)
        sensitivity = rng.uniform(0.55, 0.90)
        age = rng.randint(24, 58)
    else:
        engagement = rng.uniform(5, 28)
        days = rng.randint(96, 320)
        sensitivity = rng.uniform(0.50, 0.95)
        age = rng.randint(25, 62)

    return {
        "engagement_score": round(engagement, 2),
        "days_since_last_purchase": days,
        "discount_sensitivity": round(sensitivity, 4),
        "age": age,
    }


def _intended_order_count(segment: str, engagement: float, rng: random.Random) -> int:
    base = {
        "HIGH_VALUE": rng.randint(4, 8),
        "REGULAR": rng.randint(2, 5),
        "NEW": rng.randint(1, 2),
        "AT_RISK": rng.randint(1, 3),
        "DORMANT": rng.randint(0, 2),
    }[segment]
    if engagement > 85:
        base += 1
    return base


def _conversion_probability(engagement: float, days_since: int, segment: str) -> float:
    recency = _clip(1.0 - (days_since / 180.0), 0.0, 1.0)
    p = 0.18 + 0.50 * (engagement / 100.0) + 0.22 * recency
    if segment == "DORMANT":
        p -= 0.18
    elif segment == "AT_RISK":
        p -= 0.10
    elif segment == "HIGH_VALUE":
        p += 0.08
    return _clip(p, 0.08, 0.88)


def _payment_failure_probability(segment: str, method: str) -> float:
    p = 0.07
    if segment == "NEW":
        p += 0.04
    elif segment == "DORMANT":
        p += 0.03
    if method == "CARD":
        p += 0.03
    elif method == "NETBANKING":
        p += 0.02
    elif method == "UPI":
        p -= 0.02
    elif method == "COD":
        p = 0.02
    return _clip(p, 0.02, 0.22)


def _order_timestamps(
    rng: random.Random,
    created_at: datetime,
    days_since_last: int,
    count: int,
) -> list[datetime]:
    if count <= 0:
        return []
    last = AS_OF - timedelta(days=days_since_last, hours=rng.randint(0, 12))
    if last < created_at:
        last = created_at + timedelta(days=1)
    timestamps = [last]
    span_days = max((last - created_at).days, count + 1)
    for _ in range(count - 1):
        offset = rng.randint(0, span_days)
        ts = created_at + timedelta(days=offset, hours=rng.randint(0, 23))
        if ts > last:
            ts = last - timedelta(days=rng.randint(0, max(days_since_last, 1)))
        if ts < created_at:
            ts = created_at
        timestamps.append(ts)
    timestamps.sort()
    return timestamps


def _pick_products(
    rng: random.Random,
    catalog: list[dict[str, Any]],
    count: int,
) -> list[dict[str, Any]]:
    active = [p for p in catalog if p["is_active"]] or catalog
    k = min(count, len(active))
    return rng.sample(active, k=k)


def generate_commerce_data(seed: int = SEED) -> dict[str, list[dict[str, Any]]]:
    """Build a correlated synthetic commerce dataset with a fixed seed."""
    rng = random.Random(seed)

    merchants: list[dict[str, Any]] = []
    customers: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []
    carts: list[dict[str, Any]] = []
    cart_items: list[dict[str, Any]] = []
    orders: list[dict[str, Any]] = []
    order_items: list[dict[str, Any]] = []
    payments: list[dict[str, Any]] = []
    campaigns: list[dict[str, Any]] = []
    offers: list[dict[str, Any]] = []
    agent_actions: list[dict[str, Any]] = []
    audit_logs: list[dict[str, Any]] = []

    products_by_merchant: dict[int, list[dict[str, Any]]] = {}
    customers_by_merchant: dict[int, list[dict[str, Any]]] = {}
    customers_by_id: dict[int, dict[str, Any]] = {}
    abandoned_by_merchant: dict[int, list[int]] = {i: [] for i in range(1, 11)}
    campaign_revenue: dict[int, float] = {}

    product_id = 1
    for merchant_id, (name, category) in enumerate(MERCHANT_PROFILES, start=1):
        merchants.append(
            {
                "id": merchant_id,
                "name": name,
                "category": category,
                "monthly_revenue": 0,
                "conversion_rate": 0,
                "average_order_value": 0,
                "cart_abandonment_rate": 0,
                "repeat_purchase_rate": 0,
            }
        )
        catalog: list[dict[str, Any]] = []
        templates = PRODUCT_TEMPLATES[category]
        low, high = PRICE_RANGES[category]
        for i in range(30):
            template = templates[i % len(templates)]
            product = {
                "id": product_id,
                "merchant_id": merchant_id,
                "name": f"{name} {template} {i + 1}",
                "category": category,
                "price": _money(rng.uniform(low, high)),
                "stock_quantity": rng.randint(8, 420),
                "rating": round(rng.uniform(3.2, 4.9), 2),
                "is_active": rng.random() > 0.06,
            }
            catalog.append(product)
            products.append(product)
            product_id += 1
        products_by_merchant[merchant_id] = catalog

    used_emails: set[str] = set()
    customer_id = 1
    for merchant_id in range(1, 11):
        bucket: list[dict[str, Any]] = []
        for _ in range(500):
            segment = rng.choices(SEGMENTS, weights=SEGMENT_WEIGHTS, k=1)[0]
            traits = _segment_traits(segment, rng)
            tenure_days = traits["days_since_last_purchase"] + rng.randint(20, 420)
            created_at = AS_OF - timedelta(days=tenure_days, hours=rng.randint(0, 20))
            name, email = _pick_name(rng, used_emails, customer_id)
            row = {
                "id": customer_id,
                "merchant_id": merchant_id,
                "name": name,
                "email": email,
                "age": traits["age"],
                "city": rng.choice(CITIES),
                "customer_segment": segment,
                "lifetime_value": 0,
                "purchase_frequency": 0,
                "average_order_value": 0,
                "days_since_last_purchase": traits["days_since_last_purchase"],
                "discount_sensitivity": traits["discount_sensitivity"],
                "engagement_score": traits["engagement_score"],
                "created_at": created_at,
                "_intended_orders": _intended_order_count(
                    segment,
                    traits["engagement_score"],
                    rng,
                ),
            }
            customers.append(row)
            bucket.append(row)
            customers_by_id[customer_id] = row
            customer_id += 1
        customers_by_merchant[merchant_id] = bucket

    total_intended = sum(c["_intended_orders"] for c in customers)
    target_orders = 12_000
    if total_intended < target_orders:
        eligible = [c for c in customers if c["customer_segment"] in {"HIGH_VALUE", "REGULAR"}]
        idx = 0
        while total_intended < target_orders:
            eligible[idx % len(eligible)]["_intended_orders"] += 1
            total_intended += 1
            idx += 1
    elif total_intended > target_orders:
        eligible = [c for c in customers if c["_intended_orders"] > 0]
        rng.shuffle(eligible)
        idx = 0
        scanned = 0
        while total_intended > target_orders and scanned < len(customers) * 4:
            customer = eligible[idx % len(eligible)]
            if customer["_intended_orders"] > 0:
                customer["_intended_orders"] -= 1
                total_intended -= 1
            idx += 1
            scanned += 1

    order_id = 1
    order_item_id = 1
    payment_id = 1
    merchant_orders: dict[int, list[dict[str, Any]]] = {i: [] for i in range(1, 11)}
    customer_orders: dict[int, list[dict[str, Any]]] = {c["id"]: [] for c in customers}

    for customer in customers:
        catalog = products_by_merchant[customer["merchant_id"]]
        timestamps = _order_timestamps(
            rng,
            customer["created_at"],
            customer["days_since_last_purchase"],
            customer["_intended_orders"],
        )
        for ts in timestamps:
            chosen = _pick_products(rng, catalog, rng.randint(1, 4))
            items = []
            total = 0.0
            for product in chosen:
                qty = rng.randint(1, 3)
                if customer["customer_segment"] == "HIGH_VALUE":
                    qty = rng.randint(1, 4)
                unit = float(product["price"])
                total += unit * qty
                items.append((product["id"], qty, unit))
            total = _money(total)

            method = rng.choices(PAYMENT_METHODS, weights=PAYMENT_METHOD_WEIGHTS, k=1)[0]
            fail_p = _payment_failure_probability(customer["customer_segment"], method)
            failed = rng.random() < fail_p
            if failed:
                status = "PAYMENT_FAILED"
                pay_status = "FAILED"
                reason = rng.choices(FAILURE_REASONS, weights=FAILURE_WEIGHTS, k=1)[0]
                attempts = rng.randint(1, 3)
            else:
                age_days = (AS_OF - ts).days
                if age_days <= 2:
                    status = "CONFIRMED"
                elif age_days <= 6:
                    status = "SHIPPED"
                else:
                    status = "DELIVERED"
                pay_status = "SUCCESS"
                reason = None
                attempts = 1 if rng.random() > 0.12 else 2

            order = {
                "id": order_id,
                "customer_id": customer["id"],
                "merchant_id": customer["merchant_id"],
                "total_amount": total,
                "status": status,
                "order_date": ts,
            }
            orders.append(order)
            merchant_orders[customer["merchant_id"]].append(order)
            customer_orders[customer["id"]].append(order)

            for product_fk, qty, unit in items:
                order_items.append(
                    {
                        "id": order_item_id,
                        "order_id": order_id,
                        "product_id": product_fk,
                        "quantity": qty,
                        "unit_price": _money(unit),
                    }
                )
                order_item_id += 1

            payments.append(
                {
                    "id": payment_id,
                    "order_id": order_id,
                    "customer_id": customer["id"],
                    "amount": total,
                    "payment_method": method,
                    "status": pay_status,
                    "failure_reason": reason,
                    "attempt_number": attempts,
                    "created_at": ts + timedelta(minutes=rng.randint(1, 40)),
                }
            )
            payment_id += 1
            order_id += 1

    for customer in customers:
        own = customer_orders[customer["id"]]
        paid = [o for o in own if o["status"] != "PAYMENT_FAILED"]
        if paid:
            ltv = sum(float(o["total_amount"]) for o in paid)
            customer["lifetime_value"] = _money(ltv)
            customer["average_order_value"] = _money(ltv / len(paid))
            last = max(o["order_date"] for o in own)
            customer["days_since_last_purchase"] = max((AS_OF - last).days, 0)
            tenure_days = max((AS_OF - customer["created_at"]).days, 30)
            customer["purchase_frequency"] = round(len(paid) / (tenure_days / 30.0), 4)
        elif own:
            customer["lifetime_value"] = 0
            customer["average_order_value"] = _money(
                sum(float(o["total_amount"]) for o in own) / len(own)
            )
            last = max(o["order_date"] for o in own)
            customer["days_since_last_purchase"] = max((AS_OF - last).days, 0)
            customer["purchase_frequency"] = 0

    cart_id = 1
    cart_item_id = 1
    merchant_carts: dict[int, list[dict[str, Any]]] = {i: [] for i in range(1, 11)}
    while len(carts) < 8_000:
        customer = rng.choice(customers)
        catalog = products_by_merchant[customer["merchant_id"]]
        p_convert = _conversion_probability(
            float(customer["engagement_score"]),
            int(customer["days_since_last_purchase"]),
            customer["customer_segment"],
        )
        converted = rng.random() < p_convert
        chosen = _pick_products(rng, catalog, rng.randint(1, 4))
        total = 0.0
        line_items = []
        for product in chosen:
            qty = rng.randint(1, 3)
            unit = float(product["price"])
            total += unit * qty
            line_items.append((product["id"], qty, unit))
        created_at = AS_OF - timedelta(
            days=rng.randint(0, min(int(customer["days_since_last_purchase"]) + 14, 90)),
            hours=rng.randint(0, 23),
        )
        if created_at < customer["created_at"]:
            created_at = customer["created_at"]
        status = "CHECKED_OUT" if converted else "ABANDONED"
        cart = {
            "id": cart_id,
            "customer_id": customer["id"],
            "merchant_id": customer["merchant_id"],
            "total_value": _money(total),
            "status": status,
            "abandoned": not converted,
            "created_at": created_at,
        }
        carts.append(cart)
        merchant_carts[customer["merchant_id"]].append(cart)
        if not converted:
            abandoned_by_merchant[customer["merchant_id"]].append(customer["id"])
        for product_fk, qty, unit in line_items:
            cart_items.append(
                {
                    "id": cart_item_id,
                    "cart_id": cart_id,
                    "product_id": product_fk,
                    "quantity": qty,
                    "unit_price": _money(unit),
                }
            )
            cart_item_id += 1
        cart_id += 1

    campaign_id = 1
    for merchant_id, (name, _category) in enumerate(MERCHANT_PROFILES, start=1):
        for i in range(10):
            campaign_type = CAMPAIGN_TYPES[i % len(CAMPAIGN_TYPES)]
            target = CAMPAIGN_SEGMENT[campaign_type]
            if campaign_type == "REACTIVATION" and rng.random() < 0.5:
                target = "AT_RISK"
            created_at = AS_OF - timedelta(days=rng.randint(5, 120))
            row = {
                "id": campaign_id,
                "merchant_id": merchant_id,
                "name": f"{name} {campaign_type.replace('_', ' ').title()} {i + 1}",
                "campaign_type": campaign_type,
                "target_segment": target,
                "budget": _money(rng.uniform(25_000, 250_000)),
                "discount_percent": round(rng.uniform(8, 35), 2),
                "status": rng.choices(
                    ("ACTIVE", "PAUSED", "COMPLETED"),
                    weights=(0.6, 0.15, 0.25),
                    k=1,
                )[0],
                "revenue_generated": 0,
                "created_at": created_at,
            }
            campaigns.append(row)
            campaign_revenue[campaign_id] = 0.0
            campaign_id += 1

    offer_id = 1
    while len(offers) < 2_000:
        campaign = rng.choice(campaigns)
        pool = [
            c
            for c in customers_by_merchant[campaign["merchant_id"]]
            if c["customer_segment"] == campaign["target_segment"]
        ]
        if not pool:
            pool = customers_by_merchant[campaign["merchant_id"]]
        weights = [float(c["discount_sensitivity"]) + 0.05 for c in pool]
        customer = rng.choices(pool, weights=weights, k=1)[0]
        discount = float(campaign["discount_percent"])
        sensitivity = float(customer["discount_sensitivity"])
        engagement = float(customer["engagement_score"]) / 100.0
        recency = _clip(1.0 - int(customer["days_since_last_purchase"]) / 180.0, 0.0, 1.0)
        p_convert = _clip(
            0.08
            + 0.55 * sensitivity
            + 0.18 * (discount / 40.0)
            + 0.12 * engagement
            + 0.10 * recency,
            0.04,
            0.92,
        )
        if rng.random() < p_convert:
            status = "ACCEPTED"
        elif rng.random() < 0.18:
            status = "EXPIRED"
        else:
            status = "DECLINED" if rng.random() < 0.55 else "SENT"
        expected_revenue = _money(
            float(customer["average_order_value"] or rng.uniform(400, 2200))
            * (1 - discount / 100.0)
            * p_convert
        )
        created_at = max(campaign["created_at"], customer["created_at"]) + timedelta(
            days=rng.randint(0, 20)
        )
        if created_at > AS_OF:
            created_at = AS_OF - timedelta(hours=rng.randint(1, 48))
        offers.append(
            {
                "id": offer_id,
                "merchant_id": campaign["merchant_id"],
                "customer_id": customer["id"],
                "campaign_id": campaign["id"],
                "discount_percent": discount,
                "expected_conversion_probability": round(p_convert, 4),
                "expected_revenue": expected_revenue,
                "status": status,
                "created_at": created_at,
            }
        )
        if status == "ACCEPTED":
            campaign_revenue[campaign["id"]] += expected_revenue
        offer_id += 1

    for campaign in campaigns:
        campaign["revenue_generated"] = _money(campaign_revenue[campaign["id"]])

    action_id = 1
    audit_id = 1
    while len(agent_actions) < 3_000:
        merchant_id = rng.randint(1, 10)
        merchant_customers = customers_by_merchant[merchant_id]
        roll = rng.random()
        if roll < 0.28 and abandoned_by_merchant[merchant_id]:
            customer = customers_by_id[rng.choice(abandoned_by_merchant[merchant_id])]
            action_type = "CART_RECOVERY"
            reason = "Customer left a high-value cart without checkout."
        elif roll < 0.50:
            at_risk_pool = [
                c
                for c in merchant_customers
                if c["customer_segment"] in {"AT_RISK", "DORMANT"}
            ]
            customer = rng.choice(at_risk_pool or merchant_customers)
            action_type = (
                "REACTIVATION_NUDGE"
                if customer["customer_segment"] == "DORMANT"
                else "WINBACK"
            )
            reason = f"{customer['customer_segment']} customer with low recent activity."
        elif roll < 0.72:
            customer = rng.choice(merchant_customers)
            action_type = "SEND_OFFER"
            reason = "Discount sensitivity and campaign fit exceeded send threshold."
        elif roll < 0.88:
            hv_pool = [
                c for c in merchant_customers if c["customer_segment"] == "HIGH_VALUE"
            ]
            customer = rng.choice(hv_pool or merchant_customers)
            action_type = "UPSELL_PROMPT"
            reason = "High-value customer eligible for premium bundle upsell."
        else:
            regular_pool = [
                c for c in merchant_customers if c["customer_segment"] == "REGULAR"
            ]
            customer = rng.choice(regular_pool or merchant_customers)
            action_type = "CROSS_SELL_PROMPT"
            reason = "Regular buyer likely to add an adjacent category item."

        engagement = float(customer["engagement_score"])
        if engagement < 20:
            policy_status = rng.choices(
                ("ALLOWED", "REVIEW", "BLOCKED"),
                weights=(0.55, 0.30, 0.15),
                k=1,
            )[0]
        else:
            policy_status = rng.choices(
                ("ALLOWED", "REVIEW", "BLOCKED"),
                weights=(0.82, 0.14, 0.04),
                k=1,
            )[0]

        if policy_status == "BLOCKED":
            approval_status = "REJECTED"
            execution_status = "SKIPPED"
        elif policy_status == "REVIEW":
            approval_status = rng.choices(
                ("PENDING", "APPROVED", "REJECTED"),
                weights=(0.35, 0.50, 0.15),
                k=1,
            )[0]
            execution_status = {
                "PENDING": "QUEUED",
                "APPROVED": "EXECUTED",
                "REJECTED": "SKIPPED",
            }[approval_status]
        else:
            approval_status = "AUTO_APPROVED"
            execution_status = "EXECUTED" if rng.random() > 0.06 else "FAILED"

        created_at = AS_OF - timedelta(days=rng.randint(0, 60), hours=rng.randint(0, 23))
        agent_actions.append(
            {
                "id": action_id,
                "merchant_id": merchant_id,
                "customer_id": customer["id"],
                "action_type": action_type,
                "reason": reason,
                "expected_impact": f"Lift conversion for {customer['customer_segment']} cohort",
                "policy_status": policy_status,
                "approval_status": approval_status,
                "execution_status": execution_status,
                "created_at": created_at,
            }
        )
        audit_logs.append(
            {
                "id": audit_id,
                "agent_action_id": action_id,
                "event_type": "ACTION_CREATED",
                "message": f"Created {action_type} for customer {customer['id']}.",
                "metadata_json": {
                    "segment": customer["customer_segment"],
                    "engagement_score": customer["engagement_score"],
                },
                "created_at": created_at,
            }
        )
        audit_id += 1
        audit_logs.append(
            {
                "id": audit_id,
                "agent_action_id": action_id,
                "event_type": f"ACTION_{execution_status}",
                "message": (
                    f"Policy={policy_status}; approval={approval_status}; "
                    f"execution={execution_status}."
                ),
                "metadata_json": {
                    "policy_status": policy_status,
                    "approval_status": approval_status,
                    "execution_status": execution_status,
                },
                "created_at": created_at + timedelta(minutes=rng.randint(1, 25)),
            }
        )
        audit_id += 1
        action_id += 1

    for merchant in merchants:
        mid = merchant["id"]
        paid_orders = [o for o in merchant_orders[mid] if o["status"] != "PAYMENT_FAILED"]
        merchant_cart_rows = merchant_carts[mid]
        monthly_cutoff = AS_OF - timedelta(days=30)
        monthly = [o for o in paid_orders if o["order_date"] >= monthly_cutoff]
        merchant["monthly_revenue"] = _money(sum(float(o["total_amount"]) for o in monthly))
        if paid_orders:
            merchant["average_order_value"] = _money(
                sum(float(o["total_amount"]) for o in paid_orders) / len(paid_orders)
            )
        if merchant_cart_rows:
            abandoned = sum(1 for c in merchant_cart_rows if c["abandoned"])
            converted = len(merchant_cart_rows) - abandoned
            merchant["cart_abandonment_rate"] = round(abandoned / len(merchant_cart_rows), 4)
            merchant["conversion_rate"] = round(converted / len(merchant_cart_rows), 4)
        buyers = [
            cid
            for cid, rows in customer_orders.items()
            if customers_by_id[cid]["merchant_id"] == mid and rows
        ]
        repeat = [
            cid
            for cid in buyers
            if sum(1 for o in customer_orders[cid] if o["status"] != "PAYMENT_FAILED") >= 2
        ]
        merchant["repeat_purchase_rate"] = round((len(repeat) / len(buyers)) if buyers else 0, 4)

    for customer in customers:
        customer.pop("_intended_orders", None)

    return {
        "merchants": merchants,
        "customers": customers,
        "products": products,
        "carts": carts,
        "cart_items": cart_items,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "campaigns": campaigns,
        "offers": offers,
        "agent_actions": agent_actions,
        "audit_logs": audit_logs,
    }
