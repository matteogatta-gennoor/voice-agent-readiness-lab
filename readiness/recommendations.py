from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from readiness.models import UseCase


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def _load(name: str) -> dict[str, Any]:
    with (CONFIG_DIR / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_recommendations(
    use_case: UseCase,
    score: int,
    risk_level: str,
    dimension_scores: dict[str, int],
) -> dict[str, list[str]]:
    sector_risks = _load("sector_risks.yaml")
    board_questions = _load("board_questions.yaml")
    kpi_library = _load("kpi_library.yaml")

    main_risks = _main_risks(use_case, dimension_scores, sector_risks)
    required_integrations = _required_integrations(use_case)
    handover_design = _handover_design(use_case)
    compliance_checklist = _compliance_checklist(use_case)
    failure_modes = _failure_modes(use_case)
    pilot_design = _pilot_design(use_case, score, risk_level)
    questions = _board_questions(use_case, board_questions)
    kpis = _kpis(use_case, kpi_library)

    return {
        "main_risks": main_risks,
        "required_integrations": required_integrations,
        "handover_design": handover_design,
        "compliance_checklist": compliance_checklist,
        "failure_modes": failure_modes,
        "board_questions": questions,
        "pilot_design": pilot_design,
        "kpi_framework": kpis,
    }


def _main_risks(
    use_case: UseCase,
    dimension_scores: dict[str, int],
    sector_risks: dict[str, Any],
) -> list[str]:
    risks: list[str] = []

    if use_case.customer_authentication == "not_defined":
        risks.append("Customer authentication is undefined before account data is exposed.")
    if use_case.human_handover in {"none", "partial"}:
        risks.append("Escalation to human agents lacks explicit thresholds and routing.")
    if use_case.regulated_context:
        risks.append("The use case operates in a regulated context and needs auditable controls.")
    if len(use_case.languages) >= 3:
        risks.append("Multilingual quality needs benchmarking across every supported language.")
    if dimension_scores.get("integration", 100) < 65:
        risks.append("Core CRM, ticketing, or system-of-record integrations are not yet production-defined.")
    if use_case.fraud_risk == "high":
        risks.append("Fraud and social-engineering controls are not strong enough for high-risk calls.")

    sector_key = use_case.company_sector.lower().replace(" ", "_")
    risks.extend(sector_risks.get(sector_key, {}).get("risks", [])[:2])

    return _dedupe(risks)[:7]


def _required_integrations(use_case: UseCase) -> list[str]:
    integrations = ["Contact center platform", "Call recording and transcript store", "Knowledge base"]
    integrations.extend(use_case.data_access)

    if use_case.customer_authentication != "not_defined":
        integrations.append("Identity and authentication service")
    if use_case.human_handover != "none":
        integrations.append("Live agent routing and ticketing")
    if use_case.regulated_context:
        integrations.append("Audit logging and compliance review queue")
    if use_case.fraud_risk in {"medium", "high"}:
        integrations.append("Fraud monitoring or risk scoring")

    return _dedupe(integrations)


def _handover_design(use_case: UseCase) -> list[str]:
    items = [
        "Escalate when confidence drops below the approved threshold.",
        "Escalate when the customer asks for a human or shows repeated frustration.",
        "Pass transcript, detected intent, authentication state, and last completed step to the human agent.",
    ]

    if use_case.customer_impact in {"high", "critical"}:
        items.append("Escalate all complaints, disputes, vulnerable-customer cases, and irreversible account changes.")
    if use_case.regulated_context:
        items.append("Escalate regulated advice, consent disputes, and data-subject requests.")
    if use_case.fraud_risk == "high":
        items.append("Escalate suspicious identity, payment, or account-takeover signals.")

    return items


def _compliance_checklist(use_case: UseCase) -> list[str]:
    checklist = [
        "Disclose that the customer is speaking with an AI voice agent.",
        "Define call recording notice, consent capture, and retention period.",
        "Maintain searchable transcripts and decision logs for QA and audit.",
        "Define prohibited actions and mandatory escalation categories.",
    ]

    if use_case.regulated_context:
        checklist.extend(
            [
                "Map sector-specific obligations before external pilot launch.",
                "Review data processing, privacy notice, and cross-border data transfer posture.",
            ]
        )
    if use_case.customer_authentication == "not_defined":
        checklist.append("Define authentication before exposing account-specific information.")

    return checklist


def _failure_modes(use_case: UseCase) -> list[str]:
    modes = [
        "The agent gives plausible but wrong information from an outdated knowledge base.",
        "The customer interrupts, changes topic, or uses an accent the system handles poorly.",
        "Latency creates awkward pauses and customer frustration.",
        "The agent fails to recognize that the customer needs a human.",
        "Transcript or CRM sync fails, leaving the human agent without context.",
    ]

    if use_case.regulated_context:
        modes.append("The agent omits a required disclosure or gives regulated guidance.")
    if use_case.fraud_risk in {"medium", "high"}:
        modes.append("A fraudster uses the voice channel to bypass weak identity checks.")
    if len(use_case.languages) > 1:
        modes.append("Language switching degrades intent recognition or response quality.")

    return modes


def _pilot_design(use_case: UseCase, score: int, risk_level: str) -> list[str]:
    design = [
        "Start with a narrow use case and a limited customer segment.",
        "Run human review on a statistically meaningful sample of calls.",
        "Define rollback criteria before launch.",
        "Measure containment only after quality, compliance, and escalation performance are acceptable.",
    ]

    if score < 65 or risk_level in {"High", "Critical"}:
        design.insert(0, "Begin with an internal, shadow, or agent-assist pilot before autonomous customer handling.")
    if use_case.customer_impact in {"medium", "high", "critical"}:
        design.append("Exclude disputes, complaints, payments, account changes, and vulnerable-customer cases from the first pilot.")
    else:
        design.append("Allow low-risk FAQ and appointment flows with immediate human fallback.")

    return design


def _board_questions(use_case: UseCase, question_config: dict[str, Any]) -> list[str]:
    questions = list(question_config["general"])

    if use_case.regulated_context:
        questions.extend(question_config["regulated"])
    if use_case.autonomy_level in {"transactional", "decisioning"}:
        questions.extend(question_config["autonomy"])

    return _dedupe(questions)[:8]


def _kpis(use_case: UseCase, kpi_library: dict[str, Any]) -> list[str]:
    kpis = list(kpi_library["core"])
    kpis.extend(use_case.target_kpis)

    if use_case.regulated_context:
        kpis.extend(kpi_library["compliance"])
    if use_case.human_handover != "none":
        kpis.extend(kpi_library["handover"])
    if len(use_case.languages) > 1:
        kpis.extend(kpi_library["language"])

    return _dedupe(kpis)


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
