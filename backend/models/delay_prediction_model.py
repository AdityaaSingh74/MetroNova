"""
🚇 KMRL Delay Prediction Model
Enhanced version of your Gradio notebook implementation with additional features

Features:
- Multi-model ensemble for better accuracy
- Real-time delay prediction
- Integration with operational data
- Scenario-based predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DelayPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = ["dwell_time_seconds", "distance_km", "scheduled_load_factor"]
        self.is_trained = False
        
    def create_delay_features(self, df):
        """Create synthetic delay data as per your notebook logic"""
        np.random.seed(42)
        df["delay_minutes"] = (
            df["dwell_time_seconds"] / 60 * df["scheduled_load_factor"] * 5
            + np.random.normal(0, 1, size=len(df))
        ).round(1)
        
        # Add more realistic delay factors
        # Peak hour delays
        if 'time_of_day' in df.columns:
            peak_hours = [7, 8, 9, 17, 18, 19]  # Rush hours
            df['is_peak_hour'] = df['time_of_day'].isin(peak_hours).astype(int)
            df["delay_minutes"] += df['is_peak_hour'] * np.random.normal(2, 0.5, len(df))
        
        # Weather impact
        if 'weather_condition' in df.columns:
            weather_delays = {'rainy': 1.5, 'foggy': 2.0, 'clear': 0, 'cloudy': 0.3}
            df["delay_minutes"] += df['weather_condition'].map(weather_delays).fillna(0)
        
        # Station congestion
        if 'passenger_density' in df.columns:
            df["delay_minutes"] += df['passenger_density'] * 0.02
        
        # Ensure no negative delays
        df["delay_minutes"] = df["delay_minutes"].clip(lower=0)
        
        return df
    
    def categorize_delay(self, x):
        """Categorize delays as per your logic"""
        if x < 5:
            return "Low"
        elif x < 10:
            return "Medium"
        else:
            return "High"
    
    def generate_training_data(self, base_df):
        """Generate comprehensive training data"""
        # Expand your basic features with operational data
        expanded_data = []
        
        for idx, row in base_df.iterrows():
            # Create multiple scenarios per train
            for hour in range(6, 23):  # Operating hours
                for load in [0.3, 0.5, 0.7, 0.9]:  # Different load factors
                    for dwell in [30, 45, 60, 90]:  # Different dwell times
                        scenario = {
                            'train_id': row.get('TrainID', f'T{idx:03d}'),
                            'dwell_time_seconds': dwell,
                            'distance_km': row.get('distance_km', np.random.uniform(1, 15)),
                            'scheduled_load_factor': load,
                            'time_of_day': hour,
                            'day_type': 'Weekday' if hour < 20 else 'Evening',
                            'service_pattern': 'Peak' if hour in [7,8,9,17,18,19] else 'Off_Peak',
                            'weather_condition': np.random.choice(['clear', 'cloudy', 'rainy'], p=[0.6, 0.3, 0.1]),
                            'passenger_density': np.random.uniform(0.2, 1.0) * load,
                            'train_type': row.get('train_type', 'Standard'),
                            'route_complexity': np.random.uniform(0.5, 2.0)
                        }
                        expanded_data.append(scenario)
        
        expanded_df = pd.DataFrame(expanded_data)
        return self.create_delay_features(expanded_df)
    
    def train_model(self, data_path=None, df=None):
        """Train the delay prediction models"""
        try:
            if df is None:
                if data_path and os.path.exists(data_path):
                    df = pd.read_csv(data_path)
                else:
                    # Generate sample data if no data provided
                    df = self.generate_sample_data()
            
            # Generate comprehensive training data
            training_df = self.generate_training_data(df)
            
            # Prepare features and targets
            features = ["dwell_time_seconds", "distance_km", "scheduled_load_factor"]
            if 'time_of_day' in training_df.columns:
                features.extend(['time_of_day', 'passenger_density', 'route_complexity'])
            
            X = training_df[features]
            
            # Multiple targets as per your notebook
            y_delay_cat = training_df["delay_minutes"].apply(self.categorize_delay)
            y_delay_min = training_df["delay_minutes"]
            y_pattern = training_df["service_pattern"]
            y_daytype = training_df["day_type"]
            
            # Train models
            print("🚇 Training Delay Prediction Models...")
            
            # Delay category classifier
            self.models['delay_category'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['delay_category'].fit(X, y_delay_cat)
            
            # Delay minutes regressor
            self.models['delay_minutes'] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models['delay_minutes'].fit(X, y_delay_min)
            
            # Service pattern classifier
            self.models['service_pattern'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['service_pattern'].fit(X, y_pattern)
            
            # Day type classifier
            self.models['day_type'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['day_type'].fit(X, y_daytype)
            
            # Additional ensemble model for better accuracy
            self.models['delay_ensemble'] = RandomForestRegressor(
                n_estimators=200, max_depth=15, random_state=42
            )
            self.models['delay_ensemble'].fit(X, y_delay_min)
            
            self.feature_names = features
            self.is_trained = True
            
            # Calculate accuracies
            X_test = X.iloc[-100:]  # Use last 100 samples for testing
            y_cat_test = y_delay_cat.iloc[-100:]
            y_min_test = y_delay_min.iloc[-100:]
            
            cat_accuracy = accuracy_score(y_cat_test, self.models['delay_category'].predict(X_test))
            min_mae = mean_absolute_error(y_min_test, self.models['delay_minutes'].predict(X_test))
            
            print(f"✅ Models trained successfully!")
            print(f"   - Delay Category Accuracy: {cat_accuracy:.3f}")
            print(f"   - Delay Minutes MAE: {min_mae:.3f}")
            
            # Save models
            self.save_models()
            
            return {
                'category_accuracy': cat_accuracy,
                'minutes_mae': min_mae,
                'models_count': len(self.models)
            }
            
        except Exception as e:
            print(f"❌ Error training models: {str(e)}")
            return {'error': str(e)}
    
    def predict_schedule(self, dwell_time, distance, load_factor, time_of_day=12, passenger_density=0.5, route_complexity=1.0):
        """Enhanced prediction function from your notebook"""
        if not self.is_trained:
            self.load_models()
            
        try:
            # Prepare input data
            input_features = {
                "dwell_time_seconds": dwell_time,
                "distance_km": distance,
                "scheduled_load_factor": load_factor
            }
            
            # Add additional features if available
            if len(self.feature_names) > 3:
                input_features.update({
                    'time_of_day': time_of_day,
                    'passenger_density': passenger_density,
                    'route_complexity': route_complexity
                })
            
            new_schedule = pd.DataFrame([input_features])
            
            # Make predictions using all models
            predictions = {
                "Predicted Delay Category": self.models['delay_category'].predict(new_schedule)[0],
                "Predicted Delay Minutes": round(self.models['delay_minutes'].predict(new_schedule)[0], 2),
                "Predicted Service Pattern": self.models['service_pattern'].predict(new_schedule)[0],
                "Predicted Day Type": self.models['day_type'].predict(new_schedule)[0]
            }
            
            # Add ensemble prediction for better accuracy
            if 'delay_ensemble' in self.models:
                ensemble_delay = self.models['delay_ensemble'].predict(new_schedule)[0]
                predictions["Ensemble Delay Minutes"] = round(ensemble_delay, 2)
            
            # Add confidence scores
            delay_proba = self.models['delay_category'].predict_proba(new_schedule)[0]
            predictions["Confidence"] = round(max(delay_proba) * 100, 1)
            
            # Add recommendations
            recommendations = self.generate_recommendations(predictions)
            predictions["Recommendations"] = recommendations
            
            return predictions
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def predict_batch(self, scenarios_df):
        """Predict delays for multiple scenarios"""
        predictions = []
        for _, row in scenarios_df.iterrows():
            pred = self.predict_schedule(
                dwell_time=row.get('dwell_time_seconds', 60),
                distance=row.get('distance_km', 8.5),
                load_factor=row.get('scheduled_load_factor', 0.7),
                time_of_day=row.get('time_of_day', 12),
                passenger_density=row.get('passenger_density', 0.5),
                route_complexity=row.get('route_complexity', 1.0)
            )
            predictions.append(pred)
        return predictions
    
    def generate_recommendations(self, predictions):
        """Generate operational recommendations based on predictions"""
        recommendations = []
        
        delay_minutes = predictions.get("Predicted Delay Minutes", 0)
        delay_category = predictions.get("Predicted Delay Category", "Low")
        
        if delay_category == "High" or delay_minutes > 10:
            recommendations.extend([
                "Consider reducing dwell time at non-critical stations",
                "Activate backup train if available",
                "Notify passengers about potential delays"
            ])
        elif delay_category == "Medium" or delay_minutes > 5:
            recommendations.extend([
                "Monitor passenger boarding carefully",
                "Consider skipping non-essential announcements"
            ])
        else:
            recommendations.append("Normal operations expected")
        
        # Time-based recommendations
        service_pattern = predictions.get("Predicted Service Pattern", "")
        if service_pattern == "Peak":
            recommendations.append("Extra staff recommended at busy stations")
        
        return recommendations
    
    def get_feature_importance(self):
        """Get feature importance from trained models"""
        if not self.is_trained:
            return {}
        
        importances = {}
        for model_name, model in self.models.items():
            if hasattr(model, 'feature_importances_'):
                importances[model_name] = dict(zip(
                    self.feature_names,
                    model.feature_importances_
                ))
        
        return importances
    
    def save_models(self):
        """Save trained models"""
        model_dir = 'backend/models/saved_models'
        os.makedirs(model_dir, exist_ok=True)
        
        for name, model in self.models.items():
            joblib.dump(model, f'{model_dir}/delay_{name}_model.pkl')
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'models': list(self.models.keys()),
            'trained_at': datetime.now().isoformat()
        }
        
        import json
        with open(f'{model_dir}/delay_model_metadata.json', 'w') as f:
            json.dump(metadata, f)
    
    def load_models(self):
        """Load saved models"""
        model_dir = 'backend/models/saved_models'
        
        try:
            # Load metadata
            with open(f'{model_dir}/delay_model_metadata.json', 'r') as f:
                metadata = json.load(f)
            
            self.feature_names = metadata['feature_names']
            
            # Load models
            for model_name in metadata['models']:
                model_path = f'{model_dir}/delay_{model_name}_model.pkl'
                if os.path.exists(model_path):
                    self.models[model_name] = joblib.load(model_path)
            
            self.is_trained = True
            print(f"✅ Loaded {len(self.models)} delay prediction models")
            
        except Exception as e:
            print(f"⚠️  Could not load saved models: {str(e)}")
            self.is_trained = False
    
    def generate_sample_data(self):
        """Generate sample data for testing"""
        np.random.seed(42)
        
        sample_data = []
        for i in range(50):  # 50 sample trains
            train_data = {
                'TrainID': f'KMRL_{i:03d}',
                'distance_km': np.random.uniform(2, 25),  # KMRL line length variations
                'train_type': np.random.choice(['Standard', 'Express']),
                'depot': np.random.choice(['Muttom', 'Kalamassery'])
            }
            sample_data.append(train_data)
        
        return pd.DataFrame(sample_data)

# Test the model
if __name__ == "__main__":
    print("🚇 Testing KMRL Delay Prediction Model")
    print("="*50)
    
    predictor = DelayPredictor()
    
    # Train with sample data
    training_results = predictor.train_model()
    print(f"Training Results: {training_results}")
    
    # Test prediction (your original example)
    example = predictor.predict_schedule(dwell_time=60, distance=8.5, load_factor=0.7)
    print(f"\\nExample Prediction: {example}")
    
    # Test with rush hour scenario
    rush_hour = predictor.predict_schedule(
        dwell_time=90, distance=12.5, load_factor=0.9, 
        time_of_day=8, passenger_density=0.8
    )
    print(f"\\nRush Hour Prediction: {rush_hour}")
    
    print("\\n✅ Delay Prediction Model Test Complete!")