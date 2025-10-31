"""
🚇 KMRL API Routes
RESTful API endpoints for train scheduling operations
"""

from flask import Blueprint, request, jsonify
import json
from datetime import datetime

# Create API blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/current-schedule', methods=['GET'])
def get_current_schedule():
    """Get current schedule (placeholder)"""
    return jsonify({
        'status': 'success',
        'schedule': [],
        'message': 'No schedule available. Run optimization first.'
    })

@api_bp.route('/docs', methods=['GET'])
def api_documentation():
    """API documentation endpoint"""
    docs = {
        'title': 'KMRL Train Scheduling API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/generate-data': 'Generate mock train data',
            'POST /api/train-model': 'Train ML models',
            'POST /api/predict-delays': 'Predict train delays',
            'POST /api/optimize-schedule': 'Optimize train schedule',
            'POST /api/whatif-analysis': 'Run what-if scenarios',
            'GET /api/system-status': 'Get system status',
            'GET /api/download-schedule': 'Download schedule CSV',
            'GET /api/health': 'Health check',
            'GET /api/current-schedule': 'Get current schedule'
        }
    }
    
    return jsonify(docs)