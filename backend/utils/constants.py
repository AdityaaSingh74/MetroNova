"""
🚇 KMRL System Constants
Central configuration and constants for the train scheduling system
"""

# System Information
SYSTEM_NAME = "KMRL AI Train Scheduling System"
SYSTEM_VERSION = "1.0.0"
SYSTEM_DESCRIPTION = "AI-Driven Train Induction Planning & Scheduling for Kochi Metro Rail Limited"

# KMRL Operational Constants
TRAIN_NAMES = [
    "KRISHNA", "TAPTI", "NILA", "SARAYU", "ARUTH",
    "VAIGAI", "JHANAVI", "DHWANIL", "BHAVANI", "PADMA", 
    "MANDAKINI", "YAMUNA", "PERIYAR", "KABANI", "VAAYU",
    "KAVERI", "SHIRIYA", "PAMPA", "NARMADA", "MAHE",
    "MAARUT", "SABARMATHI", "GODHAVARI", "GANGA", "PAVAN"
]

STATION_NAMES = [
    "Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom",
    "Kalamassery", "Cusat", "Pathadipalam", "Edapally", "Changampuzha Park",
    "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road", 
    "Maharajas", "Ernakulam South", "Kadavanthra", "Elamkulam",
    "Vyttila", "Thaikoodam", "Petta", "SN Junction"
]

# Operational Parameters
DEFAULT_FLEET_SIZE = 25
MAX_FLEET_SIZE = 40
MIN_SERVICE_QUOTA = 13
MAX_SERVICE_QUOTA = 20
MAX_CLEANING_SLOTS = 5
MAX_MAINTENANCE_SLOTS = 8

# Service Patterns
SERVICE_PATTERNS = {
    'PEAK': {
        'hours': [7, 8, 9, 17, 18, 19],
        'frequency_minutes': 4,
        'load_factor_target': 0.85
    },
    'OFF_PEAK': {
        'hours': [10, 11, 12, 13, 14, 15, 16, 20, 21],
        'frequency_minutes': 6,
        'load_factor_target': 0.65
    },
    'NIGHT': {
        'hours': [22, 23, 5, 6],
        'frequency_minutes': 10,
        'load_factor_target': 0.40
    }
}

# Maintenance Thresholds
MAINTENANCE_THRESHOLDS = {
    'BRAKE_WEAR_WARNING': 75.0,
    'BRAKE_WEAR_CRITICAL': 85.0,
    'HVAC_WEAR_WARNING': 80.0,
    'HVAC_WEAR_CRITICAL': 90.0,
    'BATTERY_HEALTH_WARNING': 70.0,
    'BATTERY_HEALTH_CRITICAL': 60.0,
    'MILEAGE_SERVICE_INTERVAL': 45000,
    'MILEAGE_WARNING_INTERVAL': 8000,
    'MAX_OPEN_JOB_CARDS': 3
}

# Fitness Certificate Validity (days)
FITNESS_VALIDITY_PERIODS = {
    'ROLLING_STOCK': 730,    # 2 years
    'SIGNALLING': 1825,      # 5 years  
    'TELECOM': 1460          # 4 years
}

# Optimization Weights
OPTIMIZATION_WEIGHTS = {
    'GENETIC_ALGORITHM': {
        'service_compliance': 0.35,
        'maintenance_urgency': 0.25,
        'mileage_balance': 0.20,
        'operational_efficiency': 0.20
    },
    'MULTI_OBJECTIVE': {
        'fitness_status': 0.25,
        'job_card_status': 0.20, 
        'branding_priority': 0.15,
        'mileage_factors': 0.15,
        'wear_tear': 0.10,
        'operational_status': 0.10,
        'efficiency_factors': 0.05
    }
}

# Delay Categories and Thresholds
DELAY_CATEGORIES = {
    'LOW': {'min': 0, 'max': 5, 'color': '#10b981', 'impact': 'Minimal'},
    'MEDIUM': {'min': 5, 'max': 10, 'color': '#f59e0b', 'impact': 'Moderate'}, 
    'HIGH': {'min': 10, 'max': float('inf'), 'color': '#ef4444', 'impact': 'Severe'}
}

# Weather Impact Factors
WEATHER_IMPACTS = {
    'CLEAR': {'delay_factor': 1.0, 'speed_reduction': 0.0, 'visibility': 1.0},
    'CLOUDY': {'delay_factor': 1.1, 'speed_reduction': 0.05, 'visibility': 0.95},
    'LIGHT_RAIN': {'delay_factor': 1.3, 'speed_reduction': 0.1, 'visibility': 0.8},
    'HEAVY_RAIN': {'delay_factor': 1.8, 'speed_reduction': 0.25, 'visibility': 0.6},
    'FOG': {'delay_factor': 2.2, 'speed_reduction': 0.4, 'visibility': 0.3},
    'STORM': {'delay_factor': 3.0, 'speed_reduction': 0.6, 'visibility': 0.2}
}

