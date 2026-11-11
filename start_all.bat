@echo off
title AgroVision AI - Full System Launcher
echo ====================================================================
echo Launching AgroVision AI: LeafVision-DINO + AgERA5 + Spring AI
echo ====================================================================

start "LeafVision ML Service" cmd /k "%~dp0start_ml_service.bat"
timeout /t 3 /nobreak >nul
start "Spring Boot Backend" cmd /k "%~dp0start_backend.bat"

echo.
echo Both servers are starting up:
echo 1. ML Vision Transformer API: http://127.0.0.1:8000/docs
echo 2. Web Application & Dashboard: http://localhost:8080
echo ====================================================================
pause
