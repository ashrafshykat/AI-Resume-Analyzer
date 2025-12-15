# AI Resume Analyzer - Complete System

A full-stack AI-powered resume analysis system that extracts information, classifies job roles, and estimates experience levels.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Frontend Usage](#frontend-usage)
- [Features](#features)
- [File Structure](#file-structure)

## 🎯 Project Overview

This system provides:
- **Resume Parsing**: Extract key information from PDF or text resumes
- **Information Extraction**: Name, email, phone, skills, education
- **Experience Calculation**: Automatic calculation of years from date ranges
- **Job Classification**: ML-based classification into 6 job categories
- **Experience Level**: Auto-estimate Junior/Mid/Senior levels
- **Web Interface**: Simple React/Next.js UI for easy usage

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        React/Next.js Frontend           │
│          (localhost:3000)               │
│       - File upload (PDF)               │
│       - Text paste input                │
│       - Results visualization           │
└────────────────┬────────────────────────┘
                 │
           HTTP Requests
                 │
                 ▼
┌─────────────────────────────────────────┐
│      FastAPI Backend Server             │
│      (localhost:8001)                   │
│  - Resume parsing                       │
│  - Text extraction from PDF             │
│  - ML model inference                   │
│  - Data extraction (regex + NLP)        │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴───────┐
        ▼                 ▼
    ML Model       Extraction Utils
 (classifier)      (utils.py)
  TF-IDF           - Email/Phone regex
  Logistic         - Skill detection
  Regression       - Date parsing
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ (recommended: 3.10+)
- Node.js 16+ & npm
- Git

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Train the ML model (one-time)
python train_model.py

# Start the server
python server.py
```

Backend will be available at: `http://127.0.0.1:8001`

### Frontend Setup

```bash
cd frontend

# Install npm dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 📡 API Documentation

### Health Check
```http
GET /health
```
**Response:**
```json
{"status": "healthy"}
```

### Analyze Resume
```http
POST /analyze
Content-Type: multipart/form-data

Parameters:
- file: PDF file (optional)
- text: Raw text (optional)
```

**Request Examples:**

**PDF Upload:**
```bash
curl -X POST http://127.0.0.1:8001/analyze \
  -F "file=@resume.pdf"
```

**Text Input:**
```bash
curl -X POST http://127.0.0.1:8001/analyze \
  -F "text=John Doe, john@email.com, ..."
```

**Response:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8901",
  "skills": ["Python", "FastAPI", "Docker", "Kubernetes"],
  "education": ["BS in Computer Science"],
  "experience_years": 4.5,
  "experience_level": "Mid",
  "classification": "FullStack Developer",
  "confidence": 0.87,
  "raw_text": "First 500 characters of resume..."
}
```

## 🖥️ Frontend Usage

1. Open `http://localhost:3000` in your browser
2. Choose upload mode:
   - **PDF Upload**: Drag & drop or click to select PDF file
   - **Paste Text**: Paste resume text directly
3. Click **"Analyze Resume"** button
4. View results:
   - Extracted candidate information
   - Detected skills with badges
   - Job role classification with confidence score
   - Experience level and years
   - Education entries

## ✨ Features

### Resume Parsing
- **PDF Extraction**: Uses PyPDF2 for text extraction
- **Text Cleaning**: Handles various formatting
- **Robust Parsing**: Works with different resume formats

### Information Extraction
- **Name**: Using pattern matching (first few lines)
- **Email**: Regex-based extraction
- **Phone**: International format support
- **Skills**: Comprehensive skill list matching
- **Education**: Keyword-based detection
- **Experience**: Date range parsing and calculation

### ML Classification
- **Algorithm**: Logistic Regression with TF-IDF vectorization
- **Training Data**: 12 hand-crafted resume samples
- **Classes**: 
  - Software Engineer
  - AI/ML Engineer
  - Data Scientist
  - Web Developer
  - DevOps/Cloud Engineer
  - FullStack Developer

### Experience Level
- **Junior**: 0–2 years
- **Mid**: 2–5 years
- **Senior**: 5+ years

## 📁 File Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── utils.py             # Parsing & extraction utilities
│   │   └── model.py             # Model loading/saving
│   ├── models/
│   │   ├── vectorizer.joblib    # TF-IDF vectorizer
│   │   └── classifier.joblib    # Trained classifier
│   ├── train_model.py           # Model training script
│   ├── server.py                # Server runner
│   ├── run.py                   # Alternative runner
│   ├── requirements.txt         # Python dependencies
│   └── start.bat               # Windows batch starter
│
├── frontend/
│   ├── pages/
│   │   ├── index.jsx           # Main page
│   │   └── _app.jsx            # App wrapper
│   ├── components/
│   │   ├── ResumeUploader.jsx  # Main component
│   │   └── ResumeUploader.module.css
│   ├── styles/
│   │   └── globals.css
│   ├── public/
│   ├── next.config.js
│   ├── package.json
│   └── .gitignore
│
└── README.md (this file)
```
