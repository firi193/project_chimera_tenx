"""Judge service (T019): validate output, assign confidence score, apply routing.

Routing: auto_approved (high), review_queue (medium), rejected (low).
Sensitive-topic content always goes to review_queue.
"""
from __future__ import annotations

from services.judge.config import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM


def evaluate(
    output_content: str,
    sensitive_topic_flags: list[str] | None = None,
) -> tuple[float, str]:
    """Evaluate agent output and return (confidence_score, routing).

    routing is one of: auto_approved, review_queue, rejected.
    """
    sensitive_topic_flags = sensitive_topic_flags or []
    if sensitive_topic_flags:
        # Constitution: sensitive topic always -> human review
        return (0.0, "review_queue")  # confidence not used for routing when sensitive

    # Stub: assign a deterministic confidence from content length for demo
    # In production this would be from a model or heuristic
    raw = min(1.0, 0.5 + len(output_content) / 500.0)
    confidence = round(raw, 2)

    if confidence > CONFIDENCE_HIGH:
        routing = "auto_approved"
    elif confidence >= CONFIDENCE_MEDIUM:
        routing = "review_queue"
    else:
        routing = "rejected"
    return (confidence, routing)
