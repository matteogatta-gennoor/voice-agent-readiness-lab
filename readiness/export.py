from __future__ import annotations

from readiness.models import Assessment, UseCase


def render_markdown(use_case: UseCase, assessment: Assessment) -> str:
    lines = [
        "# Voice AI Production Readiness Assessment",
        "",
        f"**Use Case:** {use_case.use_case}",
        f"**Sector:** {use_case.company_sector}",
        f"**Readiness Score:** {assessment.score} / 100",
        f"**Risk Level:** {assessment.risk_level}",
        f"**Recommendation:** {assessment.recommendation}",
        "",
        "## Dimension Scores",
        "",
    ]

    for name, score in assessment.dimension_scores.items():
        lines.append(f"- **{name.replace('_', ' ').title()}:** {score} / 100")

    sections = [
        ("Main Risks", assessment.main_risks),
        ("Required Integrations", assessment.required_integrations),
        ("Human Handover Design", assessment.handover_design),
        ("Compliance and Consent Checklist", assessment.compliance_checklist),
        ("Conversation Failure Modes", assessment.failure_modes),
        ("Recommended Pilot", assessment.pilot_design),
        ("KPI Framework", assessment.kpi_framework),
        ("Board-Level Questions", assessment.board_questions),
    ]

    for title, items in sections:
        lines.extend(["", f"## {title}", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(items, start=1))

    lines.extend(
        [
            "",
            "## Input Summary",
            "",
            f"- Agent type: {use_case.agent_type}",
            f"- Autonomy level: {use_case.autonomy_level}",
            f"- Customer impact: {use_case.customer_impact}",
            f"- Languages: {', '.join(use_case.languages)}",
            f"- Data access: {', '.join(use_case.data_access) if use_case.data_access else 'None specified'}",
            f"- Authentication: {use_case.customer_authentication}",
            f"- Human handover: {use_case.human_handover}",
            f"- Regulated context: {'Yes' if use_case.regulated_context else 'No'}",
            f"- Call recording: {'Yes' if use_case.call_recording else 'No'}",
            f"- Consent capture: {use_case.consent_capture}",
            f"- Fraud risk: {use_case.fraud_risk}",
            f"- QA monitoring: {use_case.qa_monitoring}",
            f"- Latency target: {use_case.latency_target_ms} ms",
        ]
    )

    return "\n".join(lines) + "\n"
