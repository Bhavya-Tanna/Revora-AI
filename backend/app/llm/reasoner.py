import os

from openai import OpenAI


def explain_opportunity(opportunity: dict, policy_decision: dict) -> str:
    fallback = (
        f"{opportunity['title']}. "
        f"Estimated revenue impact is "
        f"₹{float(opportunity['estimated_revenue']):,.2f}. "
        f"Confidence is {float(opportunity['confidence']):.0%}. "
        f"Recommended action: {opportunity['recommended_action']}."
    )

    api_key = os.getenv("OPENAI_API_KEY")

    # LLM is optional for the MVP.
    if not api_key:
        return fallback

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
You are Revora AI, a revenue growth analyst.

Opportunity:
Type: {opportunity['opportunity_type']}
Title: {opportunity['title']}
Description: {opportunity['description']}
Estimated Revenue: ₹{opportunity['estimated_revenue']}
Confidence: {opportunity['confidence']}
Priority: {opportunity['priority']}
Recommended Action: {opportunity['recommended_action']}

Policy:
Allowed: {policy_decision['allowed']}
Approval Required: {policy_decision['requires_approval']}
Reason: {policy_decision['reason']}

Explain in 2 concise sentences why this opportunity matters
and what the merchant should do. Do not invent information.
""",
        )

        return response.output_text.strip()

    except Exception:
        # Never allow an LLM failure to break the revenue agent.
        return fallback