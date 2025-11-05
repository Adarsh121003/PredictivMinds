from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class BaseResponse(BaseModel):
    success: bool
    timestamp: str = datetime.now().isoformat()


class DemandPrediction(BaseModel):
    district: str
    service_type: str
    predicted_demand: int
    confidence_level: str
    trend: str
    model_version: str
    _privacy_protected: bool = True


class DemandForecastResponse(BaseResponse):
    prediction: DemandPrediction


class CrisisPrediction(BaseModel):
    district: str
    crisis_predicted: bool
    probability: float
    alert_level: str
    days_until_crisis: Optional[int]
    affected_population_estimate: int
    recommendations: List[str]
    model_version: str
    _privacy_protected: bool = True


class CrisisPredictionResponse(BaseResponse):
    prediction: CrisisPrediction


class PriorityComponents(BaseModel):
    urgency: int
    impact: int
    resource_availability: int
    citizen_sentiment: int


class PriorityResult(BaseModel):
    district: str
    domain: str
    issue_type: str
    priority_score: float
    components: PriorityComponents
    recommendation: str
    _privacy_protected: bool = True


class PriorityScoreResponse(BaseResponse):
    priority: PriorityResult


class HealthCheckResponse(BaseModel):
    status: str
    api_version: str
    models: Dict[str, Any]
    privacy_framework: Dict[str, Any]
