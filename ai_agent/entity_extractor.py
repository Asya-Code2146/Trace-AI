# ai_agent/entity_extractor.py

import json
import logging
from google import genai
from google.genai import types

from .config import load_config
from .models import GeneralEntities

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """
Analisis teks berikut yang diambil dari bukti digital (chat, screenshot, OCR).
Ekstrak informasi berikut. Jika TIDAK DITEMUKAN, wajib isi null. JANGAN MENGARANG.
Jika ada informasi spesifik seperti 'judul lowongan', 'harga barang', 'nama paket investasi', masukkan ke dalam field 'case_specific_data'.

Format JSON:
{{
  "company_name": null,
  "person_name": null,
  "phone_numbers": [],
  "whatsapp_numbers": [],
  "emails": [],
  "websites": [],
  "urls": [],
  "bank_accounts": [],
  "ewallets": [],
  "addresses": [],
  "transaction_amounts": [],
  "social_media_accounts": [],
  "case_specific_data": {{}}
}}

Teks:
{raw_text}
"""

def extract_entities(raw_text: str) -> GeneralEntities:
    if not raw_text or raw_text == "not_available":
        return GeneralEntities()
        
    config = load_config()
    client = genai.Client(api_key=config.api_key)
    prompt = EXTRACTION_PROMPT.format(raw_text=raw_text)
    
    try:
        response = client.models.generate_content(
            model=config.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        
        if response.text:
            data = json.loads(response.text)
            return GeneralEntities(**data)
    except Exception as e:
        logger.error(f"Gagal mengekstrak entitas: {e}")
        
    return GeneralEntities()