from pathlib import Path
import joblib
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sqlalchemy import select
from app.core.database import SessionLocal
from app.models import Customer, Order


MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def train_reactivation_model():
    db = SessionLocal()

    try:
        customers = db.scalars(select(Customer)).all()
        orders = db.scalars(select(Order).order_by(Order.order_date)).all()

        if len(orders) < 100:
            raise RuntimeError("Not enough orders to train the model.")

        # Use a historical cutoff so the model learns from past behaviour.
        cutoff_index = int(len(orders) * 0.70)
        cutoff_date = orders[cutoff_index].order_date

        historical = [o for o in orders if o.order_date <= cutoff_date]
        future = [o for o in orders if o.order_date > cutoff_date]

        orders_by_customer = {}

        for order in historical:
            orders_by_customer.setdefault(order.customer_id, []).append(order)

        future_customers = {o.customer_id for o in future}

        X = []
        y = []

        for customer in customers:
            history = orders_by_customer.get(customer.id, [])

            if not history:
                continue

            order_count = len(history)
            total_spend = sum(float(o.total_amount) for o in history)
            avg_order_value = total_spend / order_count

            last_order_date = max(o.order_date for o in history)
            days_since_last_order = max(
                0,
                (cutoff_date - last_order_date).days,
            )

            X.append([
                order_count,
                avg_order_value,
                total_spend,
                days_since_last_order,
                float(customer.engagement_score),
                float(customer.discount_sensitivity),
                float(customer.purchase_frequency),
                float(customer.lifetime_value),
            ])

            y.append(1 if customer.id in future_customers else 0)

        X = np.asarray(X)
        y = np.asarray(y)

        if len(set(y)) < 2:
            raise RuntimeError("Training data contains only one target class.")

        model = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(
                max_iter=1000,
                random_state=42,
            )),
        ])

        model.fit(X, y)

        output = MODEL_DIR / "reactivation_model.joblib"
        joblib.dump(model, output)

        print("Reactivation ML model trained successfully.")
        print(f"Training samples: {len(X)}")
        print(f"Positive samples: {int(y.sum())}")
        print(f"Negative samples: {int(len(y) - y.sum())}")
        print(f"Model saved to: {output}")

    finally:
        db.close()


if __name__ == "__main__":
    train_reactivation_model()