# Scoring Parameters
SCORING_PARAMETERS = {
    'FITNESS_CERTIFICATE_SCORE': 35,    # Max points for valid fitness
    'JOB_CARD_CLOSED_SCORE': 15,       # Max points for closed job cards
    'BRANDING_ACTIVE_SCORE': 15,       # Max points for active branding
    'MILEAGE_OPTIMAL_SCORE': 15,       # Max points for optimal mileage
    'WEAR_MINIMAL_SCORE': 10,          # Max points for minimal wear
    'OPERATIONAL_READY_SCORE': 10,     # Max points for operational readiness
    'PERFECT_SCORE': 100                # Maximum possible score
}

# API Configuration
API_CONFIG = {
    'MAX_REQUESTS_PER_MINUTE': 60,
    'REQUEST_TIMEOUT_SECONDS': 30,
    'MAX_PAYLOAD_SIZE_MB': 10,
    'SUPPORTED_FORMATS': ['json', 'csv', 'excel'],
    'DEFAULT_PAGINATION_SIZE': 25,
    'MAX_PAGINATION_SIZE': 100
}

# File Paths
FILE_PATHS = {
    'DATA_DIR': 'data/',
    'SAMPLE_DATA_DIR': 'data/sample_data/',
    'EXPORTS_DIR': 'data/exports/',
    'LOGS_DIR': 'logs/',
    'MODELS_DIR': 'backend/models/saved_models/',
    'TEMP_DIR': 'temp/',
    'BACKUP_DIR': 'backup/'
}

# Database Configuration
DATABASE_CONFIG = {
    'DEFAULT_ENGINE': 'sqlite',
    'SQLITE_PATH': 'data/kmrl_system.db',
    'CONNECTION_POOL_SIZE': 10,
    'CONNECTION_TIMEOUT': 30,
    'BACKUP_FREQUENCY_HOURS': 24
}

# Real-time Update Intervals (seconds)
UPDATE_INTERVALS = {
    'SYSTEM_STATUS': 10,
    'TRAIN_STATUS': 15,
    'DELAY_PREDICTIONS': 30,
    'SCHEDULE_REFRESH': 60,
    'HEALTH_CHECK': 120,
    'PERFORMANCE_METRICS': 300
}

# Error Codes
ERROR_CODES = {
    'DATA_NOT_FOUND': 1001,
    'INVALID_TRAIN_ID': 1002,
    'OPTIMIZATION_FAILED': 2001,
    'MODEL_NOT_TRAINED': 2002,
    'PREDICTION_FAILED': 2003,
    'FILE_OPERATION_ERROR': 3001,
    'DATABASE_ERROR': 3002,
    'API_RATE_LIMIT': 4001,
    'AUTHENTICATION_FAILED': 4002,
    'SYSTEM_OVERLOAD': 5001,
    'MAINTENANCE_MODE': 5002
}

# Success Messages
SUCCESS_MESSAGES = {
    'DATA_GENERATED': 'Train data generated successfully',
    'MODEL_TRAINED': 'Machine learning model trained successfully',
    'OPTIMIZATION_COMPLETE': 'Schedule optimization completed successfully',
    'PREDICTION_COMPLETE': 'Delay prediction completed successfully',
    'SCHEDULE_EXPORTED': 'Schedule exported successfully',
    'SYSTEM_HEALTHY': 'All systems operational'
}

# Notification Types
NOTIFICATION_TYPES = {
    'INFO': {'color': '#06b6d4', 'icon': 'info-circle'},
    'SUCCESS': {'color': '#10b981', 'icon': 'check-circle'},
    'WARNING': {'color': '#f59e0b', 'icon': 'exclamation-triangle'}, 
    'ERROR': {'color': '#ef4444', 'icon': 'times-circle'},
    'DEBUG': {'color': '#64748b', 'icon': 'bug'}
}

# Performance Benchmarks
PERFORMANCE_BENCHMARKS = {
    'DATA_GENERATION_MAX_TIME': 10.0,      # seconds
    'MODEL_TRAINING_MAX_TIME': 60.0,       # seconds
    'GA_OPTIMIZATION_MAX_TIME': 30.0,      # seconds
    'MOO_OPTIMIZATION_MAX_TIME': 15.0,     # seconds
    'PREDICTION_MAX_TIME': 1.0,            # seconds
    'API_RESPONSE_MAX_TIME': 5.0           # seconds
}

