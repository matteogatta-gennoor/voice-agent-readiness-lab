from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml

from readiness.export import render_markdown
from readiness.models import UseCase
from readiness.scorer import score_use_case


ROOT = Path(__file__).resolve().parent
EXAMPLES_DIR = ROOT / "examples"


st.set_page_config(
    page_title="Voice Agent Readiness Lab",
    page_icon="VAL",
    layout="wide",
)


def load_example(filename: str) -> dict:
    with (EXAMPLES_DIR / filename).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def example_options() -> dict[str, str]:
    return {
        "Telecom billing support": "telecom_billing.yaml",
        "Hospital appointment confirmation": "hospital_appointment.yaml",
        "Banking card replacement": "banking_card_replacement.yaml",
        "Retail multilingual support": "retail_multilingual_support.yaml",
    }


def build_use_case(data: dict) -> UseCase:
    return UseCase(
        company_sector=data["company_sector"],
        use_case=data["use_case"],
        customer_impact=data["customer_impact"],
        languages=data["languages"],
        agent_type=data["agent_type"],
        autonomy_level=data["autonomy_level"],
        data_access=data["data_access"],
        customer_authentication=data["customer_authentication"],
        human_handover=data["human_handover"],
        regulated_context=data["regulated_context"],
        call_recording=data["call_recording"],
        consent_capture=data["consent_capture"],
        fraud_risk=data["fraud_risk"],
        qa_monitoring=data["qa_monitoring"],
        latency_target_ms=data["latency_target_ms"],
        target_kpis=data["target_kpis"],
    )


st.title("Voice Agent Readiness Lab")
st.caption("Assess whether an enterprise Voice AI use case is ready for production.")

with st.sidebar:
    st.header("Load Example")
    selected_example = st.selectbox("Example use case", list(example_options()))
    loaded = load_example(example_options()[selected_example])

    st.divider()
    st.markdown("The MVP is deterministic and YAML-driven. No LLM API key is required.")

with st.container():
    left, right = st.columns(2)

    with left:
        company_sector = st.selectbox(
            "Company sector",
            ["telecom", "healthcare", "banking", "retail", "insurance", "utilities", "other"],
            index=["telecom", "healthcare", "banking", "retail", "insurance", "utilities", "other"].index(
                loaded.get("company_sector", "telecom")
            )
            if loaded.get("company_sector", "telecom") in ["telecom", "healthcare", "banking", "retail", "insurance", "utilities", "other"]
            else 6,
        )
        use_case_text = st.text_area("Use case", value=loaded["use_case"], height=90)
        customer_impact = st.select_slider(
            "Customer impact",
            options=["low", "medium", "high", "critical"],
            value=loaded["customer_impact"],
        )
        languages = st.multiselect(
            "Languages",
            ["English", "Dutch", "French", "Spanish", "German", "Italian", "Arabic", "Portuguese"],
            default=loaded["languages"],
        )
        autonomy_level = st.selectbox(
            "Autonomy level",
            ["information_only", "guided_resolution", "transactional", "decisioning"],
            index=["information_only", "guided_resolution", "transactional", "decisioning"].index(loaded["autonomy_level"]),
        )
        data_access = st.multiselect(
            "Data access",
            ["CRM", "billing system", "ticketing system", "helpdesk", "knowledge base", "scheduling system", "core banking"],
            default=loaded["data_access"],
        )

    with right:
        customer_authentication = st.selectbox(
            "Customer authentication",
            ["not_defined", "basic", "strong"],
            index=["not_defined", "basic", "strong"].index(loaded["customer_authentication"]),
        )
        human_handover = st.selectbox(
            "Human handover",
            ["none", "partial", "clear"],
            index=["none", "partial", "clear"].index(loaded["human_handover"]),
        )
        regulated_context = st.toggle("Regulated context", value=loaded["regulated_context"])
        call_recording = st.toggle("Call recording", value=loaded["call_recording"])
        consent_capture = st.selectbox(
            "Consent capture",
            ["not_defined", "implicit", "explicit"],
            index=["not_defined", "implicit", "explicit"].index(loaded["consent_capture"]),
        )
        fraud_risk = st.selectbox(
            "Fraud risk",
            ["low", "medium", "high"],
            index=["low", "medium", "high"].index(loaded["fraud_risk"]),
        )
        qa_monitoring = st.selectbox(
            "QA monitoring",
            ["not_defined", "sampled", "continuous"],
            index=["not_defined", "sampled", "continuous"].index(loaded["qa_monitoring"]),
        )
        latency_target_ms = st.number_input(
            "Latency target in ms",
            min_value=300,
            max_value=5000,
            value=int(loaded["latency_target_ms"]),
            step=100,
        )
        target_kpis = st.multiselect(
            "Target KPIs",
            [
                "cost per call",
                "containment rate",
                "CSAT",
                "escalation rate",
                "first call resolution",
                "appointment confirmation rate",
                "fraud exception rate",
                "customer effort score",
            ],
            default=loaded["target_kpis"],
        )
data = {
    "company_sector": company_sector,
    "use_case": use_case_text,
    "customer_impact": customer_impact,
    "languages": languages or ["English"],
    "agent_type": "voice",
    "autonomy_level": autonomy_level,
    "data_access": data_access,
    "customer_authentication": customer_authentication,
    "human_handover": human_handover,
    "regulated_context": regulated_context,
    "call_recording": call_recording,
    "consent_capture": consent_capture,
    "fraud_risk": fraud_risk,
    "qa_monitoring": qa_monitoring,
    "latency_target_ms": int(latency_target_ms),
    "target_kpis": target_kpis,
}

use_case = build_use_case(data)
assessment = score_use_case(use_case)
report_markdown = render_markdown(use_case, assessment)

metric_left, metric_mid, metric_right = st.columns(3)
metric_left.metric("Readiness Score", f"{assessment.score} / 100")
metric_mid.metric("Risk Level", assessment.risk_level)
metric_right.metric("Recommendation", assessment.recommendation)

st.progress(assessment.score / 100)

tabs = st.tabs(
    [
        "Assessment",
        "Pilot",
        "Board Questions",
        "KPIs",
        "Markdown Export",
    ]
)

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Main Risks")
        for item in assessment.main_risks:
            st.write(f"- {item}")

        st.subheader("Dimension Scores")
        for name, score in assessment.dimension_scores.items():
            st.write(f"- **{name.replace('_', ' ').title()}**: {score} / 100")

    with col2:
        st.subheader("Required Integrations")
        for item in assessment.required_integrations:
            st.write(f"- {item}")

        st.subheader("Compliance and Consent")
        for item in assessment.compliance_checklist:
            st.write(f"- {item}")

with tabs[1]:
    st.subheader("Recommended Pilot Design")
    for item in assessment.pilot_design:
        st.write(f"- {item}")

    st.subheader("Human Handover Design")
    for item in assessment.handover_design:
        st.write(f"- {item}")

    st.subheader("Conversation Failure Modes")
    for item in assessment.failure_modes:
        st.write(f"- {item}")

with tabs[2]:
    for index, question in enumerate(assessment.board_questions, start=1):
        st.write(f"{index}. {question}")

with tabs[3]:
    for item in assessment.kpi_framework:
        st.write(f"- {item}")

with tabs[4]:
    st.download_button(
        "Download Markdown Report",
        report_markdown,
        file_name="voice_ai_readiness_assessment.md",
        mime="text/markdown",
    )
    st.code(report_markdown, language="markdown")
