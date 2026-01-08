# app.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import joblib, os

DATABASE_URL = "sqlite:///./sms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()   

class SMSDB(Base):
    __tablename__ = "sms"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

class SMSCreate(BaseModel):
    text: str

class SMSOut(SMSCreate):
    id: int
    category: str
    timestamp: datetime
    class Config:
        orm_mode = True

app = FastAPI(title="SMS Sorter Backend")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Try to load trained model pipeline if exists (sms_pipeline.pkl)
model = None
if os.path.exists("sms_pipeline.pkl"):
    model = joblib.load("sms_pipeline.pkl")
    print("Loaded ML pipeline: sms_pipeline.pkl")
else:
    print("No model found — endpoint will use simple heuristics.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/sms", response_model=SMSOut)
def create_sms(sms: SMSCreate, db=Depends(get_db)):
    text = sms.text
    if model:
        category = model.predict([text])[0]
    else:
        # very simple fallback rules for demo
        low = text.lower()
        if any(w in low for w in ["offer","sale","buy","discount"]):
            category = "promotions"
        elif any(w in low for w in ["otp","transaction","credited","debited","bank","upi","balance"]):
            category = "transactions"
        elif any(w in low for w in ["win","prize","free","click","congrat"]):
            category = "spam"
        else:
            category = "personal"
    db_sms = SMSDB(text=text, category=category)
    db.add(db_sms)
    db.commit()
    db.refresh(db_sms)
    return db_sms

@app.get("/sms", response_model=List[SMSOut])
def list_sms(category: Optional[str] = None, skip: int = 0, limit:int = 100, db=Depends(get_db)):
    q = db.query(SMSDB)
    if category:
        q = q.filter(SMSDB.category == category)
    return q.offset(skip).limit(limit).all()

@app.get("/sms/{sms_id}", response_model=SMSOut)
def get_sms(sms_id: int, db=Depends(get_db)):
    s = db.query(SMSDB).filter(SMSDB.id == sms_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    return s

@app.delete("/sms/{sms_id}", response_model=SMSOut)
def delete_sms(sms_id: int, db=Depends(get_db)):
    s = db.query(SMSDB).filter(SMSDB.id == sms_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(s)
    db.commit()
    return s
