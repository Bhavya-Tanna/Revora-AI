POLICY_DOCUMENTS = [
    {
        "id": "payment_recovery",
        "title": "Payment Recovery Policy",
        "content": (
            "Failed payments may be retried when the failure is temporary, "
            "such as gateway errors or timeouts. Insufficient-funds failures "
            "should not be repeatedly retried. Payment actions must respect "
            "customer safety and transaction limits."
        ),
    },
    {
        "id": "cart_recovery",
        "title": "Cart Recovery Policy",
        "content": (
            "Abandoned cart recovery may use a targeted offer when the "
            "estimated recovery value justifies the incentive. Discounts "
            "must remain within merchant-configured limits."
        ),
    },
    {
        "id": "customer_reactivation",
        "title": "Customer Reactivation Policy",
        "content": (
            "Dormant customers may receive personalized reactivation offers. "
            "High-value customers should receive higher priority. Offers "
            "should be relevant to previous customer activity."
        ),
    },
    {
        "id": "cross_sell",
        "title": "Cross-Sell Recommendation Policy",
        "content": (
            "Cross-sell product recommendations should be personalized based on "
            "customer order history and purchase frequency. Low-friction product "
            "suggestions do not require financial approval but must respect customer "
            "segmentation and product availability."
        ),
    },
    {
        "id": "agent_safety",
        "title": "AI Agent Safety Policy",
        "content": (
            "The AI agent must never execute financial actions without "
            "policy validation. High-impact actions require explicit approval. "
            "Every executed or rejected action must be recorded in the audit log."
        ),
    },
]


def retrieve_policies(query: str, top_k: int = 3) -> list[dict]:
    """
    Lightweight keyword-based retrieval.
    This provides the RAG contract without requiring an embedding service.
    """

    query_words = set(query.lower().replace("_", " ").split())

    scored = []

    for document in POLICY_DOCUMENTS:
        text = (
            document["title"] + " " + document["content"]
        ).lower()

        score = sum(
            1 for word in query_words
            if len(word) > 3 and word in text
        )

        scored.append((score, document))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        document
        for score, document in scored[:top_k]
        if score > 0
    ]