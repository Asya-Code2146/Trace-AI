# ai_agent/red_flag_detector.py

import re
import logging

logger = logging.getLogger(__name__)

PATTERNS = {
    "FEE_REQUEST": [
        r'biaya\s+(administrasi|pendaftaran|proses|hasil|admin)',
        r'transfer\s+(ke\s+rekening|sebelum|untuk|dp)',
        r'bayar\s+(dp|uang\s+muka|admin|first)'
    ],
    "UNREALISTIC_PROMISE": [
        r'gaji\s+([\d.]+)\s*(juta|jt)\s*(tanpa\s+syarat|hanya\s+modal\s+hp|dari\s+rumah|per\s+hari)',
        r'penghasilan\s+([\d.]+)\s*(juta|jt)\s*(per\s+hari|per\s+minggu|pasti)',
        r'profit\s+(tetap|pasti|garansi)\s+([\d.]+)',
        r'keuntungan\s+(\d{2,3})\s*%'
    ],
    "SENSITIVE_DATA_REQUEST": [
        r'kirim\s+(foto\s+ktp|scan\s+ktp|fc\s+ktp|foto\s+sim)',
        r'upload\s+(ktp|kk|ijazah|paspor)',
        r'pin\s+(anda|kamu|bapak|ibu)',
        r'otp\s+(anda|kamu)'
    ],
    "URGENCY": [
        r'segera|hari\s+ini|terakhir|kuota\s+terbatas|tinggal\s+(\d+)',
        r'jika\s+tidak|akan\s+di.*blokir|akan\s+di.*hapus'
    ],
    "PERSONAL_WHATSAPP": [
        r'hubungi\s+(wa|whatsapp)\s*:\s*\+?62\d{8,12}',
        r'wa\.me/\d+'
    ],
    "SUSPICIOUS_URL": [
        r'http[s]?://(?!www\.|(.*\.)?(go\.id|co\.id|ac\.id|sch\.id))\S+',
        r'bit\.ly/\S+|tinyurl\.com/\S+|t\.me/\S+'
    ]
}

def detect_quick_red_flags(text: str) -> list[str]:
    if not text or text == "not_available":
        return []
        
    flags = set()
    text_lower = text.lower()
    
    for flag_type, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                flags.add(flag_type)
                break 
                
    return list(flags)