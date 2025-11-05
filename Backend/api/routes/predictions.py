from fastapi import APIRouter, HTTPException, Request
from models.requests import DemandForecastRequest, CrisisPredictionRequest, PriorityScoreRequest
from models.responses import DemandForecastResponse, CrisisPredictionResponse, PriorityScoreResponse
from services.demand_service import DemandForecastingService
from services.crisis_service import CrisisPredictionService
from services.priority_service import PriorityService
from utils.logger import logger

router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("/demand", response_model=DemandForecastResponse)
async def predict_demand(request: Request, payload: DemandForecastRequest):
    """
    Predict service demand for next week
    Model: XGBoost Regressor (R² = 0.960)
    """
    logger.log_api_request("/api/v1/predict/demand",
                           "POST", payload.dict(), request.client.host)

    try:
        return DemandForecastingService.predict(payload, request.client.host)
    except Exception as e:
        logger.log_error(e, "Demand prediction failed")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/crisis", response_model=CrisisPredictionResponse)
async def predict_crisis(request: Request, payload: CrisisPredictionRequest):
    """
    Predict water shortage crisis
    Model: XGBoost Classifier (F1 = 0.992, Accuracy = 99.8%)
    """
    logger.log_api_request("/api/v1/predict/crisis",
                           "POST", payload.dict(), request.client.host)

    try:
        return CrisisPredictionService.predict(payload, request.client.host)
    except Exception as e:
        logger.log_error(e, "Crisis prediction failed")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/priority", response_model=PriorityScoreResponse)
async def calculate_priority(request: Request, payload: PriorityScoreRequest):
    """
    Calculate priority score for an issue
    Engine: Multi-criteria Decision Analysis
    """
    logger.log_api_request("/api/v1/calculate/priority",
                           "POST", payload.dict(), request.client.host)

    try:
        return PriorityService.calculate(payload, request.client.host)
    except Exception as e:
        logger.log_error(e, "Priority calculation failed")
        raise HTTPException(status_code=400, detail=str(e))
