
import time
from flask import request, jsonify
from orchestrator import run_full_schedule_optimization
from logger import system_logger as logger
"""
backend/app.py

Minimal Flask app exposing /optimize endpoint with SocketIO support for real-time features.
"""
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from backend.optimization.optimization_run import run_optimization
from backend.orchestrator import run_full_schedule_optimization
import os

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/optimize", methods=["POST"])
def optimize():
    payload = request.json or {}
    trainsets = payload.get("trainsets_csv", "data/trainsets.csv")
    jobcards = payload.get("jobcards_csv")
    model = payload.get("model_path")
    min_peak = int(payload.get("min_peak", 18))
    res = run_optimization(trainset_csv=trainsets, jobcards_csv=jobcards, model_path=model, min_peak_trainsets=min_peak)
    details = res.get("details")
    if hasattr(details, "to_dict"):
        details = details.to_dict(orient="records")
    return jsonify({
        "status": res.get("pulp_status"),
        "objective": res.get("objective_value"),
        "selected_trainsets": res.get("selected_trainsets"),
        "details": details
    })

# Add these imports at the top of app.py

# Add this route to your existing Flask app
@app.route('/api/run_schedule', methods=['POST'])
def run_schedule():
    """
    Main API endpoint to run full train scheduling optimization
    """
    start_time = time.time()
    
    try:
        # 1) Parse JSON input from request
        data = request.get_json() or {}
        train_csv = data.get('train_csv')
        jobcards_csv = data.get('jobcards_csv')
        ml_model_path = data.get('ml_model_path')
        constraints = data.get('constraints', {
            'min_service': 13,
            'max_maintenance': 8,
            'weights': {
                'service_readiness': 0.40,
                'punctuality_protection': 0.25,
                'maintenance_cost': 0.15,
                'revenue_protection': 0.12,
                'efficiency': 0.08
            }
        })
        scenario = data.get('scenario')

        logger.info(f"API /run_schedule called with constraints: {constraints}")

        # 2) Run the main orchestration
        final_schedule, whatif_analysis = run_full_schedule_optimization(
            train_csv_path=train_csv,
            jobcards_csv_path=jobcards_csv,
            ml_model_path=ml_model_path,
            constraints=constraints,
            scenario_config=scenario
        )

        # 3) Calculate summary statistics
        duration = time.time() - start_time
        
        summary_stats = {
            'total_trains': len(final_schedule),
            'service_trains': len(final_schedule[final_schedule['final_operational_status'] == 'service']),
            'standby_trains': len(final_schedule[final_schedule['final_operational_status'] == 'standby']),
            'maintenance_trains': len(final_schedule[final_schedule['final_operational_status'] == 'maintenance']),
            'avg_delay_minutes': final_schedule['predicted_delay_minutes'].mean(),
            'avg_readiness_score': final_schedule['readiness_score'].mean(),
            'avg_moo_score': final_schedule['moo_score'].mean(),
            'fitness_compliance_percent': (final_schedule['RollingStockFitnessStatus'].sum() / len(final_schedule)) * 100
        }

        # 4) Prepare schedule data for frontend
        schedule_data = final_schedule[[
            'TrainID', 'final_operational_status', 'predicted_delay_minutes', 
            'readiness_score', 'moo_score', 'RollingStockFitnessStatus',
            'BrakepadWear%', 'HVACWear%', 'OpenJobCards', 'TotalMileageKM'
        ]].to_dict(orient='records')

        logger.info(f"Schedule API completed successfully in {duration:.2f}s")

        # 5) Return comprehensive JSON response
        return jsonify({
            "status": "success",
            "message": f"Schedule optimization completed for {summary_stats['total_trains']} trains",
            "duration_seconds": round(duration, 2),
            "summary": summary_stats,
            "schedule": schedule_data,
            "whatif_analysis": whatif_analysis,
            "optimization_method": "Ensemble (GA + MOO + PuLP)",
            "timestamp": final_schedule.iloc[0]['optimization_timestamp'] if len(final_schedule) > 0 else None
        }), 200

    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"Schedule optimization failed: {str(e)}"
        logger.error(error_msg)
        
        return jsonify({
            "status": "error",
            "message": error_msg,
            "duration_seconds": round(duration, 2),
            "error_type": type(e).__name__
        }), 500


@app.route('/api/schedule_status', methods=['GET'])
def get_schedule_status():
    """
    Get current schedule status and basic metrics
    """
    try:
        # Check if optimized schedule exists
        schedule_file = 'outputs/final_optimized_schedule.csv'
        
        if os.path.exists(schedule_file):
            df = pd.read_csv(schedule_file)
            
            status_data = {
                'schedule_available': True,
                'last_optimization': df.iloc[0]['optimization_timestamp'] if 'optimization_timestamp' in df.columns else None,
                'total_trains': len(df),
                'service_trains': len(df[df['final_operational_status'] == 'service']),
                'standby_trains': len(df[df['final_operational_status'] == 'standby']),
                'maintenance_trains': len(df[df['final_operational_status'] == 'maintenance']),
                'avg_delay': df['predicted_delay_minutes'].mean() if 'predicted_delay_minutes' in df.columns else 0,
                'optimization_method': df.iloc[0]['optimization_method'] if 'optimization_method' in df.columns else 'Unknown'
            }
        else:
            status_data = {
                'schedule_available': False,
                'message': 'No optimized schedule available. Run /api/run_schedule first.'
            }
        
        return jsonify(status_data), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'schedule_available': False
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)

