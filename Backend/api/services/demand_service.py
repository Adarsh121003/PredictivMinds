import pandas as pd
from services.model_loader import model_loader
from models.requests import DemandForecastRequest
from models.responses import DemandForecastResponse, DemandPrediction
from middleware.data_privacy import privacy_framework
from utils.logger import logger


class DemandForecastingService:
    """
    Business logic for demand forecasting
    """

    @staticmethod
    def predict(request: DemandForecastRequest, ip_address: str) -> DemandForecastResponse:
        """
        Predict service demand
        """
        # Anonymize data
        anonymized_data = privacy_framework.anonymize_data(request.dict())

        # Encode categorical variables
        district_encoded = model_loader.demand_encoders['district'].transform([
                                                                              request.district])[0]
        service_encoded = model_loader.demand_encoders['service_type'].transform(
            [request.service_type])[0]
        demand_trend = request.demand_lag_7days - request.demand_lag_30days

        # Prepare features
        features = pd.DataFrame([{
            'district_encoded': district_encoded,
            'service_type_encoded': service_encoded,
            'day_of_week': request.day_of_week,
            'month': request.month,
            'is_weekend': request.is_weekend,
            'is_monsoon': request.is_monsoon,
            'population_factor': request.population_factor,
            'urban_ratio': request.urban_ratio,
            'demand_lag_7days': request.demand_lag_7days,
            'demand_lag_30days': request.demand_lag_30days,
            'demand_trend': demand_trend,
            'resource_utilization_rate': request.resource_utilization_rate,
            'complaint_rate': request.complaint_rate,
            'response_time_minutes': request.response_time_minutes
        }])

        # Predict
        prediction_value = model_loader.demand_model.predict(features)[0]
        confidence = "High" if abs(demand_trend) < 10 else "Medium"
        trend = "Increasing" if demand_trend > 0 else "Decreasing" if demand_trend < 0 else "Stable"

        # Create response
        prediction = DemandPrediction(
            district=request.district,
            service_type=request.service_type,
            predicted_demand=int(round(prediction_value)),
            confidence_level=confidence,
            trend=trend,
            model_version="1.0"
        )

        response = DemandForecastResponse(
            success=True,
            prediction=prediction
        )

        # Log prediction
        logger.log_prediction(
            "demand_forecasting",
            request.dict(),
            response.dict(),
            ip_address
        )

        return response
