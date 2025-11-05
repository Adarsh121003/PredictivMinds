from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from routes import health, predictions, dashboard
from services.model_loader import model_loader
from utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Secure, AI-driven Governance Platform transforming raw government data into predictive intelligence",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event


@app.on_event("startup")
async def startup_event():
    """Load all models on startup"""
    logger.logger.info(
        f" Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.logger.info("="*60)
    success = model_loader.load_all_models()
    if success:
        logger.logger.info("System ready to serve predictions")
    else:
        logger.logger.error("System startup failed - check model paths")
    logger.logger.info("="*60)

# Shutdown event


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.logger.info(
        "Shutting down PredictivMinds Maharashtra Governance AI API")

# Include routers
app.include_router(health.router)
app.include_router(predictions.router, prefix=settings.API_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
