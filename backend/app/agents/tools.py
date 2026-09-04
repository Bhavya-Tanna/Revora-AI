from datetime import datetime

from sqlalchemy.orm import Session

from app.models import AgentAction, AuditLog


def create_agent_action(
    db: Session,
    merchant_id: int,
    customer_id: int | None,
    action_type: str,
    reason: str,
    expected_impact: str,
    policy_status: str,
    approval_status: str,
    execution_status: str = "PENDING",
) -> AgentAction:

    action = AgentAction(
        merchant_id=merchant_id,
        customer_id=customer_id,
        action_type=action_type,
        reason=reason,
        expected_impact=expected_impact,
        policy_status=policy_status,
        approval_status=approval_status,
        execution_status=execution_status,
        created_at=datetime.utcnow(),
    )

    db.add(action)
    db.flush()

    audit = AuditLog(
        agent_action_id=action.id,
        event_type="AGENT_ACTION_CREATED",
        message=reason,
        metadata_json={
            "action_type": action_type,
            "expected_impact": expected_impact,
            "policy_status": policy_status,
            "approval_status": approval_status,
        },
        created_at=datetime.utcnow(),
    )

    db.add(audit)
    db.commit()
    db.refresh(action)

    return action