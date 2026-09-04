from sqlalchemy.orm import Session

from app.llm.reasoner import explain_opportunity
from app.rag.knowledge_base import retrieve_policies
from app.rag.policy_engine import validate_action
from app.services.revenue_intelligence import (
    calculate_revenue_opportunities,
)
from app.agents.tools import create_agent_action
from app.models.agent_action import AgentAction


class GrowthAgent:

    def __init__(self, db: Session):
        self.db = db

    def analyze(
        self,
        merchant_id: int,
        limit: int = 10,
    ) -> dict:

        opportunities = calculate_revenue_opportunities(
            self.db,
            merchant_id=merchant_id,
            limit=limit,
        )

        recommendations = []

        for opportunity in opportunities:

            action_type = opportunity["recommended_action"]

            policies = retrieve_policies(
                opportunity["opportunity_type"]
            )

            policy_ids = [
                policy["id"]
                for policy in policies
            ]

            decision = validate_action(
                action_type=action_type,
                estimated_revenue=float(
                    opportunity["estimated_revenue"]
                ),
                confidence=opportunity["confidence"],
                policy_ids=policy_ids,
            )

            policy_decision = {
                "allowed": decision.allowed,
                "requires_approval": decision.requires_approval,
                "reason": decision.reason,
                "policy_ids": decision.policy_ids,
            }

            recommendation = {
                "opportunity": opportunity,
                "policy_decision": policy_decision,
                "llm_explanation": explain_opportunity(
                    opportunity,
                    policy_decision,
                ),
            }

            if decision.allowed:
                approval_status = (
                    "REQUIRED"
                    if decision.requires_approval
                    else "NOT_REQUIRED"
                )

                # Safe deduplication: reuse active PENDING action for same customer & action type
                existing_action = (
                    self.db.query(AgentAction)
                    .filter(
                        AgentAction.merchant_id == opportunity["merchant_id"],
                        AgentAction.customer_id == opportunity["customer_id"],
                        AgentAction.action_type == action_type,
                        AgentAction.execution_status == "PENDING",
                    )
                    .order_by(AgentAction.created_at.desc())
                    .first()
                )

                if existing_action:
                    action = existing_action
                else:
                    action = create_agent_action(
                        db=self.db,
                        merchant_id=opportunity["merchant_id"],
                        customer_id=opportunity["customer_id"],
                        action_type=action_type,
                        reason=opportunity["description"],
                        expected_impact=(
                            f"Estimated revenue impact: "
                            f"₹{float(opportunity['estimated_revenue']):,.2f}"
                        ),
                        policy_status="APPROVED",
                        approval_status=approval_status,
                    )

                recommendation["action_id"] = action.id

            else:
                recommendation["action_id"] = None

            recommendations.append(recommendation)

        return {
            "merchant_id": merchant_id,
            "opportunities_analyzed": len(opportunities),
            "recommendations": recommendations,
        }