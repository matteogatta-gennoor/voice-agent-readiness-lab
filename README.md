# Voice Agent Readiness Lab

A practical toolkit for assessing whether enterprise Voice AI agents are ready for production.

Voice AI is moving from impressive demos to real enterprise workflows. But production readiness requires more than a natural-sounding model. This toolkit helps executives, advisors, product teams, and board members assess whether a Voice AI agent is ready to operate safely, reliably, and commercially in front of real customers.

## What It Does

The app takes a structured Voice AI use case and produces:

- Production readiness score
- Risk classification
- Required integrations
- Human handover design
- Compliance and consent checklist
- Conversation failure modes
- Board-level questions
- Pilot design
- KPI framework
- Go / no-go recommendation

## Why This Exists

Voice AI demos beautifully. Production is a different animal: latency, escalation, compliance, language quality, CRM integration, customer frustration, hallucination, call recording, consent, authentication, fraud, and handover to humans.

This tool exposes the gap between a promising demo and a production-safe enterprise deployment.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish To GitHub

Create an empty GitHub repository named `voice-agent-readiness-lab`, then run:

```bash
git add .
git commit -m "Initial Voice Agent Readiness Lab MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/voice-agent-readiness-lab.git
git push -u origin main
```

## Example Use Cases

- Inbound customer care agent for billing questions in telecom
- Outbound appointment confirmation for hospitals
- Voice AI agent for banking card replacement
- Multilingual retail customer support agent

Sample YAML inputs are available in [`examples/`](examples/).

## How Scoring Works

The MVP is deterministic and config-driven. Scores are calculated from [`config/scoring_framework.yaml`](config/scoring_framework.yaml), then adjusted for sector, autonomy, compliance, authentication, integrations, and operational readiness.

This makes the logic inspectable and easy to adapt for your own risk appetite.

## Project Structure

```text
voice-agent-readiness-lab/
  app.py
  readiness/
    models.py
    scorer.py
    recommendations.py
    export.py
  config/
    scoring_framework.yaml
    sector_risks.yaml
    board_questions.yaml
    kpi_library.yaml
  examples/
    telecom_billing.yaml
    hospital_appointment.yaml
    banking_card_replacement.yaml
    retail_multilingual_support.yaml
  tests/
    test_scorer.py
```

## Current Scope

Version 1 focuses on board and pilot readiness, not vendor benchmarking. It does not claim that a specific Voice AI platform is safe. It helps teams ask the right questions before putting an agent in front of customers.

## Roadmap

- PDF export
- Optional LLM-assisted report drafting
- Industry-specific compliance modules
- Scenario testing and red-team checklists
- Batch comparison of multiple use cases
- Vendor-neutral integration readiness checklist

## License

MIT
