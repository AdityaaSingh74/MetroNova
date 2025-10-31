"""
🚇 KMRL System Logger
Centralized logging configuration for the train scheduling system
"""

import logging
import logging.handlers
import os
from datetime import datetime
import sys
from pathlib import Path

def setup_logger(name='kmrl_system', level=logging.INFO):
    """Setup centralized logging for KMRL system"""
    
    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler - Main log (rotating, 10MB max, keep 5 files)
    main_log_file = log_dir / 'kmrl_system.log'
    file_handler = logging.handlers.RotatingFileHandler(
        main_log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error log file (ERROR and above)
    error_log_file = log_dir / 'kmrl_errors.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Performance log for optimization timing
    perf_log_file = log_dir / 'kmrl_performance.log'
    perf_handler = logging.handlers.RotatingFileHandler(
        perf_log_file,
        maxBytes=5*1024*1024,
        backupCount=3
    )
    perf_handler.setLevel(logging.INFO)
    perf_handler.setFormatter(detailed_formatter)
    
    # Add filter for performance logs
    class PerformanceFilter(logging.Filter):
        def filter(self, record):
            return 'PERF' in record.getMessage()
    
    perf_handler.addFilter(PerformanceFilter())
    logger.addHandler(perf_handler)
    
    return logger

def log_performance(logger, operation, duration, details=None):
    """Log performance metrics"""
    details_str = f" | {details}" if details else ""
    logger.info(f"PERF | {operation} | {duration:.3f}s{details_str}")

def log_optimization_result(logger, algorithm, trains_count, score, duration):
    """Log optimization results"""
    logger.info(f"OPTIMIZATION | {algorithm} | {trains_count} trains | Score: {score:.2f} | {duration:.3f}s")

def log_api_request(logger, endpoint, method, status_code, duration):
    """Log API requests"""
    logger.info(f"API | {method} {endpoint} | {status_code} | {duration:.3f}s")

def log_system_health(logger, metrics):
    """Log system health metrics"""
    logger.info(f"HEALTH | Active: {metrics.get('active_trains', 0)} | "
               f"Standby: {metrics.get('standby_trains', 0)} | "
               f"Maintenance: {metrics.get('maintenance_trains', 0)} | "
               f"Avg Delay: {metrics.get('avg_delay', 0):.1f}min")

# Create global logger instance
system_logger = setup_logger()

if __name__ == "__main__":
    # Test the logger
    test_logger = setup_logger('test_logger')
    
    test_logger.debug("Debug message - should appear in file only")
    test_logger.info("Info message - should appear in console and file")
    test_logger.warning("Warning message")
    test_logger.error("Error message - should appear in error log too")
    
    # Test performance logging
    log_performance(test_logger, "Genetic Algorithm", 2.345, "25 trains optimized")
    log_optimization_result(test_logger, "MOO", 25, 85.67, 1.234)
    
    print("✅ Logger test complete. Check logs/ directory for output files.")