"""Create tables and seed the local SQLite database with synthetic commerce data.

Run from the backend directory:

    python scripts/seed_database.py
"""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.models import (
    AgentAction,
    AuditLog,
    Campaign,
    Cart,
    CartItem,
    Customer,
    Merchant,
    Offer,
    Order,
    OrderItem,
    Payment,
    Product,
)
from generate_data import generate_commerce_data

# SQLite has a bound-variable limit; keep chunks small enough for wide rows.
INSERT_CHUNK_SIZE = 200

INSERT_ORDER = (
    ("merchants", Merchant),
    ("customers", Customer),
    ("products", Product),
    ("campaigns", Campaign),
    ("carts", Cart),
    ("cart_items", CartItem),
    ("orders", Order),
    ("order_items", OrderItem),
    ("payments", Payment),
    ("offers", Offer),
    ("agent_actions", AgentAction),
    ("audit_logs", AuditLog),
)


def _chunked_insert(session: Session, model, rows: list[dict], chunk_size: int = INSERT_CHUNK_SIZE) -> None:
    if not rows:
        return
    table = model.__table__
    for start in range(0, len(rows), chunk_size):
        session.execute(insert(table), rows[start : start + chunk_size])


def seed_database() -> dict[str, int]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    dataset = generate_commerce_data()
    session = SessionLocal()
    try:
        for key, model in INSERT_ORDER:
            _chunked_insert(session, model, dataset[key])
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return {key: len(rows) for key, rows in dataset.items()}


def main() -> None:
    counts = seed_database()
    print("Revora database seeded")
    print(f"  merchants created: {counts['merchants']}")
    print(f"  customers created: {counts['customers']}")
    print(f"  products created: {counts['products']}")
    print(f"  carts created: {counts['carts']}")
    print(f"  orders created: {counts['orders']}")
    print(f"  payments created: {counts['payments']}")
    print(f"  campaigns created: {counts['campaigns']}")
    print(f"  offers created: {counts['offers']}")
    print(f"  agent actions created: {counts['agent_actions']}")
    print(f"  audit logs created: {counts['audit_logs']}")
    print(f"  cart items created: {counts['cart_items']}")
    print(f"  order items created: {counts['order_items']}")


if __name__ == "__main__":
    main()
