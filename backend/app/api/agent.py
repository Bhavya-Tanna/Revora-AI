from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.agents.growth_agent import GrowthAgent
from app.core.database import get_db


router = APIRouter(
    prefix="/api/agent",
    tags=["Growth Agent"],
)


@router.post("/analyze/{merchant_id}")
def analyze_merchant(
    merchant_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    agent = GrowthAgent(db)

    return agent.analyze(
        merchant_id=merchant_id,
        limit=limit,
    )


@router.get("/actions/{merchant_id}")
def get_merchant_actions(
    merchant_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    from app.models.agent_action import AgentAction

    actions = (
        db.query(AgentAction)
        .filter(AgentAction.merchant_id == merchant_id)
        .order_by(AgentAction.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "merchant_id": a.merchant_id,
            "customer_id": a.customer_id,
            "customer_name": a.customer.name if a.customer else f"Customer #{a.customer_id}",
            "customer_email": a.customer.email if a.customer else None,
            "action_type": a.action_type,
            "reason": a.reason,
            "expected_impact": a.expected_impact,
            "policy_status": a.policy_status,
            "approval_status": a.approval_status,
            "execution_status": a.execution_status,
            "created_at": a.created_at.isoformat(),
        }
        for a in actions
    ]


@router.get("/audit-logs/{merchant_id}")
def get_merchant_audit_logs(
    merchant_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    from app.models.agent_action import AgentAction
    from app.models.audit_log import AuditLog

    logs = (
        db.query(AuditLog)
        .join(AgentAction, AuditLog.agent_action_id == AgentAction.id)
        .filter(AgentAction.merchant_id == merchant_id)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": log.id,
            "agent_action_id": log.agent_action_id,
            "event_type": log.event_type,
            "message": log.message,
            "metadata": log.metadata_json or {},
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]


@router.get("/actions-count/{merchant_id}")
def get_merchant_actions_count(
    merchant_id: int,
    db: Session = Depends(get_db),
):
    from app.models.agent_action import AgentAction

    count = (
        db.query(AgentAction)
        .filter(AgentAction.merchant_id == merchant_id)
        .count()
    )

    return {
        "merchant_id": merchant_id,
        "total_actions": count,
    }
