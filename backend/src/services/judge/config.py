"""Confidence threshold configuration (T020). Constitution: high > 0.90, medium 0.70–0.90, low < 0.70."""
from config import settings

CONFIDENCE_HIGH = settings.confidence_high   # > this -> auto_approved
CONFIDENCE_MEDIUM = settings.confidence_medium  # >= this and <= HIGH -> review_queue; < this -> rejected
