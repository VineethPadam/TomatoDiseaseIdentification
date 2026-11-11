"""
FastAPI Server for LeafVision-DINO ViT-S/16 & AgERA5 v2.0
=========================================================
Exposes high-speed REST API endpoints for tomato disease prediction,
AgERA5 meteorological conditioning, and model inspection.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import uvicorn
import logging

from ml_service.model.weights import LeafVisionInferenceEngine
from ml_service.data.plantvillage_classes import PLANTVILLAGE_TOMATO_CLASSES, DISEASE_METADATA
from ml_service.data.agera5_indicators import AGERA5_PRESET_SCENARIOS, calculate_vpd
from ml_service.pdf_generator import build_phytosanitary_pdf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LeafVisionAPI")

app = FastAPI(
    title="LeafVision-DINO (ViT-S/16) + AgERA5 Disease Identification API",
    version="1.0.0",
    description="Multimodal Vision Transformer & Copernicus AgERA5 microclimate disease inference engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
engine: Optional[LeafVisionInferenceEngine] = None


@app.on_event("startup")
def load_model():
    global engine
    logger.info("Initializing LeafVision-DINO ViT-S/16 model and weights...")
    engine = LeafVisionInferenceEngine()
    logger.info("LeafVision-DINO ViT-S/16 successfully loaded and ready for inference!")


@app.get("/")
def root():
    return {
        "service": "LeafVision-DINO (ViT-S/16) + AgERA5 v2.0 API",
        "status": "ONLINE",
        "model_architecture": "Vision Transformer Small (16x16 patch, 384 embed_dim, 6 heads, DINO self-supervised features)",
        "dataset": "PlantVillage (10 Tomato Disease Classes)",
        "weather_dataset": "Copernicus AgERA5 v2.0 Agrometeorological Indicators",
        "endpoints": ["/predict", "/classes", "/agera5-presets", "/health"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "model_loaded": engine is not None,
        "classes_count": len(PLANTVILLAGE_TOMATO_CLASSES)
    }


@app.get("/classes")
def list_classes():
    return {
        "count": len(PLANTVILLAGE_TOMATO_CLASSES),
        "classes": PLANTVILLAGE_TOMATO_CLASSES,
        "metadata": DISEASE_METADATA
    }


@app.get("/agera5-presets")
def get_agera5_presets():
    return AGERA5_PRESET_SCENARIOS


@app.post("/predict")
async def predict_disease(
    file: UploadFile = File(...),
    temperature: Optional[float] = Form(None),
    humidity: Optional[float] = Form(None),
    precipitation: Optional[float] = Form(None),
    solar_radiation: Optional[float] = Form(None),
    wind_speed: Optional[float] = Form(None),
    vpd: Optional[float] = Form(None)
):
    """
    Receives tomato leaf image + optional AgERA5 weather indicators.
    Executes LeafVision-DINO ViT-S/16 inference with cross-modal fusion.
    """
    global engine
    if engine is None:
        raise HTTPException(status_code=503, detail="Model engine not initialized yet.")

    # Validate file extension
    valid_exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    if not any(file.filename.lower().endswith(ext) for ext in valid_exts):
        raise HTTPException(status_code=400, detail="Invalid image file format. Supported: JPG, PNG, WEBP.")

    try:
        contents = await file.read()

        # Assemble AgERA5 indicators if provided
        weather_dict = None
        if temperature is not None or humidity is not None:
            t = temperature if temperature is not None else 24.5
            h = humidity if humidity is not None else 70.0
            p = precipitation if precipitation is not None else 2.5
            s = solar_radiation if solar_radiation is not None else 18.0
            w = wind_speed if wind_speed is not None else 2.5
            v = vpd if vpd is not None else calculate_vpd(t, h)

            weather_dict = {
                "temperature": t,
                "humidity": h,
                "precipitation": p,
                "solar_radiation": s,
                "wind_speed": w,
                "vpd": v
            }

        result = engine.predict(contents, weather=weather_dict)
        result["filename"] = file.filename
        result["weather_input"] = weather_dict
        return result

    except Exception as e:
        logger.error(f"Inference error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Inference execution failed: {str(e)}")


@app.post("/generate-pdf")
async def generate_pdf_endpoint(request: Request):
    """
    Builds and returns a publication-grade, byte-for-byte phytosanitary PDF report
    with embedded side-by-side original and Grad-CAM heatmap images.
    Guarantees non-empty PDF, vector crispness, and zero image cutting/distortion.
    """
    try:
        data = await request.json()
        record = data.get("record", data)
        pdf_bytes = build_phytosanitary_pdf(record=record)
        
        disease_clean = str(record.get("predictedDisease", "Leaf")).replace(" ", "_").replace("/", "_")
        filename = f"AgroVision_Phytosanitary_Report_{record.get('id', 'scan')}_{disease_clean}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\"",
                "Content-Length": str(len(pdf_bytes)),
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        logger.error(f"PDF generation endpoint failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
