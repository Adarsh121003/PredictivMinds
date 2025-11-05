from pydantic import BaseModel, Field
from typing import Optional


class DemandForecastRequest(BaseModel):
    district: str = Field(..., description="District name")
    service_type: str = Field(..., description="Type of service")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    day_of_week: int = Field(..., ge=0, le=6,
                             description="Day of week (0=Mon)")
    is_weekend: int = Field(..., ge=0, le=1, description="Is weekend (0/1)")
    is_monsoon: int = Field(..., ge=0, le=1,
                            description="Is monsoon season (0/1)")
    population_factor: float = Field(..., description="Population factor")
    urban_ratio: float = Field(..., description="Urban ratio")
    demand_lag_7days: float = Field(..., description="7-day demand average")
    demand_lag_30days: float = Field(..., description="30-day demand average")
    resource_utilization_rate: float = Field(...,
                                             description="Resource utilization rate")
    complaint_rate: float = Field(..., description="Complaint rate")
    response_time_minutes: float = Field(...,
                                         description="Response time in minutes")

    class Config:
        json_schema_extra = {
            "example": {
                "district": "Mumbai",
                "service_type": "Ambulance_Emergency",
                "month": 7,
                "day_of_week": 1,
                "is_weekend": 0,
                "is_monsoon": 1,
                "population_factor": 2.5,
                "urban_ratio": 1.0,
                "demand_lag_7days": 45.0,
                "demand_lag_30days": 42.0,
                "resource_utilization_rate": 0.75,
                "complaint_rate": 0.15,
                "response_time_minutes": 16.5
            }
        }


class CrisisPredictionRequest(BaseModel):
    district: str = Field(..., description="District name")
    month: int = Field(..., ge=1, le=12, description="Month")
    is_monsoon: int = Field(..., ge=0, le=1, description="Monsoon flag")
    population_factor: float = Field(..., description="Population factor")
    demand_requests: int = Field(..., description="Demand requests")
    pending_requests: int = Field(..., description="Pending requests")
    citizen_complaints: int = Field(..., description="Citizen complaints")
    response_time_hours: float = Field(...,
                                       description="Response time in hours")
    demand_lag_7days: float = Field(..., description="7-day demand average")
    demand_lag_30days: float = Field(..., description="30-day demand average")
    resolution_rate: float = Field(..., description="Resolution rate")

    class Config:
        json_schema_extra = {
            "example": {
                "district": "Nagpur",
                "month": 5,
                "is_monsoon": 0,
                "population_factor": 1.5,
                "demand_requests": 80,
                "pending_requests": 35,
                "citizen_complaints": 12,
                "response_time_hours": 48.0,
                "demand_lag_7days": 75.0,
                "demand_lag_30days": 60.0,
                "resolution_rate": 0.45
            }
        }


class PriorityScoreRequest(BaseModel):
    domain: str = Field(...,
                        description="Domain (Health/Infrastructure/PublicSafety)")
    district: str = Field(..., description="District name")
    issue_type: str = Field(..., description="Type of issue")
    requests: int = Field(..., description="Number of requests")
    complaints: int = Field(..., description="Number of complaints")
    response_time: float = Field(..., description="Response time")
    is_monsoon: int = Field(..., ge=0, le=1, description="Monsoon flag")
    population_factor: float = Field(..., description="Population factor")
    resolution_rate: Optional[float] = Field(
        0.7, description="Resolution rate")
    severity_level: Optional[str] = Field(
        "Medium", description="Severity level")

    class Config:
        json_schema_extra = {
            "example": {
                "domain": "Health",
                "district": "Pune",
                "issue_type": "Hospital_Bed_ICU",
                "requests": 95,
                "complaints": 8,
                "response_time": 25.5,
                "is_monsoon": 0,
                "population_factor": 2.0,
                "resolution_rate": 0.65,
                "severity_level": "High"
            }
        }
