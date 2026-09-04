import pytest
from starlette.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Revora AI"
    assert data["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_merchants_list(client):
    response = client.get("/api/merchants")
    assert response.status_code == 200
    merchants = response.json()
    assert len(merchants) >= 10
    merchant_10 = next((m for m in merchants if m["id"] == 10), None)
    assert merchant_10 is not None
    assert merchant_10["name"] == "Lumen Jewels"
    assert merchant_10["category"] == "Jewelry"


def test_revenue_overview(client):
    response = client.get("/api/revenue/overview?merchant_id=10")
    assert response.status_code == 200
    data = response.json()
    assert "total_current_revenue" in data
    assert "total_estimated_opportunity" in data
    assert "opportunity_breakdown" in data
    assert "high_priority_count" in data
    assert "top_opportunities" in data
    assert float(data["total_current_revenue"]) > 0
    assert float(data["total_estimated_opportunity"]) > 0


def test_revenue_opportunities(client):
    response = client.get("/api/revenue/opportunities?merchant_id=10&limit=5")
    assert response.status_code == 200
    opportunities = response.json()
    assert len(opportunities) <= 5
    if opportunities:
        first = opportunities[0]
        assert "opportunity_type" in first
        assert "title" in first
        assert "estimated_revenue" in first
        assert "confidence" in first
        assert "priority" in first
        assert "recommended_action" in first


def test_agent_analyze(client):
    response = client.post("/api/agent/analyze/10?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["merchant_id"] == 10
    assert "recommendations" in data
    assert len(data["recommendations"]) == 2
    rec = data["recommendations"][0]
    assert "opportunity" in rec
    assert "policy_decision" in rec
    assert "llm_explanation" in rec
    assert "allowed" in rec["policy_decision"]
    assert "requires_approval" in rec["policy_decision"]


def test_agent_actions(client):
    response = client.get("/api/agent/actions/10?limit=10")
    assert response.status_code == 200
    actions = response.json()
    assert isinstance(actions, list)
    assert len(actions) > 0
    action = actions[0]
    assert "action_type" in action
    assert "expected_impact" in action
    assert "policy_status" in action
    assert "approval_status" in action
    assert "execution_status" in action


def test_agent_audit_logs(client):
    response = client.get("/api/agent/audit-logs/10?limit=10")
    assert response.status_code == 200
    logs = response.json()
    assert isinstance(logs, list)
    assert len(logs) > 0
    log = logs[0]
    assert "event_type" in log
    assert "message" in log
    assert "agent_action_id" in log


def test_agent_actions_count(client):
    response = client.get("/api/agent/actions-count/10")
    assert response.status_code == 200
    data = response.json()
    assert data["merchant_id"] == 10
    assert "total_actions" in data
    assert data["total_actions"] >= 300


def test_rag_policy_guardrails():
    from app.rag.knowledge_base import retrieve_policies
    from app.rag.policy_engine import validate_action

    # Cart recovery should match policy and require approval
    policies = retrieve_policies("ABANDONED_CART_RECOVERY")
    policy_ids = [p["id"] for p in policies]
    assert "cart_recovery" in policy_ids

    decision = validate_action(
        action_type="SEND_CART_RECOVERY_OFFER",
        estimated_revenue=5000.0,
        confidence=0.85,
        policy_ids=policy_ids,
    )
    assert decision.allowed is True
    assert decision.requires_approval is True

    # Low confidence action (<0.40) must be BLOCKED
    blocked_decision = validate_action(
        action_type="SEND_CART_RECOVERY_OFFER",
        estimated_revenue=5000.0,
        confidence=0.35,
        policy_ids=policy_ids,
    )
    assert blocked_decision.allowed is False
    assert "below the minimum action threshold" in blocked_decision.reason


def test_ml_reactivation_prediction():
    from app.core.database import SessionLocal
    from app.models import Customer
    from app.ml.predict import predict_reactivation_probability

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.days_since_last_purchase >= 90).first()
        assert customer is not None
        prob = predict_reactivation_probability(db, customer)
        assert 0.0 <= prob <= 1.0
    finally:
        db.close()


def test_agent_action_deduplication(client):
    r1 = client.post("/api/agent/analyze/10?limit=2").json()
    r2 = client.post("/api/agent/analyze/10?limit=2").json()
    ids1 = [rec["action_id"] for rec in r1["recommendations"] if rec["action_id"] is not None]
    ids2 = [rec["action_id"] for rec in r2["recommendations"] if rec["action_id"] is not None]
    assert len(ids1) > 0
    assert ids1 == ids2

