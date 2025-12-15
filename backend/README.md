# AI Resume Analyzer Backend

FastAPI backend for resume analysis and job classification.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m app.main
```

Server runs on `http://localhost:8000`

## API Endpoints

### POST /analyze
Analyze a resume and extract information.

**Input (multipart/form-data):**
- `file`: PDF file (optional)
- `text`: Raw text input (optional)

**Output:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8901",
  "skills": ["Python", "FastAPI", "Docker"],
  "education": ["BS in Computer Science"],
  "experience_years": 3.5,
  "experience_level": "Mid",
  "classification": "Software Engineer",
  "confidence": 0.89
}
```

### GET /health
Health check endpoint.

## Features

- PDF and text resume parsing
- Named entity recognition for name extraction
- Email and phone number extraction via regex
- Skill detection from comprehensive skill list
- Experience calculation from date ranges
- Job role classification using Logistic Regression
- Experience level estimation (Junior/Mid/Senior)
