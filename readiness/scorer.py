from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from readiness.models import Assessment, UseCase
from readiness.recommendations import build_recommendations


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_framework() -> dict[str, Any]:
    return load_yaml(CONFIG_DIR / "scoring_framework.yaml")


def score_use_case(use_case: UseCase, framework: dict[str, Any] | None = None) -> Assessment:
    framework = framework or load_framework()
    dimensions = framework["dimensions"]
    penalties = framework["penalties"]

    dimension_scores = {
        name: _score_dimension(use_case, name, rules)
        for name, rules in dimensions.items()
    }

    weighted_score = sum(
        dimension_scores[name] * dimensions[name]["weight"]
        for name in dimensions
    )

    penalty = _calculate_penalty(use_case, penalties)
    score = max(0, min(100, round(weighted_score - penalty)))
    risk_level = _risk_level(score, use_case)
    recommendation = _recommendation(score, risk_level)

    recs = build_recommendations(use_case, score, risk_level, dimension_scores)

    return Assessment(
        score=score,
        risk_level=risk_level,
        recommendation=recommendation,
        dimension_scores=dimension_scores,
        **recs,
    )


def _score_dimension(use_case: UseCase, name: str, rules: dict[str, Any]) -> int:
    base = rules["base"]
    score = base

    for check in rules.get("checks", []):
        field_value = getattr(use_case, check["field"])
        expected = check["equals"]
        delta = check["delta"]

        if field_value == expected:
            score += delta

    for check in rules.get("contains_checks", []):
        values = [value.lower() for value in getattr(use_case, check["field"])]
        if any(item.lower() in values for item in check["contains_any"]):
            score += check["delta"]

    return max(0, min(100, score))


def _calculate_penalty(use_case: UseCase, penalties: dict[str, int]) -> int:
    penalty = 0

    if use_case.regulated_context:
        penalty += penalties["regulated_context"]
    if use_case.customer_authentication == "not_defined":
        penalty += penalties["undefined_authentication"]
    if use_case.human_handover in {"none", "partial"}:
        penalty += penalties["weak_handover"]
    if use_case.autonomy_level in {"transactional", "decisioning"}:
        penalty += penalties["high_autonomy"]
    if use_case.fraud_risk == "high":
        penalty += penalties["high_fraud_risk"]
    if len(use_case.languages) >= 3:
        penalty += penalties["multilingual_complexity"]
    if use_case.latency_target_ms > 1500:
        penalty += penalties["latency_above_threshold"]

    return penalty


def _risk_level(score: int, use_case: UseCase) -> str:
    if use_case.regulated_context and use_case.autonomy_level == "decisioning":
        return "Critical"
    if score >= 80:
        return "Moderate"
    if score >= 65:
        return "Elevated"
    if score >= 50:
        return "High"
    return "Critical"


def _recommendation(score: int, risk_level: str) -> str:
    if score >= 80 and risk_level == "Moderate":
        return "Proceed to controlled production pilot with strict monitoring."
    if score >= 65:
        return "Pilot only, with restricted scope and clear human escalation."
    if score >= 50:
        return "Promising, but not production-ready. Run a narrow internal or shadow pilot first."
    return "No-go for customer-facing deployment until core controls are defined."
