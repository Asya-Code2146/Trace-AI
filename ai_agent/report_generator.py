# ai_agent/report_generator.py

import json
import logging
from datetime import datetime, timezone
from .models import InvestigationReport

logger = logging.getLogger(__name__)

def generate_final_output(report: InvestigationReport) -> dict:
    output = {
        "investigation_report": {
            "case_type": report.case_type,
            "risk_score": report.risk_score,
            "risk_level": report.risk_level.value,
            "confidence_score": report.confidence_score,
            "ml_prediction": report.ml_prediction,           # <- BARU
            "ml_probability": report.ml_probability,         # <- BARU
            "evidence_summary": report.evidence_summary,
            "entities_summary": report.entities_summary,
            "red_flags": [
                {"type": rf.type, "description": rf.description, "severity": rf.severity, "evidence_reference": rf.evidence_reference}
                for rf in report.red_flags
            ],
            "verified_information": report.verified_information,
            "unverified_information": report.unverified_information,
            "missing_evidence": report.missing_evidence,
            "reasoning": report.reasoning,
            "recommendation": report.recommendation,
            "confidence": report.confidence.value,
        },
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "red_flags_count": len(report.red_flags),
            "high_severity_flags": sum(1 for rf in report.red_flags if rf.severity == "high")
        }
    }
    return output