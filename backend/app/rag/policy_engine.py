from dataclasses import dataclass


@dataclass
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str
    policy_ids: list[str]


HIGH_IMPACT_ACTIONS = {
    "RETRY_PAYMENT",
    "SEND_CART_RECOVERY_OFFER",
    "SEND_REACTIVATION_OFFER",
}


def validate_action(
    action_type: str,
    estimated_revenue: float,
    confidence: float,
    policy_ids: list[str],
) -> PolicyDecision:

    if confidence < 0.40:
        return PolicyDecision(
            allowed=False,
            requires_approval=False,
            reason="Confidence is below the minimum action threshold.",
            policy_ids=policy_ids,
        )

    if estimated_revenue <= 0:
        return PolicyDecision(
            allowed=False,
            requires_approval=False,
            reason="Estimated revenue must be positive.",
            policy_ids=policy_ids,
        )

    if action_type in HIGH_IMPACT_ACTIONS:
        return PolicyDecision(
            allowed=True,
            requires_approval=True,
            reason=(
                "Action is permitted but requires merchant approval "
                "because it can affect customers or financial transactions."
            ),
            policy_ids=policy_ids,
        )

    return PolicyDecision(
        allowed=True,
        requires_approval=False,
        reason="Action passed policy validation.",
        policy_ids=policy_ids,
    )