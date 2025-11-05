import joblib
from config.settings import settings
from utils.logger import logger


class ModelLoader:
    """
    Centralized model loading service
    """

    def __init__(self):
        self.demand_model = None
        self.demand_encoders = None
        self.demand_features = None

        self.crisis_model = None
        self.crisis_encoders = None
        self.crisis_features = None

        self.priority_engine = None

    def load_all_models(self):
        """Load all ML models"""
        try:
            # Demand Forecasting Model
            self.demand_model = joblib.load(settings.MODEL_PATH_DEMAND)
            self.demand_encoders = joblib.load(
                settings.MODEL_PATH_ENCODERS_DEMAND)
            self.demand_features = joblib.load(
                settings.MODEL_PATH_FEATURES_DEMAND)
            logger.logger.info(
                "✅ Demand Forecasting Model loaded (R² = 0.960)")

            # Crisis Prediction Model
            self.crisis_model = joblib.load(settings.MODEL_PATH_CRISIS)
            self.crisis_encoders = joblib.load(
                settings.MODEL_PATH_ENCODERS_CRISIS)
            self.crisis_features = joblib.load(
                settings.MODEL_PATH_FEATURES_CRISIS)
            logger.logger.info("✅ Crisis Prediction Model loaded (F1 = 0.992)")

            # Priority Engine
            from priority_engine_helper import PriorityScoringEngine
            self.priority_engine = PriorityScoringEngine()
            logger.logger.info("✅ Priority Scoring Engine loaded")

            logger.logger.info("🎉 All models loaded successfully!")
            return True

        except Exception as e:
            logger.log_error(e, "Model loading failed")
            return False


# Global model loader instance
model_loader = ModelLoader()
