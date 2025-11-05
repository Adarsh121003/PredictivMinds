import pandas as pd
from services.model_loader import model_loader
from models.requests import CrisisPredictionRequest
from models.responses import CrisisPredictionResponse, CrisisPrediction
from middleware.data_privacy import privacy_framework
from utils.logger import logger


class CrisisPredictionService:
    """
    Business logic for crisis prediction
    """

    @staticmethod
    def predict(request: CrisisPredictionRequest, ip_address: str) -> CrisisPredictionResponse:
        """
        Predict water shortage crisis
        """
        # Anonymize data
        anonymized_data = privacy_framework.anonymize_data(request.dict())

        # Encode features
        district_encoded = model_loader.crisis_encoders['district'].transform([
                                                                              request.district])[0]
        demand_trend = request.demand_lag_7days - request.demand_lag_30days
        response_efficiency = 100 / (request.response_time_hours + 1)

        # Prepare features
        features = pd.DataFrame([{
            'district_encoded': district_encoded,
            'month': request.month,
            'is_monsoon': request.is_monsoon,
            'population_factor': request.population_factor,
            'demand_requests': request.demand_requests,
            'pending_requests': request.pending_requests,
            'citizen_complaints': request.citizen_complaints,
            'response_time_hours': request.response_time_hours,
            'demand_lag_7days': request.demand_lag_7days,
            'demand_lag_30days': request.demand_lag_30days,
            'demand_trend': demand_trend,
            'resolution_rate': request.resolution_rate,
            'response_efficiency': response_efficiency,
            'water_level_drop_7days': 0,
            'water_level_drop_30days': 0
        }])

        # Predict
        prediction_value = model_loader.crisis_model.predict(features)[0]
        probability = float(
            model_loader.crisis_model.predict_proba(features)[0][1])

        # Determine alert level
        if probability > 0.8:
            alert_level = "CRITICAL"
        elif probability > 0.6:
            alert_level = "HIGH"
        elif probability > 0.4:
            alert_level = "MEDIUM"
        else:
            alert_level = "LOW"

        # Generate recommendations
        recommendations = []
        if prediction_value == 1:
            recommendations = [
                "Deploy mobile water tankers immediately",
                "Issue public advisory via SMS/WhatsApp",
                "Coordinate with nearby wards for water sharing",
                "Increase water treatment plant capacity"
            ]

        # Create response
        prediction = CrisisPrediction(
            district=request.district,
            crisis_predicted=bool(prediction_value),
            probability=round(probability, 3),
            alert_level=alert_level,
            days_until_crisis=7 if prediction_value else None,
            affected_population_estimate=int(
                request.demand_requests * request.population_factor * 100),
            recommendations=recommendations,
            model_version="1.0"
        )

        response = CrisisPredictionResponse(
            success=True,
            prediction=prediction
        )

        # Log prediction
        logger.log_prediction(
            "crisis_prediction",
            request.dict(),
            response.dict(),
            ip_address
        )

        return response
