import time


@app.route('/api/run_schedule', methods=['POST'])
def run_schedule():
    """Enhanced API endpoint with master orchestrator"""
    start_time = time.time()
    
    try:
        data = request.get_json() or {}
        constraints = data.get('constraints', {
            'min_service': 13,
            'max_maintenance': 8
        })
        scenario = data.get('scenario')

        # Call master orchestrator
        orchestrator = KMRLMasterOrchestrator()
        final_schedule, summary, emergency = orchestrator.run_master_optimization(
            constraints=constraints,
            scenario=scenario
        )

        duration = time.time() - start_time
        
        # Prepare response data
        schedule_data = final_schedule[[
            'TrainID', 'final_operational_status', 'predicted_delay_minutes', 
            'ai_readiness_score', 'maintenance_recommendation',
            'RollingStockFitnessStatus'
        ]].to_dict(orient='records')

        return jsonify({
            "status": "success",
            "message": f"Master AI optimization completed for {summary['total_trains']} trains",
            "duration_seconds": round(duration, 2),
            "summary": summary,
            "schedule": schedule_data,
            "emergency_response": emergency,
            "optimization_method": "Master AI Pipeline (SmartAI + DelayPredictor + PuLP + OR-Tools)",
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"Master optimization failed: {str(e)}"
        
        return jsonify({
            "status": "error", 
            "message": error_msg,
            "duration_seconds": round(duration, 2),
            "error_type": type(e).__name__
        }), 500
