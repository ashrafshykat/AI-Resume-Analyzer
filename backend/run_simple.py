import sys
from pathlib import Path
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Suppress Fortran warnings
os.environ['FOR_DISABLE_INIT_SYNC_IO'] = '1'

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    
    from app.main import app
    import uvicorn
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
