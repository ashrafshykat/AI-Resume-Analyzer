@echo off
REM Quick start script for Resume Analyzer (Windows)

echo.
echo 🚀 Starting AI Resume Analyzer...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Start backend
echo 📍 Starting Backend Server...
cd backend
python train_model.py >nul 2>&1
start "Resume Analyzer Backend" python server.py
echo ✅ Backend started on port 8001

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Start frontend
echo 📍 Starting Frontend Server...
cd ..\frontend
call npm install --silent >nul 2>&1
start "Resume Analyzer Frontend" npm run dev

REM Wait for frontend
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo 🎉 Resume Analyzer is ready!
echo ============================================================
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔌 Backend API: http://127.0.0.1:8001
echo 🏥 Health Check: http://127.0.0.1:8001/health
echo.
echo Open http://localhost:3000 in your browser to start
echo.
pause
