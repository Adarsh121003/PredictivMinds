from fastapi import APIRouter, Request
from models.responses import HealthCheckResponse
from services.model_loader import model_loader
from middleware.data_privacy import privacy_framework
from utils.logger import logger
from config.settings import settings

router = APIRouter(tags=["Health Check"])


@router.get("/", response_model=dict)
async def root(request: Request):
    """Root endpoint"""
    logger.log_api_request("/", "GET", {}, request.client.host)
    return {
        "status": "active",
        "api": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "privacy_compliant": True
    }


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(request: Request):
    """Detailed health check"""
    logger.log_api_request("/health", "GET", {}, request.client.host)

    return HealthCheckResponse(
        status="healthy",
        api_version=settings.APP_VERSION,
        models={
            "demand_forecasting": {
                "loaded": model_loader.demand_model is not None,
                "type": "XGBoost Regressor",
                "performance": "R² = 0.960"
            },
            "crisis_prediction": {
                "loaded": model_loader.crisis_model is not None,
                "type": "XGBoost Classifier",
                "performance": "F1 = 0.992, Accuracy = 99.8%"
            },
            "priority_engine": {
                "loaded": model_loader.priority_engine is not None,
                "type": "Multi-criteria Ranking"
            }
        },
        privacy_framework=privacy_framework.generate_privacy_report()
    )
