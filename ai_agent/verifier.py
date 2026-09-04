# File ini adalah stub (dummy). Nanti pas backendnya tuh ngehubungin ke API pengecekan sungguhan.

import logging

logger = logging.getLogger(__name__)

class ExternalVerifier:
    """
    Stub untuk pengecekan eksternal. 
    Tim backend bisa mengganti isi fungsi ini dengan API sungguhan.
    """
    
    def verify_urls(self, urls: list[str]) -> dict:
        """Cek apakah URL aman atau terdaftar mencurigakan."""
        results = {}
        for url in urls:
            # CONTOH: nanti diganti dengan request ke API VirusTotal/dll
            results[url] = {
                "status": "not_available",
                "message": "Verifikasi URL belum terhubung ke layanan eksternal."
            }
        return results

    def verify_contacts(self, phones: list[str], emails: list[str]) -> dict:
        """Cek nomor HP atau email di database penipuan."""
        results = {}
        for p in phones:
            results[p] = {"status": "not_available"}
        for e in emails:
            results[e] = {"status": "not_available"}
        return results

    def verify_company(self, company_name: str, website: str) -> dict:
        """Cek keabsahan nama perusahaan dan website."""
        if not company_name:
            return {"status": "no_data"}
            
        return {
            "status": "not_available",
            "message": f"Verifikasi perusahaan untuk '{company_name}' belum tersedia."
        }