import pandas as pd
from services.model_loader import model_loader
from models.requests import PriorityScoreRequest
from models.responses import PriorityScoreResponse, PriorityResult, PriorityComponents
from middleware.data_privacy import privacy_framework
from utils.logger import logger


class PriorityService:
    """Business logic for priority scoring"""

    @staticmethod
    def calculate(request: PriorityScoreRequest, ip_address: str) -> PriorityScoreResponse:
        """Calculate priority score for an issue"""

        # Anonymize data
        anonymized_data = privacy_framework.anonymize_data(request.dict())

        # Create dummy row for scoring
        dummy_row = {
            'district': request.district,
            'issue_type': request.issue_type,
            'requests': request.requests,
            'complaints': request.complaints,
            'response_time_minutes': request.response_time if request.domain == 'Health' else 0,
            'response_time_hours': request.response_time if request.domain != 'Health' else 0,
            'is_monsoon': request.is_monsoon,
            'population_factor': request.population_factor,
            'resolved_requests': int(request.requests * request.resolution_rate),
            'pending_requests': int(request.requests * (1 - request.resolution_rate)),
            'resource_availability': int(request.requests * request.resolution_rate),
            'incidents_resolved': int(request.requests * request.resolution_rate),
            'severity_level': request.severity_level
        }

        # Calculate priority components
        scores = model_loader.priority_engine.calculate_priority_for_issue(
            pd.Series(dummy_row),
            request.domain
        )

        # Create response
        components = PriorityComponents(
            urgency=scores['urgency'],
            impact=scores['impact'],
            resource_availability=scores['resource_availability'],
            citizen_sentiment=scores['citizen_sentiment']
        )

        recommendation = "Immediate action required" if scores['priority_score'] > 7.5 else \
            "Schedule within 24 hours" if scores['priority_score'] > 6.0 else \
            "Normal priority queue"

        priority = PriorityResult(
            district=request.district,
            domain=request.domain,
            issue_type=request.issue_type,
            priority_score=scores['priority_score'],
            components=components,
            recommendation=recommendation
        )

        response = PriorityScoreResponse(
            success=True,
            priority=priority
        )

        # Log
        logger.log_prediction(
            "priority_scoring",
            request.dict(),
            response.dict(),
            ip_address
        )

        return response
