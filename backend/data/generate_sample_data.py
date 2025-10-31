# Sample Data Generator for Testing
"""
Use this script to create sample data files for testing your integration
Run: python generate_sample_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data directory
os.makedirs('data', exist_ok=True)

# KMRL Train Names
TRAIN_NAMES = [
    "KRISHNA", "TAPTI", "NILA", "SARAYU", "ARUTH",
    "VAIGAI", "JHANAVI", "DHWANIL", "BHAVANI", "PADMA",
    "MANDAKINI", "YAMUNA", "PERIYAR", "KABANI", "VAAYU",
    "KAVERI", "SHIRIYA", "PAMPA", "NARMADA", "MAHE",
    "MAARUT", "SABARMATHI", "GODHAVARI", "GANGA", "PAVAN"
]

def generate_trainsets_data():
    """Generate comprehensive trainset data"""
    np.random.seed(42)
    
    data = []
    for i, train_name in enumerate(TRAIN_NAMES):
        entry = {
            'trainset_id': train_name,
            'TrainID': train_name,
            'train_id': train_name,
            
            # Operational Parameters
            'dwell_time_seconds': np.random.randint(45, 90),
            'distance_km': np.random.uniform(2.5, 15.0),
            'scheduled_load_factor': np.random.uniform(0.4, 0.95),
            'time_of_day': np.random.randint(6, 22),
            'passenger_density': np.random.uniform(0.2, 0.9),
            'route_complexity': np.random.uniform(0.8, 2.0),
            
            # Fitness Certificates
            'certificate_valid': np.random.choice([0, 1], p=[0.15, 0.85]),
            'cert_days_left_rolling_stock': np.random.randint(10, 365),
            'cert_days_left_signalling': np.random.randint(100, 1825),
            'cert_days_left_telecom': np.random.randint(150, 1460),
            
            # Status Flags
            'RollingStockFitnessStatus': np.random.choice([True, False], p=[0.88, 0.12]),
            'SignallingFitnessStatus': np.random.choice([True, False], p=[0.92, 0.08]),
            'TelecomFitnessStatus': np.random.choice([True, False], p=[0.90, 0.10]),
            
            # Maintenance Data
            'mileage_km': np.random.randint(15000, 45000),
            'TotalMileageKM': np.random.randint(15000, 45000),
            'MileageSinceLastServiceKM': np.random.randint(1000, 8000),
            'BrakepadWear%': np.random.uniform(15, 90),
            'HVACWear%': np.random.uniform(10, 85),
            'DoorSystemWear%': np.random.uniform(5, 75),
            'battery_health': np.random.uniform(65, 95),
            
            # Job Cards
            'OpenJobCards': np.random.poisson(1.2),
            'critical_jobs_open': np.random.choice([0, 1, 2], p=[0.75, 0.20, 0.05]),
            'JobCardStatus': np.random.choice(['close', 'open'], p=[0.72, 0.28]),
            
            # Location and Logistics
            'location': np.random.choice(['Muttom', 'Kalamassery'], p=[0.65, 0.35]),
            'Depot': np.random.choice(['Muttom', 'Kalamassery'], p=[0.65, 0.35]),
            'BayPositionID': np.random.randint(1, 25),
            'stabling_capacity': np.random.randint(3, 8),
            'ShuntingMovesRequired': np.random.poisson(1.8),
            'shunting_score': np.random.uniform(0.4, 1.0),
            
            # Branding and Revenue
            'BrandingActive': np.random.choice([True, False], p=[0.32, 0.68]),
            'branding_hours_today': np.random.uniform(0, 7),
            'branding_min_hours': np.random.uniform(3, 8),
            'ExposureHoursTarget': np.random.choice([260, 280, 300, 320]),
            'ExposureHoursAccrued': np.random.randint(40, 280),
            
            # Operational Status
            'OperationalStatus': np.random.choice(['service', 'standby', 'maintenance'], p=[0.50, 0.35, 0.15]),
            'CleaningRequired': np.random.choice([True, False], p=[0.28, 0.72]),
            'ReliabilityScore': np.random.uniform(0.75, 0.98),
            'MileageBalanceVariance': np.random.normal(0, 1200),
            
            # Environmental
            'weather_condition': np.random.choice(['clear', 'cloudy', 'rainy'], p=[0.65, 0.25, 0.10]),
            'is_peak_hour': np.random.choice([0, 1], p=[0.68, 0.32]),
        }
        data.append(entry)
    
    df = pd.DataFrame(data)
    df.to_csv('data/trainsets.csv', index=False)
    print(f"✅ Generated trainsets.csv with {len(df)} records")
    return df

def generate_jobcards_data():
    """Generate job cards data"""
    np.random.seed(123)
    
    data = []
    job_id = 1
    
    for train_name in TRAIN_NAMES:
        # Each train has 0-4 job cards
        num_jobs = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.35, 0.2, 0.1, 0.05])
        
        for j in range(num_jobs):
            entry = {
                'job_id': f'JOB_{job_id:04d}',
                'train_id': train_name,
                'trainset_id': train_name,
                'TrainID': train_name,
                'priority': np.random.choice(['low', 'medium', 'high', 'critical'], p=[0.4, 0.35, 0.20, 0.05]),
                'priority_level': np.random.randint(1, 5),
                'status': np.random.choice(['open', 'in_progress', 'closed'], p=[0.25, 0.15, 0.60]),
                'job_type': np.random.choice(['preventive', 'corrective', 'emergency'], p=[0.5, 0.4, 0.1]),
                'created_date': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
                'estimated_hours': np.random.randint(1, 12),
                'is_critical': np.random.choice([0, 1], p=[0.85, 0.15]),
                'component': np.random.choice(['brakes', 'hvac', 'doors', 'electrical', 'signaling'], p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                'description': f'Maintenance work on {train_name}'
            }
            data.append(entry)
            job_id += 1
    
    df = pd.DataFrame(data)
    df.to_csv('data/jobcards.csv', index=False)
    print(f"✅ Generated jobcards.csv with {len(df)} records")
    return df

def generate_depot_capacities():
    """Generate depot capacity data"""
    data = [
        {'location': 'Muttom', 'capacity': 18, 'current_occupancy': 15},
        {'location': 'Kalamassery', 'capacity': 12, 'current_occupancy': 10}
    ]
    
    df = pd.DataFrame(data)
    df.to_csv('data/depot_capacities.csv', index=False)
    print(f"✅ Generated depot_capacities.csv with {len(df)} records")
    return df

def generate_schedule_history():
    """Generate historical schedule data for reference"""
    np.random.seed(200)
    
    data = []
    for i in range(100):  # 100 historical records
        entry = {
            'date': (datetime.now() - timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d'),
            'train_id': np.random.choice(TRAIN_NAMES),
            'scheduled_departure': f"{np.random.randint(5, 23):02d}:{np.random.randint(0, 59):02d}",
            'actual_departure': f"{np.random.randint(5, 23):02d}:{np.random.randint(0, 59):02d}",
            'delay_minutes': np.random.exponential(2.5),
            'passenger_load': np.random.uniform(0.3, 0.95),
            'weather': np.random.choice(['clear', 'cloudy', 'rain', 'fog'], p=[0.6, 0.25, 0.10, 0.05]),
            'route': f"Route_{np.random.randint(1, 6)}",
            'incident_reported': np.random.choice([0, 1], p=[0.85, 0.15])
        }
        data.append(entry)
    
    df = pd.DataFrame(data)
    df.to_csv('data/schedule_history.csv', index=False)
    print(f"✅ Generated schedule_history.csv with {len(df)} records")
    return df

if __name__ == "__main__":
    print("🚇 Generating KMRL Sample Data...")
    print("=" * 50)
    
    # Generate all data files
    trainsets_df = generate_trainsets_data()
    jobcards_df = generate_jobcards_data()
    depot_df = generate_depot_capacities()
    history_df = generate_schedule_history()
    
    print("=" * 50)
    print("✅ All sample data generated successfully!")
    print(f"📁 Files created in 'data/' directory:")
    print("   - trainsets.csv (25 trains)")
    print("   - jobcards.csv (job maintenance records)")
    print("   - depot_capacities.csv (depot info)")
    print("   - schedule_history.csv (historical data)")
    print("\n🚀 Ready to run optimization!")
    print("   python orchestrator.py  # Test orchestrator")
    print("   python run.py          # Start Flask app")