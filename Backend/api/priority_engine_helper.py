import pandas as pd


class PriorityScoringEngine:
    """
    Calculate priority scores for all government issues
    Formula: Priority = Urgency×0.4 + Impact×0.3 + Resources×0.2 + Sentiment×0.1
    """

    def __init__(self):
        self.weights = {
            'urgency': 0.4,
            'impact': 0.3,
            'resource_availability': 0.2,
            'citizen_sentiment': 0.1
        }

    def calculate_urgency_score(self, row, domain):
        """Urgency: How soon will it become critical? (0-10 scale)"""
        if domain == 'Health':
            base_urgency = 7
            if row.get('requests', 0) > 80:
                base_urgency += 2
            if row.get('response_time_minutes', 20) > 30:
                base_urgency += 1
        elif domain == 'Infrastructure':
            base_urgency = 5
            pending_rate = row.get('pending_requests', 0) / \
                (row.get('requests', 1) + 1)
            if pending_rate > 0.5:
                base_urgency += 3
            if row.get('is_monsoon', 0) == 1:
                base_urgency += 2
        else:  # PublicSafety
            base_urgency = 8
            if row.get('severity_level', 'Low') == 'Critical':
                base_urgency = 10
            elif row.get('severity_level', 'Low') == 'High':
                base_urgency = 9
        return min(10, base_urgency)

    def calculate_impact_score(self, row):
        """Impact: Number of citizens affected (0-10 scale)"""
        requests = row.get('requests', 0)
        pop_factor = row.get('population_factor', 1.0)
        affected_citizens = requests * pop_factor * 100

        if affected_citizens > 50000:
            return 10
        elif affected_citizens > 20000:
            return 8
        elif affected_citizens > 10000:
            return 6
        elif affected_citizens > 5000:
            return 4
        else:
            return 2

    def calculate_resource_score(self, row, domain):
        """Resource Availability: Can we fix it now? (0-10, higher = easier)"""
        if domain == 'Health':
            resource_ratio = row.get(
                'resource_availability', 0) / (row.get('requests', 1) + 1)
            if resource_ratio > 0.9:
                return 9
            elif resource_ratio > 0.7:
                return 6
            else:
                return 3
        elif domain == 'Infrastructure':
            resolution_rate = row.get(
                'resolved_requests', 0) / (row.get('requests', 1) + 1)
            if resolution_rate > 0.8:
                return 8
            elif resolution_rate > 0.5:
                return 5
            else:
                return 2
        else:  # PublicSafety
            resolved_ratio = row.get(
                'incidents_resolved', 0) / (row.get('requests', 1) + 1)
            if resolved_ratio > 0.9:
                return 9
            elif resolved_ratio > 0.7:
                return 6
            else:
                return 3

    def calculate_sentiment_score(self, row):
        """Citizen Sentiment: Public anger level (0-10 scale)"""
        complaints = row.get('complaints', 0)
        if complaints > 10:
            return 10
        elif complaints > 7:
            return 8
        elif complaints > 5:
            return 6
        elif complaints > 3:
            return 4
        else:
            return 2

    def calculate_priority_for_issue(self, row, domain):
        """Calculate final priority score for a single issue"""
        urgency = self.calculate_urgency_score(row, domain)
        impact = self.calculate_impact_score(row)
        resource = self.calculate_resource_score(row, domain)
        sentiment = self.calculate_sentiment_score(row)

        priority_score = (
            urgency * self.weights['urgency'] +
            impact * self.weights['impact'] +
            resource * self.weights['resource_availability'] +
            sentiment * self.weights['citizen_sentiment']
        )

        return {
            'priority_score': round(priority_score, 2),
            'urgency': urgency,
            'impact': impact,
            'resource_availability': resource,
            'citizen_sentiment': sentiment
        }
