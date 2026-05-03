# Voice AI Production Readiness Assessment

**Use Case:** Inbound billing support agent for telecom customers
**Sector:** telecom
**Readiness Score:** 38 / 100
**Risk Level:** Critical
**Recommendation:** No-go for customer-facing deployment until core controls are defined.

## Dimension Scores

- **Product Scope:** 77 / 100
- **Integration:** 87 / 100
- **Compliance:** 72 / 100
- **Customer Experience:** 54 / 100
- **Operations:** 62 / 100
- **Governance:** 55 / 100
- **Language Quality:** 70 / 100

## Main Risks

1. Customer authentication is undefined before account data is exposed.
2. Escalation to human agents lacks explicit thresholds and routing.
3. The use case operates in a regulated context and needs auditable controls.
4. Multilingual quality needs benchmarking across every supported language.
5. Billing explanations can become disputes, refunds, or complaint handling.
6. Account access and SIM-related flows can create fraud and account-takeover exposure.

## Required Integrations

1. Contact center platform
2. Call recording and transcript store
3. Knowledge base
4. CRM
5. billing system
6. Live agent routing and ticketing
7. Audit logging and compliance review queue
8. Fraud monitoring or risk scoring

## Human Handover Design

1. Escalate when confidence drops below the approved threshold.
2. Escalate when the customer asks for a human or shows repeated frustration.
3. Pass transcript, detected intent, authentication state, and last completed step to the human agent.
4. Escalate regulated advice, consent disputes, and data-subject requests.

## Compliance and Consent Checklist

1. Disclose that the customer is speaking with an AI voice agent.
2. Define call recording notice, consent capture, and retention period.
3. Maintain searchable transcripts and decision logs for QA and audit.
4. Define prohibited actions and mandatory escalation categories.
5. Map sector-specific obligations before external pilot launch.
6. Review data processing, privacy notice, and cross-border data transfer posture.
7. Define authentication before exposing account-specific information.

## Conversation Failure Modes

1. The agent gives plausible but wrong information from an outdated knowledge base.
2. The customer interrupts, changes topic, or uses an accent the system handles poorly.
3. Latency creates awkward pauses and customer frustration.
4. The agent fails to recognize that the customer needs a human.
5. Transcript or CRM sync fails, leaving the human agent without context.
6. The agent omits a required disclosure or gives regulated guidance.
7. A fraudster uses the voice channel to bypass weak identity checks.
8. Language switching degrades intent recognition or response quality.

## Recommended Pilot

1. Begin with an internal, shadow, or agent-assist pilot before autonomous customer handling.
2. Start with a narrow use case and a limited customer segment.
3. Run human review on a statistically meaningful sample of calls.
4. Define rollback criteria before launch.
5. Measure containment only after quality, compliance, and escalation performance are acceptable.
6. Exclude disputes, complaints, payments, account changes, and vulnerable-customer cases from the first pilot.

## KPI Framework

1. Containment rate
2. First contact resolution
3. Customer satisfaction
4. Average latency
5. Task completion rate
6. Hallucination or incorrect-answer rate
7. cost per call
8. escalation rate
9. Consent capture rate
10. Required disclosure completion rate
11. Compliance exception rate
12. Audit sample pass rate
13. Correct escalation rate
14. Human takeover time
15. Context transfer completeness
16. Language-specific intent accuracy
17. Language-specific CSAT
18. Accent and dialect failure rate

## Board-Level Questions

1. What decisions is the voice agent allowed to make?
2. Who is accountable when the agent gives wrong information?
3. What is the fallback when confidence drops?
4. Are conversations logged, auditable, and explainable?
5. What customer experience threshold justifies scaling?
6. Which regulatory obligations apply to this call type?
7. What evidence will prove that consent, disclosure, and escalation rules were followed?
8. Who can suspend the agent if compliance exceptions rise?

## Input Summary

- Agent type: voice
- Autonomy level: guided_resolution
- Customer impact: medium
- Languages: Dutch, French, English
- Data access: CRM, billing system, knowledge base
- Authentication: not_defined
- Human handover: partial
- Regulated context: Yes
- Call recording: Yes
- Consent capture: implicit
- Fraud risk: medium
- QA monitoring: sampled
- Latency target: 1600 ms