# System Health Thresholds
HEALTH_THRESHOLDS = {
    'MEMORY_USAGE_WARNING': 80.0,          # percentage
    'MEMORY_USAGE_CRITICAL': 90.0,         # percentage
    'CPU_USAGE_WARNING': 75.0,             # percentage
    'CPU_USAGE_CRITICAL': 85.0,            # percentage
    'DISK_SPACE_WARNING': 85.0,            # percentage
    'DISK_SPACE_CRITICAL': 95.0,           # percentage
    'RESPONSE_TIME_WARNING': 2.0,          # seconds
    'RESPONSE_TIME_CRITICAL': 5.0          # seconds
}

# Feature Flags
FEATURE_FLAGS = {
    'ENABLE_REAL_TIME_UPDATES': True,
    'ENABLE_DELAY_PREDICTION': True,
    'ENABLE_GENETIC_ALGORITHM': True,
    'ENABLE_MULTI_OBJECTIVE': True,
    'ENABLE_WHAT_IF_ANALYSIS': True,
    'ENABLE_PERFORMANCE_MONITORING': True,
    'ENABLE_AUTO_BACKUP': True,
    'ENABLE_EMAIL_NOTIFICATIONS': False,
    'ENABLE_SMS_ALERTS': False,
    'ENABLE_ADVANCED_ANALYTICS': True
}

# Chart Colors (for consistent UI)
CHART_COLORS = {
    'PRIMARY': '#2563eb',
    'SUCCESS': '#10b981', 
    'WARNING': '#f59e0b',
    'DANGER': '#ef4444',
    'INFO': '#06b6d4',
    'SECONDARY': '#64748b',
    'GRADIENT_1': ['#667eea', '#764ba2'],
    'GRADIENT_2': ['#f093fb', '#f5576c'],
    'GRADIENT_3': ['#4facfe', '#00f2fe']
}

# Export this as a configuration dictionary for easy access
SYSTEM_CONFIG = {
    'system': {
        'name': SYSTEM_NAME,
        'version': SYSTEM_VERSION,
        'description': SYSTEM_DESCRIPTION
    },
    'operations': {
        'fleet_size': DEFAULT_FLEET_SIZE,
        'service_quota': MIN_SERVICE_QUOTA,
        'cleaning_slots': MAX_CLEANING_SLOTS,
        'maintenance_slots': MAX_MAINTENANCE_SLOTS
    },
    'thresholds': MAINTENANCE_THRESHOLDS,
    'weights': OPTIMIZATION_WEIGHTS,
    'paths': FILE_PATHS,
    'updates': UPDATE_INTERVALS,
    'performance': PERFORMANCE_BENCHMARKS,
    'features': FEATURE_FLAGS
}

def get_config(section=None):
    """Get configuration section or entire config"""
    if section:
        return SYSTEM_CONFIG.get(section, {})
    return SYSTEM_CONFIG

def get_train_name_by_index(index):
    """Get train name by index (0-24)"""
    if 0 <= index < len(TRAIN_NAMES):
        return TRAIN_NAMES[index]
    return f"TRAIN_{index+1:03d}"

def get_delay_category(delay_minutes):
    """Categorize delay by minutes"""
    for category, thresholds in DELAY_CATEGORIES.items():
        if thresholds['min'] <= delay_minutes < thresholds['max']:
            return category
    return 'HIGH'

def get_weather_impact(weather_condition):
    """Get weather impact factors"""
    return WEATHER_IMPACTS.get(weather_condition.upper(), WEATHER_IMPACTS['CLEAR'])

def is_peak_hour(hour):
    """Check if given hour is peak time"""
    return hour in SERVICE_PATTERNS['PEAK']['hours']

def get_service_pattern(hour):
    """Get service pattern for given hour"""
    if hour in SERVICE_PATTERNS['PEAK']['hours']:
        return 'PEAK'
    elif hour in SERVICE_PATTERNS['NIGHT']['hours']:
        return 'NIGHT'
    else:
        return 'OFF_PEAK'

# Print configuration summary when imported
if __name__ == "__main__":
    print(f"🚇 {SYSTEM_NAME} v{SYSTEM_VERSION}")
    print("="*60)
    print(f"Fleet Size: {DEFAULT_FLEET_SIZE} trains")
    print(f"Service Quota: {MIN_SERVICE_QUOTA}-{MAX_SERVICE_QUOTA}")
    print(f"Stations: {len(STATION_NAMES)}")
    print(f"Features Enabled: {sum(FEATURE_FLAGS.values())}/{len(FEATURE_FLAGS)}")
    print("✅ System constants loaded successfully")