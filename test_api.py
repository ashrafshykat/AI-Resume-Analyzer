#!/usr/bin/env python3
"""
Test script for Resume Analyzer API
Tests the backend endpoint with sample resumes
"""

import requests
import json
import time
from pathlib import Path

# API endpoint
API_URL = "http://127.0.0.1:8001"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("🏥 HEALTH CHECK")
    print("="*60)
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_resume(resume_file):
    """Test analyze endpoint with a resume file"""
    print("\n" + "="*60)
    print(f"📄 TESTING: {resume_file}")
    print("="*60)
    
    file_path = Path(__file__).parent / resume_file
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        resume_text = f.read()
    
    print(f"Resume size: {len(resume_text)} characters")
    print(f"Preview: {resume_text[:100]}...")
    
    try:
        print("\nAnalyzing resume...")
        response = requests.post(
            f"{API_URL}/analyze",
            data={'text': resume_text},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nAnalysis Complete!\n")
            
            # Candidate Info
            print("CANDIDATE INFORMATION")
            print(f"  Name: {result.get('name', 'N/A')}")
            print(f"  Email: {result.get('email', 'N/A')}")
            print(f"  Phone: {result.get('phone', 'N/A')}")
            
            # Experience
            print("\nEXPERIENCE")
            print(f"  Years: {result.get('experience_years', 0)} years")
            print(f"  Level: {result.get('experience_level', 'N/A')}")
            
            # Classification
            print("\nJOB CLASSIFICATION")
            print(f"  Role: {result.get('classification', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 0):.1%}")
            
            # Skills
            skills = result.get('skills', [])
            if skills:
                print("\nSKILLS DETECTED")
                for skill in skills:
                    print(f"  • {skill}")
            
            # Education
            education = result.get('education', [])
            if education:
                print("\nEDUCATION")
                for edu in education:
                    print(f"  • {edu}")
            
            print("\n" + "="*60)
            print("Full Response (JSON):")
            print(json.dumps(result, indent=2))
            
        else:
            print(f"Error: {response.status_code}")
            print(f"Message: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to API at {API_URL}")
        print("   Make sure backend is running: python server.py")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "🚀 "*15)
    print("RESUME ANALYZER API TEST SUITE")
    print("🚀 "*15)
    
    # Check API connectivity
    if not test_health():
        print("\nAPI is not reachable. Please start the backend:")
        print("   cd backend && python server.py")
        return
    
    # Test with sample resumes
    samples = [
        "sample_resume.txt",
        "sample_resume_data_scientist.txt",
        "sample_resume_devops.txt",
        "sample_resume_web_developer.txt",
    ]
    
    for sample in samples:
        test_resume(sample)
        time.sleep(1)  # Brief delay between requests
    
    print("\n" + ""*15)
    print("ALL TESTS COMPLETED")
    print(" "*15 + "\n")

if __name__ == "__main__":
    main()
