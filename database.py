import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from sqlalchemy.ext.serializer import Serializer, Deserializer
import json

# Setup Database Lokal (SQLite)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trace_ai.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- MODELS ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    google_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    profile_pic = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class InvestigationHistory(Base):
    __tablename__ "investigation_history" # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_type = Column(String(50), nullable=False)
    raw_text = Column(Text, nullable=True)
    result_json = Column(Text, nullable=False)  # Disimpan sebagai string JSON
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Inisialisasi Database (Buat tabel otomatis jika belum ada)
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()