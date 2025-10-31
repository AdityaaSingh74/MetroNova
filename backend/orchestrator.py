# Enhanced Orchestrator with All Best Models
"""
🚇 KMRL Complete AI Pipeline - Best of All Worlds
Integrates the top models from all your files
"""

import pandas as pd
import numpy as np
import time
import os
from datetime import datetime
from backend.models.ai_model import SmartMetroAI
from backend.models.delay_prediction_model import DelayPredictor
from backend.optimization.optimization_run import run_optimization
from backend.optimization.optimization import MetroOptimizer

# Train Names
TRAIN_NAMES = [
    "KRISHNA", "TAPTI", "NILA", "SARAYU", "ARUTH",
    "VAIGAI", "JHANAVI", "DHWANIL", "BHAVANI", "PADMA",
    "MANDAKINI", "YAMUNA", "PERIYAR", "KABANI", "VAAYU",
    "KAVERI", "SHIRIYA", "PAMPA", "NARMADA", "MAHE",
    "MAARUT", "SABARMATHI", "GODHAVARI", "GANGA", "PAVAN"
]

class KMRLMasterOrchestrator:
    def __init__(self):
        self.smart_ai = SmartMetroAI()
        self.delay_predictor = DelayPredictor()
        self.metro_optimizer = MetroOptimizer()
        
    def generate_comprehensive_data(self):
        """Generate realistic KMRL data"""
        np.random.seed(42)
        
        # Generate train data
        train_data = []
        for i, train_name in enumerate(TRAIN_NAMES):
            train_entry = {
                'train_id': train_name,
                'TrainID': train_name,
                'trainset_id': train_name,
                
                # Operational Parameters
                'dwell_time_seconds': np.random.randint(45, 90),
                'distance_km': np.random.uniform(2.5, 15.0),
                'scheduled_load_factor': np.random.uniform(0.4, 0.95),
                'time_of_day': np.random.randint(6, 22),
                'passenger_density': np.random.uniform(0.2, 0.9),
                'route_complexity': np.random.uniform(0.8, 2.0),
                'passenger_load': np.random.randint(100, 400),
                'route': np.random.choice(['Red Line', 'Blue Line', 'Green Line']),
                
                # Certificate & Fitness Status
                'certificate_valid': np.random.choice([0, 1], p=[0.15, 0.85]),
                'cert_days_left_rolling_stock': np.random.randint(10, 365),
                'cert_days_left_signalling': np.random.randint(100, 1825),
                'cert_days_left_telecom': np.random.randint(150, 1460),
                'RollingStockFitnessStatus': np.random.choice([True, False], p=[0.88, 0.12]),
                
                # Maintenance Data
                'mileage_km': np.random.randint(15000, 45000),
                'TotalMileageKM': np.random.randint(15000, 45000),
                'critical_jobs_open': np.random.choice([0, 1, 2], p=[0.75, 0.20, 0.05]),
                'mechanical_score': np.random.uniform(0.6, 0.95),
                'energy_consumption': np.random.uniform(60, 95),
                'last_maintenance': (datetime.now() - pd.Timedelta(days=np.random.randint(0, 120))).strftime('%Y-%m-%d'),
                
                # Operational Status  
                'status': np.random.choice(['Active', 'Standby', 'Maintenance'], p=[0.5, 0.35, 0.15]),
                'location': np.random.choice(['Muttom', 'Kalamassery'], p=[0.6, 0.4]),
                'readiness_score': np.random.uniform(0.7, 0.98),
                
                # Time-based features
                'scheduled_departure': (datetime.now() + pd.Timedelta(hours=np.random.randint(1, 24))).strftime('%Y-%m-%d %H:%M'),
                'weather_condition': np.random.choice(['clear', 'cloudy', 'rainy'], p=[0.6, 0.3, 0.1]),
                
                # Branding & Revenue
                'brand_hours_remaining': np.random.randint(0, 8),
                'crew_id': f'CREW_{np.random.randint(1, 50):03d}' if np.random.random() > 0.1 else None,
            }
            train_data.append(train_entry)
        
        return pd.DataFrame(train_data)
    
    def run_master_optimization(self, constraints=None, scenario=None):
        """Run complete AI-powered optimization pipeline"""
        start_time = time.time()
        print("🚇 KMRL Master AI Pipeline Starting...")
        print("=" * 60)
        
        try:
            # Step 1: Generate Data
            print("📊 Step 1/5: Generating comprehensive train data...")
            train_df = self.generate_comprehensive_data()
            
            # Create schedules data for AI training
            schedules_df = train_df.copy()
            schedules_df['delay_minutes'] = np.random.exponential(2.5, len(train_df))  # Realistic delay distribution
            
            # Create maintenance data
            maintenance_df = train_df[train_df['status'] == 'Maintenance'].copy()
            
            print(f"   ✅ Generated data for {len(train_df)} trains")
            
            # Step 2: Train Smart AI Models
            print("\n🧠 Step 2/5: Training Advanced AI Models...")
            self.smart_ai.train_models(schedules_df, train_df, maintenance_df)
            print(f"   ✅ AI Models Performance: {self.smart_ai.get_model_performance()}")
            
            # Step 3: Enhanced Delay Prediction
            print("\n⏱️ Step 3/5: Running Enhanced Delay Prediction...")
            self.delay_predictor.train_model(df=train_df)
            
            delays = []
            for _, row in train_df.iterrows():
                prediction = self.delay_predictor.predict_schedule(
                    dwell_time=row.get('dwell_time_seconds', 60),
                    distance=row.get('distance_km', 8.5),
                    load_factor=row.get('scheduled_load_factor', 0.7),
                    time_of_day=row.get('time_of_day', 12),
                    passenger_density=row.get('passenger_density', 0.5),
                    route_complexity=row.get('route_complexity', 1.0)
                )
                delay_value = prediction.get('Predicted Delay Minutes', 0) if isinstance(prediction, dict) else 0
                delays.append(max(0, delay_value))
            
            train_df['predicted_delay_minutes'] = delays
            train_df['delay_category'] = [self.delay_predictor.categorize_delay(x) for x in delays]
            print(f"   ✅ Average predicted delay: {np.mean(delays):.2f} minutes")
            
            # Step 4: AI-Based Readiness Assessment
            print("\n🔧 Step 4/5: AI-Powered Readiness Assessment...")
            readiness_scores = []
            maintenance_predictions = []
            
            for _, row in train_df.iterrows():
                # Use SmartMetroAI for readiness calculation
                readiness = self.smart_ai.calculate_train_readiness(row.to_dict())
                readiness_scores.append(readiness)
                
                # Get maintenance prediction
                maint_pred = self.smart_ai.predict_maintenance(row.to_dict())
                maintenance_predictions.append(maint_pred)
            
            train_df['ai_readiness_score'] = readiness_scores
            train_df['maintenance_recommendation'] = [pred['action'] for pred in maintenance_predictions]
            print(f"   ✅ Average AI readiness score: {np.mean(readiness_scores):.3f}")
            
            # Step 5: Multi-Level Optimization
            print("\n🎯 Step 5/5: Multi-Level Optimization...")
            
            # Save data for optimizers
            os.makedirs('temp_data', exist_ok=True)
            train_csv_path = 'temp_data/trains.csv' 
            train_df.to_csv(train_csv_path, index=False)
            
            # A) PuLP Constraint Optimization
            print("   🔧 Running PuLP constraint optimization...")
            pulp_result = run_optimization(
                trainset_csv=train_csv_path,
                jobcards_csv=None,
                min_peak_trainsets=constraints.get('min_service', 13) if constraints else 13
            )
            
            # B) OR-Tools Advanced Scheduling 
            print("   ⚙️ Running OR-Tools scheduling optimization...")
            routes = ['Red Line', 'Blue Line', 'Green Line']
            or_tools_result = self.metro_optimizer.optimize_schedule(
                trains=train_df, 
                routes=routes,
                constraints=constraints
            )
            
            # C) AI Emergency Response (if scenario provided)
            emergency_response = None
            if scenario:
                print(f"   🚨 Running emergency response for: {scenario.get('type', 'unknown')}")
                available_trains = train_df[train_df['status'] == 'Standby']
                emergency_response = self.smart_ai.emergency_response(
                    scenario_type=scenario.get('type', 'high_demand'),
                    affected_trains=scenario.get('affected_trains', ['KRISHNA']),
                    affected_routes=['Red Line'],
                    available_trains=available_trains
                )
            
            # Step 6: Ensemble Final Decision
            print("\n🎭 Creating Ensemble Final Schedule...")
            final_schedule = train_df.copy()
            
            # Combine all optimization results
            final_schedule['pulp_selected'] = 0
            if pulp_result and 'details' in pulp_result:
                pulp_details = pulp_result['details']
                for idx, train_id in enumerate(final_schedule['trainset_id']):
                    if train_id in pulp_details['trainset_id'].values:
                        selected = pulp_details[pulp_details['trainset_id'] == train_id]['selected_for_induction'].iloc[0] if len(pulp_details[pulp_details['trainset_id'] == train_id]) > 0 else 0
                        final_schedule.loc[idx, 'pulp_selected'] = selected
            
            # OR-Tools scheduling assignments
            final_schedule['or_tools_assigned'] = 0
            if or_tools_result and 'assignments' in or_tools_result:
                assigned_trains = list(or_tools_result['assignments'].keys())
                final_schedule['or_tools_assigned'] = final_schedule['train_id'].isin(assigned_trains).astype(int)
            
            # Final operational status using ensemble logic
            final_schedule['final_operational_status'] = 'standby'
            
            for idx, row in final_schedule.iterrows():
                votes = []
                
                # AI readiness vote
                if row['ai_readiness_score'] > 0.8:
                    votes.append('service')
                elif row['ai_readiness_score'] < 0.5:
                    votes.append('maintenance')
                
                # PuLP optimization vote
                if row['pulp_selected'] == 1:
                    votes.append('service')
                
                # OR-Tools vote
                if row['or_tools_assigned'] == 1:
                    votes.append('service')
                
                # Maintenance override
                if (not row['RollingStockFitnessStatus'] or 
                    row['critical_jobs_open'] > 0 or
                    row['maintenance_recommendation'] == 'Schedule Maintenance'):
                    final_status = 'maintenance'
                elif votes.count('service') >= 2:  # Majority vote
                    final_status = 'service'
                elif 'service' in votes or row['ai_readiness_score'] > 0.7:
                    final_status = 'standby'
                else:
                    final_status = 'maintenance'
                
                final_schedule.loc[idx, 'final_operational_status'] = final_status
            
            # Ensure minimum service requirement
            service_count = len(final_schedule[final_schedule['final_operational_status'] == 'service'])
            min_service = constraints.get('min_service', 13) if constraints else 13
            
            if service_count < min_service:
                standby_candidates = final_schedule[
                    final_schedule['final_operational_status'] == 'standby'
                ].nlargest(min_service - service_count, 'ai_readiness_score')
                final_schedule.loc[standby_candidates.index, 'final_operational_status'] = 'service'
            
            # Add metadata
            duration = time.time() - start_time
            final_schedule['optimization_timestamp'] = datetime.now().isoformat()
            final_schedule['optimization_method'] = 'AI Master Pipeline (SmartAI + DelayPredictor + PuLP + OR-Tools)'
            final_schedule['pipeline_duration'] = duration
            
            # Calculate comprehensive metrics
            summary = {
                'total_trains': len(final_schedule),
                'service_trains': len(final_schedule[final_schedule['final_operational_status'] == 'service']),
                'standby_trains': len(final_schedule[final_schedule['final_operational_status'] == 'standby']),
                'maintenance_trains': len(final_schedule[final_schedule['final_operational_status'] == 'maintenance']),
                'avg_delay_minutes': final_schedule['predicted_delay_minutes'].mean(),
                'avg_ai_readiness': final_schedule['ai_readiness_score'].mean(),
                'fitness_compliance': (final_schedule['RollingStockFitnessStatus'].sum() / len(final_schedule)) * 100,
                'optimization_duration': duration,
                'ai_model_performance': self.smart_ai.get_model_performance(),
                'pulp_status': pulp_result.get('pulp_status', 'N/A') if pulp_result else 'Failed',
                'or_tools_metrics': or_tools_result.get('performance_metrics', {}) if or_tools_result else {}
            }
            
            print("\n🎯 MASTER OPTIMIZATION COMPLETE!")
            print("=" * 60)
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"🚇  Service Trains: {summary['service_trains']}")
            print(f"⏸️  Standby Trains: {summary['standby_trains']}")
            print(f"🔧  Maintenance Trains: {summary['maintenance_trains']}")
            print(f"⏰  Avg Delay: {summary['avg_delay_minutes']:.2f} min")
            print(f"✅  Avg AI Readiness: {summary['avg_ai_readiness']:.3f}")
            print(f"📋  Fitness Compliance: {summary['fitness_compliance']:.1f}%")
            
            # Save results
            os.makedirs('outputs', exist_ok=True)
            final_schedule.to_csv('outputs/master_optimized_schedule.csv', index=False)
            
            return final_schedule, summary, emergency_response
            
        except Exception as e:
            print(f"❌ Master Optimization Error: {str(e)}")
            # Return fallback schedule
            fallback = self.generate_comprehensive_data()
            fallback['final_operational_status'] = 'standby'
            fallback.loc[:12, 'final_operational_status'] = 'service'
            fallback.loc[20:, 'final_operational_status'] = 'maintenance'
            return fallback, {'error': str(e)}, None

# Test the master orchestrator
if __name__ == "__main__":
    print("🧪 Testing KMRL Master AI Orchestrator")
    print("=" * 60)
    
    orchestrator = KMRLMasterOrchestrator()
    
    final_schedule, summary, emergency = orchestrator.run_master_optimization(
        constraints={'min_service': 13, 'max_maintenance': 8},
        scenario={'type': 'train_breakdown', 'affected_trains': ['KRISHNA']}
    )
    
    print(f"\n📊 Final Schedule Shape: {final_schedule.shape}")
    print("\n🚇 Operational Status Distribution:")
    print(final_schedule['final_operational_status'].value_counts())
    
    print(f"\n📈 Sample Results:")
    cols = ['TrainID', 'final_operational_status', 'ai_readiness_score', 'predicted_delay_minutes', 'maintenance_recommendation']
    print(final_schedule[cols].head(10))
    
    if emergency:
        print(f"\n🚨 Emergency Response: {emergency['scenario']}")
        print(f"   Backup Trains: {len(emergency['backup_trains'])}")
        print(f"   Actions: {len(emergency['immediate_actions'])}")
    
    print("\n✅ Master Orchestrator Test Complete!")