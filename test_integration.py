"""
Integration Test - Frontend + Backend
Tests the complete resume analyzer system
"""

import subprocess
import time
import requests
import json
import sys
from pathlib import Path

def wait_for_service(url, timeout=30):
    """Wait for a service to be ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def test_complete_system():
    """Test the complete system integration"""
    
    print("\n" + "="*70)
    print("🧪 RESUME ANALYZER - COMPLETE SYSTEM TEST")
    print("="*70 + "\n")
    
    # Check backend
    print("1️⃣  Testing Backend API...")
    print("   Checking http://127.0.0.1:8001/health")
    
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print("   ⚠️  Backend responded but unexpected status")
    except:
        print("   ❌ Backend not accessible")
        print("\n   Start backend with: cd backend && python server.py")
        return False
    
    # Check frontend
    print("\n2️⃣  Testing Frontend Server...")
    print("   Checking http://localhost:3000")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend is running")
        else:
            print("   ⚠️  Frontend responded but unexpected status")
    except:
        print("   ❌ Frontend not accessible")
        print("\n   Start frontend with: cd frontend && npm run dev")
        return False
    
    # Test API with sample resume
    print("\n3️⃣  Testing Resume Analysis API...")
    
    sample_text = """
    JOHN DOE
    john@email.com
    (555) 123-4567
    
    Full Stack Developer with 3 years experience.
    Skills: Python, Django, React, Docker, AWS
    
    Experience:
    January 2021 - Present: Senior Dev at TechCorp
    June 2019 - December 2020: Developer at StartupXYZ
    """
    
    try:
        response = requests.post(
            "http://127.0.0.1:8001/analyze",
            data={'text': sample_text},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ API returned results")
            print(f"\n   Extracted Data:")
            print(f"     - Name: {result.get('name', 'N/A')}")
            print(f"     - Email: {result.get('email', 'N/A')}")
            print(f"     - Skills: {', '.join(result.get('skills', [])[:3])}")
            print(f"     - Experience: {result.get('experience_years', 0)} years ({result.get('experience_level', 'N/A')})")
            print(f"     - Classification: {result.get('classification', 'N/A')} ({result.get('confidence', 0):.1%})")
        else:
            print(f"   ❌ API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API request failed: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - System is working correctly!")
    print("="*70)
    print("\n🎉 You can now use the Resume Analyzer at http://localhost:3000")
    print("\n📝 Tips:")
    print("   - Upload a PDF resume or paste text")
    print("   - Click 'Analyze Resume' to get results")
    print("   - Try sample resumes in d:\\Octopi\\sample_resume*.txt")
    print("   - Run test_api.py for more detailed testing")
    print()
    
    return True

if __name__ == "__main__":
    success = test_complete_system()
    sys.exit(0 if success else 1)
