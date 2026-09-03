from pathlib import Path
import joblib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer, Order


MODEL_PATH = Path("models/reactivation_model.joblib")
_model = None


def load_model():
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Run: python -m app.ml.train_models"
            )
        _model = joblib.load(MODEL_PATH)

    return _model


def predict_reactivation_probability(
    db: Session,
    customer: Customer,
) -> float:
    """Predict reactivation probability using the same features used during training."""

    orders = db.scalars(
        select(Order)
        .where(Order.customer_id == customer.id)
        .order_by(Order.order_date)
    ).all()

    if not orders:
        return 0.05

    # Match the training feature construction.
    order_count = len(orders)
    total_spend = sum(float(o.total_amount) for o in orders)
    avg_order_value = total_spend / order_count

    last_order_date = max(o.order_date for o in orders)

    # Training used these eight features.
    features = [[
        order_count,
        avg_order_value,
        total_spend,
        customer.days_since_last_purchase,
        float(customer.engagement_score),
        float(customer.discount_sensitivity),
        float(customer.purchase_frequency),
        float(customer.lifetime_value),
    ]]

    probability = load_model().predict_proba(features)[0][1]

    return round(float(probability), 4)