import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# WAJIB pilih case_type sekarang!
from ai_agent import investigate

text_phishing = """
PERINGATAN AKUN BCA ANDA AKAN DI BLOKIR!
Jika bukan Anda, segera verifikasi keamanan akun melalui link: 
http://bca-keamanan-verifikasi-update.com/aktifkan
"""

print("Menjalankan HYBRID INVESTIGATION (ML + LLM)...")
result = investigate(
    case_type="phishing",       # <- USER MEMILIH KATEGORI
    raw_text=text_phishing
)

print(json.dumps(result, ensure_ascii=False, indent=2))