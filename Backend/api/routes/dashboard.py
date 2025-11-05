from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io
from utils.logger import logger
from middleware.data_privacy import privacy_framework

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/alerts")
async def get_critical_alerts(request: Request):
    """Get all critical alerts"""
    logger.log_api_request("/api/v1/dashboard/alerts",
                           "GET", {}, request.client.host)

    # Mock data
    alerts = [
        {
            "id": 1,
            "type": "water_shortage",
            "district": "Nagpur",
            "ward": "Ward_5",
            "probability": 0.87,
            "days_until": 3,
            "affected_population": 15000,
            "priority_score": 9.2,
            "status": "CRITICAL"
        },
        {
            "id": 2,
            "type": "hospital_overflow",
            "district": "Mumbai",
            "ward": "Ward_12",
            "probability": 0.78,
            "days_until": 5,
            "affected_population": 50000,
            "priority_score": 8.7,
            "status": "HIGH"
        },
        {
            "id": 3,
            "type": "road_collapse_risk",
            "district": "Pune",
            "ward": "Ward_8",
            "probability": 0.65,
            "days_until": 10,
            "affected_population": 8000,
            "priority_score": 7.5,
            "status": "MEDIUM"
        }
    ]

    return {
        "success": True,
        "alerts": alerts,
        "total_count": len(alerts),
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.get("/statistics")
async def get_statistics(request: Request):
    """Get overall system statistics"""
    logger.log_api_request("/api/v1/dashboard/statistics",
                           "GET", {}, request.client.host)

    return {
        "success": True,
        "statistics": {
            "total_predictions_today": 156,
            "critical_alerts": 3,
            "districts_monitored": 8,
            "average_response_time_hours": 4.2,
            "citizen_satisfaction_rate": 0.87,
            "models_active": 3,
            "data_sources_integrated": 3
        },
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.post("/upload/excel")
async def upload_excel_data(
    request: Request,
    file: UploadFile = File(...),
    domain: str = "health"
):
    """
    Upload Excel file for multi-domain data integration
    Solves: "siloed data assets" problem from challenge
    """
    logger.log_api_request("/api/v1/dashboard/upload/excel", "POST",
                           {"filename": file.filename, "domain": domain},
                           request.client.host)

    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Log file upload
        logger.log_file_upload(
            filename=file.filename,
            file_size=len(contents),
            domain=domain,
            ip=request.client.host
        )

        # Anonymize uploaded data
        anonymized_records = []
        for _, row in df.iterrows():
            anonymized_row = privacy_framework.anonymize_data(row.to_dict())
            anonymized_records.append(anonymized_row)

        # Furthure: Upload to BigQuery
        # from google.cloud import bigquery
        # client = bigquery.Client()
        # table_id = f""
        # client.load_table_from_dataframe(df, table_id)

        return {
            "success": True,
            "message": f"File uploaded successfully: {file.filename}",
            "records_processed": len(df),
            "domain": domain,
            "columns_detected": list(df.columns),
            "data_anonymized": True,
            "timestamp": pd.Timestamp.now().isoformat()
        }

    except Exception as e:
        logger.log_error(e, "Excel upload failed")
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")


@router.get("/privacy-report")
async def get_privacy_report(request: Request):
    """Get privacy compliance report"""
    logger.log_api_request(
        "/api/v1/dashboard/privacy-report", "GET", {}, request.client.host)

    report = privacy_framework.generate_privacy_report()

    return {
        "success": True,
        "privacy_report": report,
        "timestamp": pd.Timestamp.now().isoformat()
    }
