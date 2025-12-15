#!/usr/bin/env bash
# Quick start script for Resume Analyzer

echo "🚀 Starting AI Resume Analyzer..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

# Start backend in background
echo "📍 Starting Backend Server..."
cd backend
python train_model.py 2>/dev/null || echo "Model already trained"
python server.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 2

# Start frontend in background
echo "📍 Starting Frontend Server..."
cd ../frontend
npm install --silent 2>/dev/null
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

# Wait a bit for frontend to compile
sleep 5

echo ""
echo "="*60
echo "🎉 Resume Analyzer is ready!"
echo "="*60
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://127.0.0.1:8001"
echo "🏥 Health Check: http://127.0.0.1:8001/health"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Keep script running
wait
