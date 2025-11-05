# feature_engineering_and_training.py (FIXED)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


class MahaGovAI_ModelTrainer:
    """
    Maharashtra Governance AI - Model Training Pipeline
    """

    def __init__(self):
        self.label_encoders = {}
        self.models = {}

    def load_and_prepare_health_data(self):
        """
        Load health data and create features for demand forecasting
        """
        print("\n" + "="*60)
        print("📊 STEP 1: LOADING & FEATURE ENGINEERING")
        print("="*60 + "\n")

        # Load data
        df = pd.read_csv('maharashtra_health_data.csv')
        print(f"✅ Loaded health data: {df.shape}")

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Encode categorical variables
        print("🔧 Encoding categorical features...")
        le_district = LabelEncoder()
        le_service = LabelEncoder()

        df['district_encoded'] = le_district.fit_transform(df['district'])
        df['service_type_encoded'] = le_service.fit_transform(
            df['service_type'])

        self.label_encoders['district'] = le_district
        self.label_encoders['service_type'] = le_service

        # Create lag features (past trends predict future)
        print("🔧 Creating lag features...")
        df = df.sort_values(['district', 'service_type', 'timestamp'])

        # Rolling averages for each district-service combination
        df['demand_lag_7days'] = df.groupby(['district', 'service_type'])['demand_requests'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )

        df['demand_lag_30days'] = df.groupby(['district', 'service_type'])['demand_requests'].transform(
            lambda x: x.rolling(window=30, min_periods=1).mean()
        )

        df['demand_trend'] = df['demand_lag_7days'] - df['demand_lag_30days']

        # Resource utilization rate
        df['resource_utilization_rate'] = df['resource_availability'] / \
            (df['demand_requests'] + 1)

        # Complaint rate
        df['complaint_rate'] = df['citizen_complaints'] / \
            (df['demand_requests'] + 1)

        # Drop NaN values from rolling calculations
        df = df.dropna()

        print(f"✅ Feature engineering complete! Final shape: {df.shape}")
        print(f"\n📋 Available features: {df.columns.tolist()}")

        return df

    def train_demand_forecasting_model(self, df):
        """
        Train XGBoost model for demand forecasting
        Goal: Predict demand_requests for next week
        """
        print("\n" + "="*60)
        print("🚀 STEP 2: TRAINING DEMAND FORECASTING MODEL")
        print("="*60 + "\n")

        # Select features for training
        feature_cols = [
            'district_encoded', 'service_type_encoded',
            'day_of_week', 'month', 'is_weekend', 'is_monsoon',
            'population_factor', 'urban_ratio',
            'demand_lag_7days', 'demand_lag_30days', 'demand_trend',
            'resource_utilization_rate', 'complaint_rate',
            'response_time_minutes'
        ]

        X = df[feature_cols]
        y = df['demand_requests']

        print(f"📊 Training data shape: X={X.shape}, y={y.shape}")

        # Time-series split (80% train, 20% test)
        # Important: Don't shuffle temporal data!
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        print(f"📈 Train: {len(X_train)} samples | Test: {len(X_test)} samples")

        # XGBoost Regressor with optimized hyperparameters
        print("\n🎯 Training XGBoost model...")
        model = xgb.XGBRegressor(
            n_estimators=300,           # More trees for better accuracy
            max_depth=8,                # Deeper trees for complex patterns
            learning_rate=0.05,         # Slower learning for better generalization
            subsample=0.8,              # Use 80% data per tree
            colsample_bytree=0.8,       # Use 80% features per tree
            min_child_weight=3,         # Prevent overfitting
            gamma=0.1,                  # Regularization
            random_state=42,
            n_jobs=-1,                  # Use all CPU cores
            objective='reg:squarederror',
            # FIXED: early_stopping_rounds removed from here
        )

        # Train with early stopping (XGBoost 3.x new API)
        model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=50  # Print every 50 iterations
        )

        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Evaluation metrics
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)

        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)

        train_mape = np.mean(
            np.abs((y_train - y_pred_train) / (y_train + 1))) * 100
        test_mape = np.mean(
            np.abs((y_test - y_pred_test) / (y_test + 1))) * 100

        # Print results
        print("\n" + "="*60)
        print("📈 MODEL PERFORMANCE METRICS")
        print("="*60)
        print(f"\n{'Metric':<20} {'Train':<15} {'Test':<15}")
        print("-"*60)
        print(f"{'MAE':<20} {train_mae:<15.2f} {test_mae:<15.2f}")
        print(f"{'RMSE':<20} {train_rmse:<15.2f} {test_rmse:<15.2f}")
        print(f"{'R² Score':<20} {train_r2:<15.3f} {test_r2:<15.3f}")
        print(f"{'MAPE (%)':<20} {train_mape:<15.2f} {test_mape:<15.2f}")
        print("="*60)

        # Interpretation
        if test_r2 > 0.85:
            print("\n✅ Excellent model performance! R² > 0.85")
        elif test_r2 > 0.75:
            print("\n✅ Good model performance! R² > 0.75")
        else:
            print("\n⚠️  Model needs improvement. Consider more features or data.")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\n🔍 TOP 5 IMPORTANT FEATURES:")
        print(feature_importance.head().to_string(index=False))

        # Save model and encoders
        print("\n💾 Saving model and encoders...")
        joblib.dump(model, 'model_health_demand_forecasting.pkl')
        joblib.dump(self.label_encoders, 'label_encoders.pkl')
        joblib.dump(feature_cols, 'feature_columns.pkl')

        print("✅ Model saved: model_health_demand_forecasting.pkl")
        print("✅ Encoders saved: label_encoders.pkl")
        print("✅ Features saved: feature_columns.pkl")

        self.models['demand_forecasting'] = model

        return model, feature_importance, {
            'train_mae': train_mae, 'test_mae': test_mae,
            'train_r2': train_r2, 'test_r2': test_r2,
            'train_mape': train_mape, 'test_mape': test_mape
        }

    def test_model_predictions(self, df):
        """
        Test model with sample predictions
        """
        print("\n" + "="*60)
        print("🧪 STEP 3: TESTING MODEL PREDICTIONS")
        print("="*60 + "\n")

        model = self.models['demand_forecasting']
        feature_cols = joblib.load('feature_columns.pkl')

        # Test with 5 random samples
        test_samples = df.sample(5, random_state=42)

        print("Sample Predictions:")
        print("-"*60)
        for idx, row in test_samples.iterrows():
            X_sample = row[feature_cols].values.reshape(1, -1)
            prediction = model.predict(X_sample)[0]
            actual = row['demand_requests']
            error_pct = abs(actual - prediction)/actual * \
                100 if actual > 0 else 0

            print(f"\n📍 District: {row['district']}")
            print(f"   Service: {row['service_type']}")
            print(f"   Date: {row['timestamp'].strftime('%Y-%m-%d')}")
            print(f"   Actual Demand: {actual:.0f}")
            print(f"   Predicted Demand: {prediction:.0f}")
            print(
                f"   Error: {abs(actual - prediction):.0f} ({error_pct:.1f}%)")

        print("\n" + "="*60)


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏛️  MAHARASHTRA GOVERNANCE AI - MODEL TRAINING PIPELINE")
    print("="*70)

    trainer = MahaGovAI_ModelTrainer()

    # Step 1: Load and prepare data
    health_df = trainer.load_and_prepare_health_data()

    # Step 2: Train model
    model, importance, metrics = trainer.train_demand_forecasting_model(
        health_df)

    # Step 3: Test predictions
    trainer.test_model_predictions(health_df)

    print("\n" + "="*70)
    print("✅ MODEL 1 (HEALTH DEMAND FORECASTING) - COMPLETE!")
    print("="*70)
    print("\n📊 Final Model Metrics:")
    print(f"   Test R² Score: {metrics['test_r2']:.3f}")
    print(f"   Test MAE: {metrics['test_mae']:.2f}")
    print(f"   Test MAPE: {metrics['test_mape']:.2f}%")
    print("\n📦 Next Steps:")
    print("  1. ✅ Health Demand Forecasting - DONE")
    print("  2. 🔄 Infrastructure Crisis Prediction (Water Shortage)")
    print("  3. 🔄 Priority Scoring Engine")
    print("  4. 🔄 FastAPI Integration")
    print("  5. 🔄 React Dashboard")
    print("="*70 + "\n")
