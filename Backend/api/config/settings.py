from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    APP_NAME: str = "Maharashtra Governance AI"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Model Paths
    MODEL_PATH_DEMAND: str = "../models/health_demand_forecasting/model_health_demand_forecasting.pkl"
    MODEL_PATH_ENCODERS_DEMAND: str = "../models/health_demand_forecasting/label_encoders.pkl"
    MODEL_PATH_FEATURES_DEMAND: str = "../models/health_demand_forecasting/feature_columns.pkl"

    MODEL_PATH_CRISIS: str = "../models/crisis_prediction/model_crisis_water_shortage.pkl"
    MODEL_PATH_ENCODERS_CRISIS: str = "../models/crisis_prediction/crisis_label_encoders.pkl"
    MODEL_PATH_FEATURES_CRISIS: str = "../models/crisis_prediction/crisis_feature_columns.pkl"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"

    # Privacy
    ENABLE_DATA_ANONYMIZATION: bool = True
    ENABLE_AUDIT_LOGGING: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
