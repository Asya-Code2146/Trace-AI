# ai_agent/models.py

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any

# ── Enum ──
class CaseType(str, Enum):
    JOB_SCAM = "job_scam"
    PHISHING = "phishing"
    WHATSAPP_SCAM = "whatsapp_scam"
    MARKETPLACE_SCAM = "marketplace_scam"
    INVESTMENT_SCAM = "investment_scam"
    IMPERSONATION = "impersonation"
    PAYMENT_SCAM = "payment_scam"
    SUSPICIOUS_EMAIL = "suspicious_email"
    UNKNOWN = "unknown"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# ── Models untuk Input & Proses ──
class GeneralEntities(BaseModel):
    """Entitas umum yang bisa muncul di berbagai kasus."""
    company_name: Optional[str] = None
    person_name: Optional[str] = None
    phone_numbers: list[str] = Field(default_factory=list)
    whatsapp_numbers: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    websites: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    bank_accounts: list[str] = Field(default_factory=list)
    ewallets: list[str] = Field(default_factory=list)
    addresses: list[str] = Field(default_factory=list)
    transaction_amounts: list[str] = Field(default_factory=list)
    social_media_accounts: list[str] = Field(default_factory=list)
    
    # Field spesifik tambahan (misal: job_title, salary) disimpan di sini
    # supaya model tetap fleksibel tanpa harus menambah kolom baru
    case_specific_data: dict[str, Any] = Field(default_factory=dict)

class UnifiedContext(BaseModel):
    """Konteks lengkap yang dikirim ke LLM."""
    case_type: str = "unknown"
    image_base64: Optional[str] = None
    image_mime_type: str = "image/jpeg"
    raw_text: str = "not_available"
    entities: GeneralEntities = Field(default_factory=GeneralEntities)
    quick_red_flags: list[str] = Field(default_factory=list)
    url_check_results: dict = Field(default_factory=dict)
    contact_check_results: dict = Field(default_factory=dict)
    company_verification: dict = Field(default_factory=dict)

# ── Models untuk Output ──
class RedFlagItem(BaseModel):
    type: str
    description: str
    severity: str 
    evidence_reference: str

class InvestigationReport(BaseModel):
    ml_prediction: Optional[str] = None          # <- TAMBAHKAN
    ml_probability: Optional[float] = None       # <- TAMBAHKAN
    ml_probabilities: dict[str, float] = Field(default_factory=dict) # <- TAMBAHKAN
    case_type: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    confidence_score: int = Field(ge=0, le=100)
    case_type: str
    evidence_summary: str
    entities_summary: dict[str, Any] = Field(default_factory=dict) # Ringkasan entitas penting
    red_flags: list[RedFlagItem]
    verified_information: list[str] = Field(default_factory=list)
    unverified_information: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    reasoning: str
    recommendation: list[str]
    confidence: Confidence