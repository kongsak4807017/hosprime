@echo off
title HosPrime Launcher
cls
echo =====================================================================
echo    👑 HosPrime: Health Organization Operating System Launcher 👑
echo                  (Milestone 1: Knowledge Oracle MVP)
echo =====================================================================
echo.

:: 1. ตรวจสอบสภาพแวดล้อม Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

:: 2. ตรวจสอบสภาพแวดล้อม Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js and add to PATH.
    pause
    exit /b 1
)

echo [1/3] Starting Backend FastAPI Server in new window...
start "HosPrime Backend" cmd /k "cd backend && set PYTHONPATH=..&& echo Installing dependencies... && pip install -r requirements.txt && echo. && echo Bootstrapping demo dataset... && python app/db/bootstrap.py && echo. && echo Starting FastAPI Server on port 8000... && python -m uvicorn app.main:app --reload --port 8000"

echo [2/3] Starting Frontend React Server in new window...
start "HosPrime Frontend" cmd /k "cd frontend && echo Starting Vite development server on port 5173... && npm run dev"

echo.
echo =====================================================================
echo    🎉 HosPrime System is initializing!
echo.
echo    - Backend API Docs:  http://localhost:8000/docs
echo    - Frontend Web App:  http://localhost:5173
echo.
echo    * กรุณารอระบบหลังบ้านเตรียมฐานข้อมูลสักครู่ก่อนเริ่มถามคำถามเดโม *
echo =====================================================================
echo.
pause
