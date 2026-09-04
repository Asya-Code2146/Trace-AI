import os
from dotenv import load_dotenv
import httpx
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, JSONResponse, FileResponse
from starlette.requests import Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import ai_agent

load_dotenv()

app = FastAPI(title="TRACE AI API")

# Konfigurasi Session Middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SECRET_KEY", "super-secret-key-trace-ai")
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"
GITHUB_PAGES_URL = "https://asya-code2146.github.io/Trace-AI/"


@app.get("/auth/login")
async def google_login(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(GITHUB_PAGES_URL)

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"prompt=select_account"
    )
    return RedirectResponse(url)


@app.get("/auth/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "Tidak ada kode autentikasi"}, status_code=400)

    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_res.json()

        if token_res.status_code != 200:
            return JSONResponse({"error": "Gagal mendapatkan token", "detail": token_data}, status_code=400)

        userinfo_res = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data.get('access_token')}"},
        )
        user_data = userinfo_res.json()

    request.session["user_id"] = user_data.get("sub", "unknown")
    request.session["user_name"] = user_data.get("name", "Unknown")
    request.session["user_email"] = user_data.get("email", "")
    request.session["user_pic"] = user_data.get("picture", "not_available")
    request.session["access_token"] = token_data.get("access_token")

    # Redirect kembali ke GitHub Pages setelah login sukses
    return RedirectResponse(GITHUB_PAGES_URL)


@app.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    # Redirect kembali ke GitHub Pages setelah logout
    return RedirectResponse(GITHUB_PAGES_URL)


@app.get("/api/auth/status")
async def auth_status(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"is_logged_in": False}
    return {
        "is_logged_in": True,
        "name": request.session.get("user_name"),
        "email": request.session.get("user_email"),
        "pic": request.session.get("user_pic", "not_available"),
    }


class InvestigateRequest(BaseModel):
    case_type: str
    raw_text: Optional[str] = None
    image_base64: Optional[str] = None


@app.post("/api/investigate")
def investigate_endpoint(req: InvestigateRequest):
    result = ai_agent.investigate(
        case_type=req.case_type,
        raw_text=req.raw_text,
        image_base64=req.image_base64,
    )
    return result


@app.get("/api/health")
def health():
    return {"status": "OK", "model": "TRACE AI (Hybrid ML+LLM)"}


# Mount static folder mengarah ke root project saat ini
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
def read_root():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)