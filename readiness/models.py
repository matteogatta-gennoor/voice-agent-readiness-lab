from dataclasses import dataclass, field


@dataclass
class UseCase:
    company_sector: str
    use_case: str
    customer_impact: str
    languages: list[str]
    agent_type: str
    autonomy_level: str
    data_access: list[str]
    customer_authentication: str
    human_handover: str
    regulated_context: bool
    call_recording: bool
    consent_capture: str
    fraud_risk: str
    qa_monitoring: str
    latency_target_ms: int
    target_kpis: list[str] = field(default_factory=list)


@dataclass
class Assessment:
    score: int
    risk_level: str
    recommendation: str
    dimension_scores: dict[str, int]
    main_risks: list[str]
    required_integrations: list[str]
    handover_design: list[str]
    compliance_checklist: list[str]
    failure_modes: list[str]
    board_questions: list[str]
    pilot_design: list[str]
    kpi_framework: list[str]
