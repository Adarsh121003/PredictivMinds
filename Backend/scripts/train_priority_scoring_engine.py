# train_priority_scoring_engine.py
import pandas as pd
import numpy as np
import joblib
from datetime import datetime


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

    def load_all_domain_data(self):
        """
        Load data from all 3 domains
        """
        print("\n" + "="*70)
        print("📊 PRIORITY SCORING ENGINE - DATA LOADING")
        print("="*70 + "\n")

        # Load all domains
        health_df = pd.read_csv('maharashtra_health_data.csv')
        infra_df = pd.read_csv('maharashtra_infrastructure_data.csv')
        safety_df = pd.read_csv('maharashtra_public_safety_data.csv')

        print(f"✅ Health data: {health_df.shape}")
        print(f"✅ Infrastructure data: {infra_df.shape}")
        print(f"✅ Public Safety data: {safety_df.shape}")

        # Standardize column names for unified processing
        health_df['issue_type'] = health_df['service_type']
        health_df['requests'] = health_df['demand_requests']
        health_df['complaints'] = health_df['citizen_complaints']

        infra_df['issue_type'] = infra_df['service_type']
        infra_df['requests'] = infra_df['demand_requests']
        infra_df['complaints'] = infra_df['citizen_complaints']

        safety_df['issue_type'] = safety_df['service_type']
        safety_df['requests'] = safety_df['incidents_reported']
        safety_df['complaints'] = 0  # Safety doesn't have complaint column

        return health_df, infra_df, safety_df

    def calculate_urgency_score(self, row, domain):
        """
        Urgency: How soon will it become critical? (0-10 scale)
        Based on: current demand, pending requests, response time
        """
        if domain == 'Health':
            # Health is most urgent
            base_urgency = 7

            # High demand = more urgent
            if row['requests'] > 80:
                base_urgency += 2

            # Slow response = more urgent
            if row.get('response_time_minutes', 20) > 30:
                base_urgency += 1

        elif domain == 'Infrastructure':
            base_urgency = 5

            # High pending = more urgent
            pending_rate = row.get('pending_requests', 0) / \
                (row['requests'] + 1)
            if pending_rate > 0.5:
                base_urgency += 3

            # Monsoon + water issue = urgent
            if row.get('is_monsoon', 0) == 1 and 'Water' in row['issue_type']:
                base_urgency += 2

        else:  # PublicSafety
            base_urgency = 8  # Safety is high priority

            # Critical severity = max urgency
            if row.get('severity_level', 'Low') == 'Critical':
                base_urgency = 10
            elif row.get('severity_level', 'Low') == 'High':
                base_urgency = 9

        return min(10, base_urgency)

    def calculate_impact_score(self, row):
        """
        Impact: Number of citizens affected (0-10 scale)
        Based on: requests, district population
        """
        requests = row['requests']
        pop_factor = row.get('population_factor', 1.0)

        # Estimate affected citizens
        affected_citizens = requests * pop_factor * 100  # Rough estimate

        # Scale to 0-10
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
        """
        Resource Availability: Can we fix it now? (0-10, higher = easier)
        Based on: resource gap, resolution rate
        """
        if domain == 'Health':
            # Resource availability ratio
            resource_ratio = row.get(
                'resource_availability', 0) / (row['requests'] + 1)

            if resource_ratio > 0.9:
                return 9  # Good resources
            elif resource_ratio > 0.7:
                return 6
            else:
                return 3  # Resource shortage

        elif domain == 'Infrastructure':
            # Resolution rate
            resolution_rate = row.get(
                'resolved_requests', 0) / (row['requests'] + 1)

            if resolution_rate > 0.8:
                return 8
            elif resolution_rate > 0.5:
                return 5
            else:
                return 2

        else:  # PublicSafety
            # Incidents resolved ratio
            resolved_ratio = row.get(
                'incidents_resolved', 0) / (row['requests'] + 1)

            if resolved_ratio > 0.9:
                return 9
            elif resolved_ratio > 0.7:
                return 6
            else:
                return 3

    def calculate_sentiment_score(self, row):
        """
        Citizen Sentiment: Public anger level (0-10 scale)
        Based on: complaint count
        """
        complaints = row.get('complaints', 0)

        # More complaints = higher sentiment score (more anger)
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
        """
        Calculate final priority score for a single issue
        """
        urgency = self.calculate_urgency_score(row, domain)
        impact = self.calculate_impact_score(row)
        resource = self.calculate_resource_score(row, domain)
        sentiment = self.calculate_sentiment_score(row)

        # Weighted sum
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

    def rank_all_issues(self, health_df, infra_df, safety_df):
        """
        Rank all issues across all domains
        """
        print("\n" + "="*70)
        print("🎯 CALCULATING PRIORITY SCORES FOR ALL ISSUES")
        print("="*70 + "\n")

        all_issues = []

        # Sample from each domain (for demo - use last 100 entries)
        print("📊 Processing Health domain...")
        for idx, row in health_df.tail(100).iterrows():
            scores = self.calculate_priority_for_issue(row, 'Health')
            all_issues.append({
                'issue_id': f"H-{idx}",
                'domain': 'Health',
                'district': row['district'],
                'issue_type': row['issue_type'],
                'timestamp': row['timestamp'],
                'requests': row['requests'],
                **scores
            })

        print("📊 Processing Infrastructure domain...")
        for idx, row in infra_df.tail(100).iterrows():
            scores = self.calculate_priority_for_issue(row, 'Infrastructure')
            all_issues.append({
                'issue_id': f"I-{idx}",
                'domain': 'Infrastructure',
                'district': row['district'],
                'issue_type': row['issue_type'],
                'timestamp': row['timestamp'],
                'requests': row['requests'],
                **scores
            })

        print("📊 Processing Public Safety domain...")
        for idx, row in safety_df.tail(100).iterrows():
            scores = self.calculate_priority_for_issue(row, 'PublicSafety')
            all_issues.append({
                'issue_id': f"S-{idx}",
                'domain': 'PublicSafety',
                'district': row['district'],
                'issue_type': row['issue_type'],
                'timestamp': row['timestamp'],
                'requests': row['requests'],
                **scores
            })

        # Create DataFrame and rank
        issues_df = pd.DataFrame(all_issues)
        issues_df = issues_df.sort_values(
            'priority_score', ascending=False).reset_index(drop=True)
        issues_df['rank'] = range(1, len(issues_df) + 1)

        print(f"✅ Calculated priority for {len(issues_df)} issues\n")

        return issues_df

    def save_priority_engine(self):
        """
        Save priority scoring logic
        """
        print("💾 Saving priority scoring engine...")
        joblib.dump(self, 'priority_scoring_engine.pkl')
        print("✅ Engine saved: priority_scoring_engine.pkl")

    def display_top_priorities(self, ranked_df, top_n=20):
        """
        Display top N priority issues
        """
        print("\n" + "="*70)
        print(f"🏆 TOP {top_n} PRIORITY ISSUES")
        print("="*70 + "\n")

        top_issues = ranked_df.head(top_n)

        print(
            f"{'Rank':<6} {'Domain':<15} {'District':<12} {'Issue':<25} {'Priority':<10}")
        print("-"*70)

        for _, row in top_issues.iterrows():
            issue_short = row['issue_type'][:23]
            print(f"{row['rank']:<6} {row['domain']:<15} {row['district']:<12} "
                  f"{issue_short:<25} {row['priority_score']:<10.2f}")

        print("\n" + "="*70)
        print("📈 PRIORITY DISTRIBUTION BY DOMAIN")
        print("="*70)

        domain_stats = top_issues.groupby('domain').agg({
            'priority_score': ['count', 'mean', 'max']
        }).round(2)

        print(domain_stats)

        # Save to CSV
        ranked_df.to_csv('priority_ranked_issues.csv', index=False)
        print(f"\n✅ Full ranked list saved: priority_ranked_issues.csv")


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏛️  MODEL 3: PRIORITY SCORING ENGINE")
    print("="*70)

    engine = PriorityScoringEngine()

    # Step 1: Load all domain data
    health_df, infra_df, safety_df = engine.load_all_domain_data()

    # Step 2: Rank all issues
    ranked_issues = engine.rank_all_issues(health_df, infra_df, safety_df)

    # Step 3: Display top priorities
    engine.display_top_priorities(ranked_issues, top_n=20)

    # Step 4: Save engine
    engine.save_priority_engine()

    print("\n" + "="*70)
    print("✅ MODEL 3 (PRIORITY SCORING ENGINE) - COMPLETE!")
    print("="*70)
    print("\n📊 Priority Formula Used:")
    print("   Priority = Urgency×0.4 + Impact×0.3 + Resources×0.2 + Sentiment×0.1")
    print("\n📈 All 3 Models Complete!")
    print("   1. ✅ Health Demand Forecasting (R²=0.960)")
    print("   2. ✅ Crisis Prediction (F1=0.992)")
    print("   3. ✅ Priority Scoring Engine")
    print("="*70 + "\n")
