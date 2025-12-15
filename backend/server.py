#!/usr/bin/env python3
"""
Backend API server for Resume Analyzer
Handles API requests without triggering Fortran runtime issues
"""
import sys
import os
from pathlib import Path

# Suppress warnings and Fortran issues
os.environ['FOR_DISABLE_INIT_SYNC_IO'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import warnings
warnings.filterwarnings("ignore")

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    try:
        # Import after environment setup
        from app.main import app
        import uvicorn
        
        print("🚀 Starting Resume Analyzer Backend...")
        print("📍 API running on http://127.0.0.1:8001")
        print("🏥 Health check: http://127.0.0.1:8001/health")
        print("📊 Analyze endpoint: POST http://127.0.0.1:8001/analyze")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Run server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8001,
            log_level="info",
            access_log=True,
            use_colors=True
        )
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
