# ai_agent/risk_assessor.py

import logging
from .models import InvestigationReport, UnifiedContext, RiskLevel, Confidence

logger = logging.getLogger(__name__)

def validate_risk_assessment(report: InvestigationReport, context: UnifiedContext | dict) -> InvestigationReport:
    if isinstance(context, UnifiedContext):
        ctx = context
    else:
        ctx = UnifiedContext(**context)

    # 1. Validasi Risk Level
    expected_level = RiskLevel.HIGH if report.risk_score >= 70 else RiskLevel.MEDIUM if report.risk_score >= 40 else RiskLevel.LOW
    if report.risk_level != expected_level:
        report.risk_level = expected_level

    # 2. Validasi Confidence berdasarkan evidence
    has_image = ctx.image_base64 is not None
    has_text = ctx.raw_text not in [None, "", "not_available"]
    
    if not has_image and not has_text:
        if report.confidence_score > 20: report.confidence_score = 10
        if report.confidence == Confidence.HIGH: report.confidence = Confidence.LOW
            
    # 3. Jika red_flags kosong tapi skor tinggi
    if not report.red_flags and report.risk_score >= 60:
        report.risk_score = 45
        report.risk_level = RiskLevel.MEDIUM

    return report