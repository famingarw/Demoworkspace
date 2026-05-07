"""Faminga WiSK demo project package."""

from .soil_rules import (
    classify_intervention_priority,
    load_field_rows,
    recommendation_for_field,
    summarize_fields,
)

__all__ = [
    "classify_intervention_priority",
    "load_field_rows",
    "recommendation_for_field",
    "summarize_fields",
]
