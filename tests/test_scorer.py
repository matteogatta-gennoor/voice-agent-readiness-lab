from readiness.models import UseCase
from readiness.scorer import score_use_case


def test_low_risk_use_case_scores_higher_than_risky_use_case():
    low_risk = UseCase(
        company_sector="retail",
        use_case="Store hours and order status support",
        customer_impact="low",
        languages=["English"],
        agent_type="voice",
        autonomy_level="information_only",
        data_access=["CRM", "knowledge base", "ticketing system"],
        customer_authentication="basic",
        human_handover="clear",
        regulated_context=False,
        call_recording=True,
        consent_capture="explicit",
        fraud_risk="low",
        qa_monitoring="continuous",
        latency_target_ms=900,
        target_kpis=["containment rate"],
    )
    high_risk = UseCase(
        company_sector="banking",
        use_case="Approve disputed card transactions",
        customer_impact="high",
        languages=["English", "French", "Dutch"],
        agent_type="voice",
        autonomy_level="decisioning",
        data_access=["CRM"],
        customer_authentication="not_defined",
        human_handover="partial",
        regulated_context=True,
        call_recording=True,
        consent_capture="not_defined",
        fraud_risk="high",
        qa_monitoring="not_defined",
        latency_target_ms=1800,
        target_kpis=[],
    )

    assert score_use_case(low_risk).score > score_use_case(high_risk).score


def test_regulated_decisioning_is_critical():
    use_case = UseCase(
        company_sector="banking",
        use_case="Loan decisioning over voice",
        customer_impact="critical",
        languages=["English"],
        agent_type="voice",
        autonomy_level="decisioning",
        data_access=["CRM", "core banking"],
        customer_authentication="strong",
        human_handover="clear",
        regulated_context=True,
        call_recording=True,
        consent_capture="explicit",
        fraud_risk="high",
        qa_monitoring="continuous",
        latency_target_ms=1000,
        target_kpis=[],
    )

    assert score_use_case(use_case).risk_level == "Critical"
