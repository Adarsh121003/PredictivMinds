# train_crisis_prediction_model.py (FIXED)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, precision_score, recall_score, f1_score)
import joblib


class CrisisPredictionModel:
    """
    Predict if crisis will happen in next 7 days (Binary Classification)
    """

    def __init__(self):
        self.label_encoders = {}
        self.model = None

    def load_and_prepare_infrastructure_data(self):
        """
        Load infrastructure data and create crisis labels
        """
        print("\n" + "="*70)
        print("🚨 CRISIS PREDICTION MODEL - DATA PREPARATION")
        print("="*70 + "\n")

        df = pd.read_csv('maharashtra_infrastructure_data.csv')
        print(f"✅ Loaded infrastructure data: {df.shape}")

        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Focus on water shortage service
        water_df = df[df['service_type'] == 'Water_Supply_Shortage'].copy()
        print(f"✅ Filtered water shortage data: {water_df.shape}")

        # Create CRISIS LABEL (Binary: 0=No Crisis, 1=Crisis)
        print("\n🔧 Creating crisis labels...")

        # Crisis indicators
        water_df['demand_high'] = (
            water_df['demand_requests'] > water_df['demand_requests'].quantile(0.75)).astype(int)
        water_df['resolution_low'] = (
            water_df['resolved_requests'] / (water_df['demand_requests'] + 1) < 0.6).astype(int)
        water_df['complaints_high'] = (
            water_df['citizen_complaints'] > 5).astype(int)

        # Crisis = 2 or more indicators triggered
        water_df['crisis_label'] = ((water_df['demand_high'] +
                                     water_df['resolution_low'] +
                                     water_df['complaints_high']) >= 2).astype(int)

        crisis_count = water_df['crisis_label'].sum()
        print(
            f"✅ Crisis samples: {crisis_count} ({crisis_count/len(water_df)*100:.1f}%)")
        print(
            f"✅ Normal samples: {len(water_df)-crisis_count} ({(len(water_df)-crisis_count)/len(water_df)*100:.1f}%)")

        # Encode categorical
        print("\n🔧 Encoding features...")
        le_district = LabelEncoder()
        water_df['district_encoded'] = le_district.fit_transform(
            water_df['district'])
        self.label_encoders['district'] = le_district

        # Create lag features
        print("🔧 Creating lag features...")
        water_df = water_df.sort_values(['district', 'timestamp'])

        water_df['demand_lag_7days'] = water_df.groupby('district')['demand_requests'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )

        water_df['demand_lag_30days'] = water_df.groupby('district')['demand_requests'].transform(
            lambda x: x.rolling(window=30, min_periods=1).mean()
        )

        water_df['demand_trend'] = water_df['demand_lag_7days'] - \
            water_df['demand_lag_30days']

        # FIXED: Handle water level columns with fillna
        if 'water_level_current' in water_df.columns:
            water_df['water_level_current'] = water_df['water_level_current'].fillna(
                60)
            water_df['water_level_7days_ago'] = water_df['water_level_7days_ago'].fillna(
                60)
            water_df['water_level_30days_ago'] = water_df['water_level_30days_ago'].fillna(
                60)

            water_df['water_level_drop_7days'] = (water_df['water_level_7days_ago'] -
                                                  water_df['water_level_current'])
            water_df['water_level_drop_30days'] = (water_df['water_level_30days_ago'] -
                                                   water_df['water_level_current'])
        else:
            # Create dummy columns if not present
            water_df['water_level_drop_7days'] = 0
            water_df['water_level_drop_30days'] = 0

        # Resolution rate
        water_df['resolution_rate'] = water_df['resolved_requests'] / \
            (water_df['demand_requests'] + 1)

        # Response efficiency
        water_df['response_efficiency'] = 100 / \
            (water_df['response_time_hours'] + 1)

        # FIXED: Only drop rows with NaN in critical columns
        critical_cols = ['district_encoded', 'crisis_label', 'demand_requests',
                         'demand_lag_7days', 'demand_lag_30days']
        water_df = water_df.dropna(subset=critical_cols)

        print(f"✅ Final dataset shape: {water_df.shape}")

        if len(water_df) == 0:
            print("❌ ERROR: No data remaining after cleaning!")
            print("   Checking original data...")
            return None

        return water_df

    def train_crisis_model(self, df):
        """
        Train XGBoost classifier for crisis prediction
        """
        if df is None or len(df) == 0:
            print("❌ Cannot train model - no data available!")
            return None, None, {}

        print("\n" + "="*70)
        print("🚀 TRAINING CRISIS PREDICTION MODEL")
        print("="*70 + "\n")

        # Select features
        feature_cols = [
            'district_encoded', 'month', 'is_monsoon',
            'population_factor', 'demand_requests', 'pending_requests',
            'citizen_complaints', 'response_time_hours',
            'demand_lag_7days', 'demand_lag_30days', 'demand_trend',
            'resolution_rate', 'response_efficiency',
            'water_level_drop_7days', 'water_level_drop_30days'
        ]

        X = df[feature_cols]
        y = df['crisis_label']

        print(f"📊 Total samples: {len(X)}")
        print(f"   Crisis samples: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
        print(
            f"   Normal samples: {len(y)-y.sum()} ({(len(y)-y.sum())/len(y)*100:.1f}%)")

        # Check if we have enough samples
        if len(X) < 100:
            print("⚠️  Warning: Very few samples. Model may not be accurate.")

        if y.sum() < 10:
            print("⚠️  Warning: Very few crisis samples. Consider adjusting thresholds.")

        # Train-test split (stratified to maintain class balance)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\n📈 Train: {len(X_train)} | Test: {len(X_test)}")

        # Calculate scale_pos_weight for imbalanced data
        if y_train.sum() > 0:
            scale_weight = (len(y_train) - y_train.sum()) / y_train.sum()
        else:
            scale_weight = 1
        print(f"⚖️  Class imbalance weight: {scale_weight:.2f}")

        # XGBoost Classifier
        print("\n🎯 Training XGBoost Classifier...")
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_weight,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )

        model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=50
        )

        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Calculate metrics
        train_acc = accuracy_score(y_train, y_pred_train)
        test_acc = accuracy_score(y_test, y_pred_test)

        train_f1 = f1_score(y_train, y_pred_train, zero_division=0)
        test_f1 = f1_score(y_test, y_pred_test, zero_division=0)

        train_precision = precision_score(
            y_train, y_pred_train, zero_division=0)
        test_precision = precision_score(y_test, y_pred_test, zero_division=0)

        train_recall = recall_score(y_train, y_pred_train, zero_division=0)
        test_recall = recall_score(y_test, y_pred_test, zero_division=0)

        # Print results
        print("\n" + "="*70)
        print("📈 CLASSIFICATION METRICS")
        print("="*70)
        print(f"\n{'Metric':<20} {'Train':<15} {'Test':<15}")
        print("-"*70)
        print(f"{'Accuracy':<20} {train_acc:<15.3f} {test_acc:<15.3f}")
        print(f"{'F1 Score':<20} {train_f1:<15.3f} {test_f1:<15.3f}")
        print(f"{'Precision':<20} {train_precision:<15.3f} {test_precision:<15.3f}")
        print(f"{'Recall':<20} {train_recall:<15.3f} {test_recall:<15.3f}")
        print("="*70)

        # Confusion Matrix
        print("\n📊 Confusion Matrix (Test Set):")
        cm = confusion_matrix(y_test, y_pred_test)
        print(f"\n                Predicted")
        print(f"              No Crisis  Crisis")
        print(f"Actual No     {cm[0,0]:>6}    {cm[0,1]:>6}")
        print(f"       Crisis {cm[1,0]:>6}    {cm[1,1]:>6}")

        # Classification report
        print("\n📋 Detailed Classification Report:")
        print(classification_report(y_test, y_pred_test,
                                    target_names=['No Crisis', 'Crisis'],
                                    zero_division=0))

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\n🔍 TOP 5 IMPORTANT FEATURES:")
        print(feature_importance.head().to_string(index=False))

        # Save model
        print("\n💾 Saving crisis prediction model...")
        joblib.dump(model, 'model_crisis_water_shortage.pkl')
        joblib.dump(self.label_encoders, 'crisis_label_encoders.pkl')
        joblib.dump(feature_cols, 'crisis_feature_columns.pkl')

        print("✅ Model saved: model_crisis_water_shortage.pkl")
        print("✅ Encoders saved: crisis_label_encoders.pkl")
        print("✅ Features saved: crisis_feature_columns.pkl")

        self.model = model

        return model, feature_importance, {
            'test_accuracy': test_acc,
            'test_f1': test_f1,
            'test_precision': test_precision,
            'test_recall': test_recall
        }

    def test_predictions(self, df):
        """
        Test crisis predictions with examples
        """
        if df is None or len(df) == 0 or self.model is None:
            print("❌ Cannot test - model not trained")
            return

        print("\n" + "="*70)
        print("🧪 TESTING CRISIS PREDICTIONS")
        print("="*70 + "\n")

        feature_cols = joblib.load('crisis_feature_columns.pkl')

        # Test 5 samples (or less if not enough data)
        n_samples = min(5, len(df))
        test_samples = df.sample(n_samples, random_state=42)

        print("Sample Crisis Predictions:")
        print("-"*70)
        for idx, row in test_samples.iterrows():
            X_sample = row[feature_cols].values.reshape(1, -1)
            prediction = self.model.predict(X_sample)[0]
            probability = self.model.predict_proba(X_sample)[0][1]
            actual = row['crisis_label']

            status = "✅ Correct" if prediction == actual else "❌ Wrong"

            print(f"\n📍 District: {row['district']}")
            print(f"   Date: {row['timestamp'].strftime('%Y-%m-%d')}")
            print(
                f"   Demand: {row['demand_requests']:.0f} | Pending: {row['pending_requests']:.0f}")
            print(f"   Complaints: {row['citizen_complaints']:.0f}")
            print(f"   Actual: {'🚨 CRISIS' if actual else '✅ Normal'}")
            print(
                f"   Predicted: {'🚨 CRISIS' if prediction else '✅ Normal'} ({probability*100:.1f}% prob)")
            print(f"   {status}")

        print("\n" + "="*70)


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏛️  MODEL 2: CRISIS PREDICTION (WATER SHORTAGE)")
    print("="*70)

    trainer = CrisisPredictionModel()

    # Step 1: Load and prepare
    infra_df = trainer.load_and_prepare_infrastructure_data()

    if infra_df is not None and len(infra_df) > 0:
        # Step 2: Train model
        model, importance, metrics = trainer.train_crisis_model(infra_df)

        if model is not None:
            # Step 3: Test predictions
            trainer.test_predictions(infra_df)

            print("\n" + "="*70)
            print("✅ MODEL 2 (CRISIS PREDICTION) - COMPLETE!")
            print("="*70)
            print("\n📊 Final Metrics:")
            print(f"   Test Accuracy: {metrics['test_accuracy']:.3f}")
            print(f"   Test F1 Score: {metrics['test_f1']:.3f}")
            print(f"   Test Precision: {metrics['test_precision']:.3f}")
            print(f"   Test Recall: {metrics['test_recall']:.3f}")
            print("="*70 + "\n")
    else:
        print("❌ Data preparation failed. Check input data.")
