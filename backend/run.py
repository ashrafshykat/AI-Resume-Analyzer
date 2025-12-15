import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from app.main import app
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
