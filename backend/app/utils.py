import re
from io import BytesIO
from typing import List, Optional
from datetime import datetime

from dateutil import parser as dateparser
from PyPDF2 import PdfReader
import spacy

nlp = spacy.load("en_core_web_sm")

# my known skills list
SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust", "ruby", "php",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
    "docker", "kubernetes", "jenkins", "gitlab", "github", "aws", "azure", "gcp",
    "react", "vue", "angular", "next.js", "svelte", "ember",
    "node", "express", "django", "flask", "spring", "fastapi", "laravel",
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "git", "linux", "bash", "shell", "html", "css", "sass", "webpack",
    "graphql", "rest", "microservices", "oop", "functional", "agile", "scrum",
] 

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extract text from PDF file bytes"""
    try:
        f = BytesIO(file_bytes)
        reader = PdfReader(f)
        texts = []
        for p in reader.pages:
            texts.append(p.extract_text() or "")
        return "\n".join(texts)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def extract_email(text: str) -> Optional[str]:
    """Extract email using regex"""
    m = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return m.group(0) if m else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number using regex"""
    m = re.search(r"(\+?\d[\d\s\-\(\)\.]{6,}\d)", text)
    return m.group(0).strip() if m else None

def extract_name(text: str) -> Optional[str]:
    """Extract candidate name using spaCy NER"""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) <= 4:
            return ent.text.strip()
    # fallback: first line heuristic
    first_line = text.strip().split('\n')[0]
    if 2 <= len(first_line.split()) <= 4:
        return first_line.strip()
    return None

def extract_skills(text: str) -> List[str]:
    """Extract skills using spaCy + keyword matching"""
    doc = nlp(text.lower())
    found = set()
    for token in doc:
        if token.text in SKILLS:
            found.add(token.text.upper())
    return list(found)

def extract_education(text: str) -> List[str]:
    """Extract education using spaCy + keyword matching"""
    edu_keywords = [
        "bachelor", "master", "phd", "associate", "bs", "ms", "ba", "ma", 
        "b.sc", "m.sc", "b.a", "m.a", "degree", "university", "college"
    ]
    doc = nlp(text.lower())
    found = []
    for sent in doc.sents:
        for kw in edu_keywords:
            if kw in sent.text:
                found.append(sent.text.strip())
                break
    return found[:5]

def parse_date(s: str) -> Optional[datetime]:
    try:
        return dateparser.parse(s, fuzzy=True)
    except Exception:
        return None

def extract_experience_years(text: str) -> float:
    """Calculate total experience using date ranges or mentions"""
    ranges = re.findall(r"([A-Za-z0-9 ,./-]{4,})\s[-–—]\s([A-Za-z0-9 ,./-]{4,})", text)
    periods = []
    for a, b in ranges:
        da = parse_date(a)
        db = parse_date(b)
        if da and db:
            periods.append((da, db))
        elif da and b.lower().strip() in ("present", "current", "today"):
            periods.append((da, datetime.now()))
    
    if not periods:
        # fallback to "X years experience"
        m = re.search(r"(\d+(?:\.\d+)?)\s+years", text.lower())
        if m:
            return float(m.group(1))
    
    total_months = 0
    for da, db in periods:
        months = (db.year - da.year) * 12 + (db.month - da.month)
        total_months += max(0, months)
    return round(total_months / 12.0, 1)

def classify_experience_level(years: float) -> str:
    """Classify experience level"""
    if years < 2:
        return "Junior"
    elif years < 5:
        return "Mid"
    else:
        return "Senior"
