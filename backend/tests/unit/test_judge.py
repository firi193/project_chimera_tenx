"""Unit tests for Judge service: confidence and routing (constitution thresholds)."""
import pytest

from services.judge.service import evaluate


def test_evaluate_sensitive_topic_always_review_queue():
    """Sensitive-topic content must always be routed to review_queue (constitution)."""
    score, routing = evaluate("some content", sensitive_topic_flags=["politics"])
    assert routing == "review_queue"
    score2, routing2 = evaluate("any text", sensitive_topic_flags=["health"])
    assert routing2 == "review_queue"


def test_evaluate_high_confidence_auto_approved():
    """Long content yields high confidence and auto_approved (stub heuristic)."""
    long_content = "x" * 500
    score, routing = evaluate(long_content)
    assert score > 0.90
    assert routing == "auto_approved"


def test_evaluate_low_confidence_rejected():
    """Very short content yields low confidence and rejected."""
    short = "hi"
    score, routing = evaluate(short)
    assert score < 0.70
    assert routing == "rejected"


def test_evaluate_medium_confidence_review_queue():
    """Content of medium length can land in review_queue band (0.70–0.90)."""
    # Stub: 0.5 + len/500. To get ~0.80 we need len ~150
    medium = "a" * 150
    score, routing = evaluate(medium)
    assert 0.70 <= score <= 0.90
    assert routing == "review_queue"


def test_evaluate_empty_content():
    """Empty content is low confidence."""
    score, routing = evaluate("")
    assert score <= 0.70
    assert routing in ("rejected", "review_queue")
