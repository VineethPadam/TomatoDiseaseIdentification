@echo off
title LeafVision-DINO (ViT-S/16) + AgERA5 FastAPI Engine
echo ====================================================================
echo Starting LeafVision-DINO (ViT-S/16) + AgERA5 Machine Learning Server
echo Host: http://127.0.0.1:8000
echo ====================================================================

python -m uvicorn ml_service.app:app --host 127.0.0.1 --port 8000 --reload
pause
