# ai_agent/__init__.py

"""
General Digital Investigation AI
==================================
Cara penggunaan oleh backend FastAPI:

    from ai_agent import investigate, DigitalInvestigationAgent

    # Investigasi Awal
    result = investigate(raw_text="Dibutuhkan karyawan...")

    # Investigasi dengan Gambar
    agent = DigitalInvestigationAgent()
    result = agent.investigate(image_base64="base64_string...")
    
    # Investigasi Lanjutan
    result_lanjutan = agent.investigate_further(
        previous_report_dict=result, 
        additional_text="Ini link websitenya: http://..."
    )
"""

from .agent import DigitalInvestigationAgent, investigate
from .models import InvestigationReport, UnifiedContext, GeneralEntities, RiskLevel, Confidence, CaseType

__all__ = [
    "DigitalInvestigationAgent",
    "investigate",
    "InvestigationReport",
    "UnifiedContext",
    "GeneralEntities",
    "RiskLevel",
    "Confidence",
    "CaseType",
]