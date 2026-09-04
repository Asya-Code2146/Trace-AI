import logging
from typing import Union
import sys
import os

# Tambahkan root folder ke path agar bisa import 'ml' saat dijalankan standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .models import InvestigationReport, UnifiedContext, GeneralEntities
from .analyzer import LLMAnalyzer
from .entity_extractor import extract_entities
from .red_flag_detector import detect_quick_red_flags
from .evidence_aggregator import build_unified_context
from .verifier import ExternalVerifier
from .risk_assessor import validate_risk_assessment
from .report_generator import generate_final_output
from .config import GeminiConfig

# Import ML Predictor
from ml.predict import predict_ml

logger = logging.getLogger(__name__)

class DigitalInvestigationAgent:
    def __init__(self, config: GeminiConfig | None = None):
        self.analyzer = LLMAnalyzer(config)
        self.verifier = ExternalVerifier()

    def investigate(
        self, 
        case_type: str,                  
        image_base64: str | None = None, 
        image_mime_type: str = "image/jpeg",
        raw_text: str | None = None
    ) -> dict:
        """Alur investigasi Hybrid (ML + LLM)."""
        logger.info("=" * 60)
        logger.info("TRACE AI (HYBRID ML+LLM) — START")
        logger.info("TRACE AI (HYBRID ML+LLM) — INVESTIGATE FURTHER STARTED")
        logger.info(f"Case Type selected by user: {case_type}")
        logger.info("=" * 60)

        ml_result = {"ml_prediction": "unknown", "ml_probability": 0.0, "ml_status": "skipped"}
        
        # 1. Ekstraksi Entitas
        entities = GeneralEntities()
        if raw_text and raw_text != "not_available":
            logger.info("Mengekstrak entitas...")
            entities = extract_entities(raw_text)

        # 2. MACHINE LEARNING PREDICTION (Hanya jika ada teks)
        if raw_text and raw_text != "not_available":
            logger.info("Menjalankan prediksi Machine Learning...")
            ml_result = predict_ml(raw_text, case_type)
            logger.info(f"ML Result: {ml_result.get('ml_prediction')} ({ml_result.get('ml_probability')})")

        # 3. Deteksi Cepat
        quick_flags = detect_quick_red_flags(raw_text or "")
        
        # 4. Verifikasi Eksternal
        url_checks = self.verifier.verify_urls(entities.urls + entities.websites)
        contact_checks = self.verifier.verify_contacts(entities.phone_numbers + entities.whatsapp_numbers, entities.emails)
        company_checks = self.verifier.verify_company(entities.company_name, entities.websites[0] if entities.websites else None) # type: ignore

        # 5. Agregasi Evidence (Termasuk hasil ML)
        unified_ctx_dict = build_unified_context(
            raw_text=raw_text or "not_available",
            image_base64=image_base64, # type: ignore
            image_mime_type=image_mime_type,
            case_type=case_type,
            entities=entities,
            quick_red_flags=quick_flags,
            url_checks=url_checks,
            contact_checks=contact_checks,
            company_checks=company_checks,
            ml_result=ml_result  
        )

        # 6. LLM Deep Analysis & Reasoning
        report = self.analyzer.analyze(unified_ctx_dict)

        # 7. Override ML fields ke report (karena LLM terkadang tidak exact)
        report.ml_prediction = ml_result.get("ml_prediction")
        report.ml_probability = ml_result.get("ml_probability")

        # 8. Risk Validation
        report = validate_risk_assessment(report, unified_ctx_dict)

        final_output = generate_final_output(report)
        logger.info(f"Investigation COMPLETE — ML: {report.ml_prediction}, Risk: {report.risk_score}")
        logger.info("=" * 60)

        return final_output

# ── Convenience function ──
_default_agent: DigitalInvestigationAgent | None = None

def investigate(case_type: str, image_base64: str | None = None, raw_text: str | None = None) -> dict:
    global _default_agent
    if _default_agent is None:
        _default_agent = DigitalInvestigationAgent()
    return _default_agent.investigate(case_type=case_type, image_base64=image_base64, raw_text=raw_text)