from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routers import auth, planners, pages

settings=get_settings()
app=FastAPI(title=settings.app_name,version="1.0.0",description="Budget-aware AI recommendation assistant")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=str(Path(__file__).resolve().parent/"static")),name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)

@app.on_event("startup")
def startup(): init_db()

@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name}

@app.get("/startup")
def startup_status(): return {"status":"initialized","ai_model":settings.gemini_model,"gemini_configured":bool(settings.gemini_api_key)}
