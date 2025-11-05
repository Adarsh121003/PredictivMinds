FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all API code
COPY . .

# Copy trained models from parent directory
RUN mkdir -p models
COPY ../models/health_demand_forecasting ./models/health_demand_forecasting
COPY ../models/crisis_prediction ./models/crisis_prediction  
COPY ../models/priority_engine ./models/priority_engine

# Create logs directory
RUN mkdir -p logs

# Expose port (Cloud Run uses $PORT)
ENV PORT=8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run application
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
