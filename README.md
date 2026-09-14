<div align="center">

# 🔍 TRACE AI
### Platform Investigasi & Analisis Kasus Berbasis AI (Hybrid ML + LLM)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📖 Tentang Proyek
**TRACE AI** adalah aplikasi web cerdas yang dirancang untuk membantu proses investigasi dan analisis kasus secara mendalam. Menggabungkan pendekatan Machine Learning konvensional dengan kemampuan *Large Language Model* (LLM), aplikasi ini mampu memproses teks mentah maupun lampiran gambar berbasis Base64 secara instan dan akurat.

---

## ✨ Fitur Utama
* 🔐 **Google OAuth Authentication**: Sistem masuk yang aman menggunakan akun Google.
* 🤖 **AI-Powered Investigation**: Agen AI cerdas untuk menganalisis berbagai jenis kasus investigasi.
* ⚡ **High-Performance API**: Dibangun menggunakan FastAPI dengan dukungan CORS dan Session Middleware.
* 🌐 **Frontend Integrations**: Terhubung mulus dengan antarmuka web modern di GitHub Pages.

---

## 📂 Struktur Repositori
```text
TRACE-AI/
├── api/                  # Konfigurasi serverless untuk deployment
├── project/              # Berisi file inti backend & modul AI
│   ├── main.py           # Entry point utama FastAPI
│   └── ai_agent.py       # Logika utama agen kecerdasan buatan
├── index.html            # Halaman antarmuka utama frontend
├── app.js                # Skrip interaksi JavaScript
├── style.css             # Desain dan tata letak antarmuka
└── requirements.txt      # Daftar dependensi pustaka Python
