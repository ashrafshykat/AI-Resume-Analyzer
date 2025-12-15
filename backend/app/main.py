from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

try:
    from .utils import (
        extract_text_from_pdf_bytes,
        extract_email,
        extract_phone,
        extract_name,
        extract_skills,
        extract_education,
        extract_experience_years,
        classify_experience_level,
    )
    from .model import load_model, model_exists
except ImportError:
    from app.utils import (
        extract_text_from_pdf_bytes,
        extract_email,
        extract_phone,
        extract_name,
        extract_skills,
        extract_education,
        extract_experience_years,
        classify_experience_level,
    )
    from app.model import load_model, model_exists

# Initialize FastAPI
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis and job classification",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model
class AnalysisResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience_years: float = 0.0
    experience_level: str = "Junior"
    classification: str = "Software Engineer"
    confidence: float = 0.0
    raw_text: Optional[str] = None

@app.on_event("startup")
async def startup():
    """Load model on startup"""
    if not model_exists():
        raise RuntimeError(
            "Model not found! Please run 'python train_model.py' first to train the classifier."
        )
    global vectorizer, classifier, label_encoder
    vectorizer, classifier, label_encoder = load_model()
    print("Model loaded successfully!")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Analyze a resume and extract information + classify job role.
    
    Accepts either:
    - file: PDF file upload
    - text: Raw text input
    """

    if file:
        if file.filename.lower().endswith('.pdf'):
            content = await file.read()
            resume_text = extract_text_from_pdf_bytes(content)
        else:
            raise HTTPException(status_code=400, detail="Only PDF files are supported for file upload")
    elif text:
        resume_text = text
    else:
        raise HTTPException(status_code=400, detail="Either 'file' or 'text' must be provided")
    
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from resume")
    
    # Extract information
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience_years = extract_experience_years(resume_text)
    experience_level = classify_experience_level(experience_years)
    
    # Classify job role
    X = vectorizer.transform([resume_text])
    classification = classifier.predict(X)[0]
    confidence = float(classifier.predict_proba(X)[0].max())
    category = label_encoder.inverse_transform([classification])[0]
    
    return AnalysisResponse(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        education=education,
        experience_years=experience_years,
        experience_level=experience_level,
        classification=category,
        confidence=confidence,
        raw_text=resume_text[:500],
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
