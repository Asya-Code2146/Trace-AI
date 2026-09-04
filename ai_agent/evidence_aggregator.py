# ai_agent/evidence_aggregator.py

import logging
from .models import UnifiedContext, GeneralEntities

logger = logging.getLogger(__name__)

def build_unified_context(
    raw_text: str,
    case_type: str = "unknown",
    image_base64: str = None, # type: ignore
    image_mime_type: str = "image/jpeg",
    entities: GeneralEntities = None, # type: ignore
    quick_red_flags: list[str] = None, # type: ignore
    url_checks: dict = None, # type: ignore
    contact_checks: dict = None, # type: ignore
    company_checks: dict = None, # type: ignore
    ml_result: dict = None       # <- TAMBAHKAN INI # type: ignore
) -> dict:
    if entities is None: entities = GeneralEntities()
    if quick_red_flags is None: quick_red_flags = []
    if url_checks is None: url_checks = {}
    if contact_checks is None: contact_checks = {}
    if company_checks is None: company_checks = {}
    if ml_result is None: ml_result = {}

    context = UnifiedContext(
        case_type=case_type,
        image_base64=image_base64,
        image_mime_type=image_mime_type,
        raw_text=raw_text,
        entities=entities,
        quick_red_flags=quick_red_flags,
        url_check_results=url_checks,
        contact_check_results=contact_checks,
        company_verification=company_checks,
        ml_result=ml_result  # <- TAMBAHKAN INI # type: ignore
    )
    
    return context.model_dump(exclude_none=True)