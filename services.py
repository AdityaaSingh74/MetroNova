"""
🚇 KMRL SERVICE LAYER - BUSINESS LOGIC ORCHESTRATION
Separates business logic from API routes for better modularity
"""

from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from logger import KMRLLogger

class TrainReadinessService:
    """Service layer for train readiness operations"""
    
    def __init__(self, readiness_model):
        self.readiness_model = readiness_model
        self.logger = KMRLLogger()
    
    def assess_single_train(self, train_data: Dict) -> Dict:
        """Assess readiness for a single train"""
        try:
            result = self.readiness_model.predict_readiness(train_data)
            
            # Add business logic
            result['deployment_recommendation'] = self._get_deployment_recommendation(result)
            result['maintenance_urgency'] = self._calculate_maintenance_urgency(train_data, result)
            
            self.logger.info(f"Train readiness assessed: {train_data.get('TrainID')} - Score: {result.get('readiness_score')}")
            return result
            
        except Exception as e:
            self.logger.error(f"Train readiness assessment failed: {str(e)}")
            return {'error': str(e)}
    
    def assess_fleet(self, trains_data: List[Dict]) -> Dict:
        """Assess readiness for entire fleet"""
        try:
            assessments = []
            for train in trains_data:
                assessment = self.assess_single_train(train)
                assessments.append(assessment)
            
            # Fleet-level analytics
            fleet_analytics = self._calculate_fleet_analytics(assessments)
            
            return {
                'success': True,
                'individual_assessments': assessments,
                'fleet_analytics': fleet_analytics,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Fleet readiness assessment failed: {str(e)}")
            return {'error': str(e)}
    
    def _get_deployment_recommendation(self, readiness_result: Dict) -> str:
        """Business logic for deployment recommendations"""
        if not readiness_result.get('operational_ready', True):
            return 'DO_NOT_DEPLOY'
        elif readiness_result.get('readiness_score', 0) > 85:
            return 'IMMEDIATE_DEPLOYMENT'
        elif readiness_result.get('readiness_score', 0) > 70:
            return 'STANDBY_READY'
        else:
            return 'REQUIRES_ATTENTION'
    
    def _calculate_maintenance_urgency(self, train_data: Dict, readiness_result: Dict) -> str:
        """Calculate maintenance urgency with business rules"""
        priority = readiness_result.get('maintenance_priority', 'Low')
        
        # Apply business rules
        if train_data.get('open_jobs', 0) >= 3:
            return 'CRITICAL'
        elif train_data.get('brake_wear', 0) > 85:
            return 'URGENT'
        elif priority == 'High':
            return 'HIGH'
        elif priority == 'Medium':
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_fleet_analytics(self, assessments: List[Dict]) -> Dict:
        """Calculate fleet-level analytics"""
        total_trains = len(assessments)
        if total_trains == 0:
            return {}
        
        ready_trains = sum(1 for a in assessments if a.get('operational_ready', False))
        avg_readiness = np.mean([a.get('readiness_score', 0) for a in assessments])
        
        priority_distribution = {}
        for assessment in assessments:
            priority = assessment.get('maintenance_priority', 'Unknown')
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
        
        return {
            'total_trains': total_trains,
            'operational_ready_count': ready_trains,
            'operational_ready_percentage': round((ready_trains / total_trains) * 100, 1),
            'average_readiness_score': round(avg_readiness, 2),
            'maintenance_priority_distribution': priority_distribution,
            'fleet_health_grade': self._get_fleet_health_grade(avg_readiness)
        }
    
    def _get_fleet_health_grade(self, avg_readiness: float) -> str:
        """Grade fleet health based on average readiness"""
        if avg_readiness >= 90:
            return 'EXCELLENT'
        elif avg_readiness >= 80:
            return 'GOOD'
        elif avg_readiness >= 70:
            return 'FAIR'
        elif avg_readiness >= 60:
            return 'POOR'
        else:
            return 'CRITICAL'


class DelayPredictionService:
    """Service layer for delay prediction operations"""
    
    def __init__(self, delay_predictor):
        self.delay_predictor = delay_predictor
        self.logger = KMRLLogger()
    
    def predict_single_delay(self, prediction_input: Dict) -> Dict:
        """Predict delay for single scenario"""
        try:
            # Validate and enrich input
            enriched_input = self._enrich_prediction_input(prediction_input)
            
            result = self.delay_predictor.predict_delay(enriched_input)
            
            # Add business intelligence
            result['delay_impact_assessment'] = self._assess_delay_impact(result)
            result['mitigation_suggestions'] = self._get_mitigation_suggestions(result)
            
            self.logger.info(f"Delay prediction completed - Predicted: {result.get('predicted_delay_minutes')} minutes")
            return result
            
        except Exception as e:
            self.logger.error(f"Delay prediction failed: {str(e)}")
            return {'error': str(e)}
    
    def predict_batch_delays(self, scenarios: List[Dict]) -> Dict:
        """Predict delays for multiple scenarios"""
        try:
            predictions = []
            for scenario in scenarios:
                prediction = self.predict_single_delay(scenario)
                predictions.append(prediction)
            
            # Batch analytics
            batch_analytics = self._calculate_batch_analytics(predictions)
            
            return {
                'success': True,
                'predictions': predictions,
                'batch_analytics': batch_analytics,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Batch delay prediction failed: {str(e)}")
            return {'error': str(e)}
    
    def _enrich_prediction_input(self, input_data: Dict) -> Dict:
        """Enrich prediction input with derived features"""
        enriched = input_data.copy()
        
        # Add time-based features if missing
        if 'time_of_day' not in enriched:
            enriched['time_of_day'] = datetime.now().hour
        
        if 'day_of_week' not in enriched:
            enriched['day_of_week'] = datetime.now().weekday()
        
        if 'is_peak_hour' not in enriched:
            enriched['is_peak_hour'] = enriched['time_of_day'] in [7, 8, 9, 17, 18, 19]
        
        if 'passenger_density' not in enriched:
            enriched['passenger_density'] = enriched.get('scheduled_load_factor', 0.7) * 1.2
        
        return enriched
    
    def _assess_delay_impact(self, prediction_result: Dict) -> Dict:
        """Assess the business impact of predicted delay"""
        delay_minutes = prediction_result.get('predicted_delay_minutes', 0)
        delay_category = prediction_result.get('delay_category', 'Low')
        
        if delay_minutes < 2:
            impact_level = 'MINIMAL'
            passenger_impact = 'LOW'
        elif delay_minutes < 5:
            impact_level = 'LOW'
            passenger_impact = 'MODERATE'
        elif delay_minutes < 10:
            impact_level = 'MODERATE'
            passenger_impact = 'HIGH'
        else:
            impact_level = 'HIGH'
            passenger_impact = 'SEVERE'
        
        return {
            'impact_level': impact_level,
            'passenger_impact': passenger_impact,
            'service_disruption_risk': delay_category,
            'recommended_action': self._get_delay_action_recommendation(delay_minutes)
        }
    
    def _get_delay_action_recommendation(self, delay_minutes: float) -> str:
        """Get action recommendation based on delay"""
        if delay_minutes < 2:
            return 'MONITOR'
        elif delay_minutes < 5:
            return 'NOTIFY_PASSENGERS'
        elif delay_minutes < 10:
            return 'ADJUST_SCHEDULE'
        else:
            return 'DEPLOY_BACKUP_TRAIN'
    
    def _get_mitigation_suggestions(self, prediction_result: Dict) -> List[str]:
        """Get mitigation suggestions based on prediction"""
        suggestions = []
        delay_minutes = prediction_result.get('predicted_delay_minutes', 0)
        confidence = prediction_result.get('confidence_score', 0)
        
        if delay_minutes > 5:
            suggestions.append("Consider reducing dwell time at stations")
            suggestions.append("Implement priority signaling")
        
        if delay_minutes > 10:
            suggestions.append("Deploy backup train if available")
            suggestions.append("Announce delays to passengers")
        
        if confidence < 70:
            suggestions.append("Monitor situation closely - prediction uncertainty high")
        
        return suggestions
    
    def _calculate_batch_analytics(self, predictions: List[Dict]) -> Dict:
        """Calculate analytics for batch predictions"""
        if not predictions:
            return {}
        
        successful_predictions = [p for p in predictions if 'error' not in p]
        
        if not successful_predictions:
            return {'error': 'No successful predictions in batch'}
        
        delays = [p.get('predicted_delay_minutes', 0) for p in successful_predictions]
        
        return {
            'total_scenarios': len(predictions),
            'successful_predictions': len(successful_predictions),
            'average_predicted_delay': round(np.mean(delays), 2),
            'max_predicted_delay': round(max(delays), 2),
            'min_predicted_delay': round(min(delays), 2),
            'high_delay_scenarios': sum(1 for d in delays if d > 10),
            'delay_distribution': {
                'low': sum(1 for d in delays if d < 5),
                'medium': sum(1 for d in delays if 5 <= d < 10),
                'high': sum(1 for d in delays if d >= 10)
            }
        }


class OptimizationService:
    """Service layer for optimization operations"""
    
    def __init__(self, genetic_optimizer, moo_optimizer):
        self.genetic_optimizer = genetic_optimizer
        self.moo_optimizer = moo_optimizer
        self.logger = KMRLLogger()
    
    def run_genetic_optimization(self, config: Dict) -> Dict:
        """Run genetic algorithm optimization with business logic"""
        try:
            # Apply business constraints
            business_config = self._apply_business_constraints(config)
            
            result = self.genetic_optimizer.optimize(
                population_size=business_config.get('population_size', 100),
                generations=business_config.get('generations', 50),
                constraints=business_config.get('constraints')
            )
            
            if 'error' not in result:
                # Add business analysis
                result['business_analysis'] = self._analyze_optimization_result(result, 'genetic')
                self.logger.info("Genetic optimization completed successfully")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Genetic optimization service error: {str(e)}")
            return {'error': str(e)}
    
    def run_moo_optimization(self, config: Dict) -> Dict:
        """Run multi-objective optimization with business logic"""
        try:
            business_config = self._apply_business_constraints(config)
            
            result = self.moo_optimizer.optimize(
                data_path=business_config.get('data_path'),
                constraints=business_config.get('constraints')
            )
            
            if 'error' not in result:
                result['business_analysis'] = self._analyze_optimization_result(result, 'moo')
                self.logger.info("MOO optimization completed successfully")
            
            return result
            
        except Exception as e:
            self.logger.error(f"MOO optimization service error: {str(e)}")
            return {'error': str(e)}
    
    def _apply_business_constraints(self, config: Dict) -> Dict:
        """Apply KMRL-specific business constraints"""
        business_config = config.copy()
        
        # Ensure minimum service levels
        constraints = business_config.get('constraints', {})
        constraints.update({
            'min_service_trains': max(constraints.get('min_service_trains', 12), 12),
            'max_maintenance_concurrent': min(constraints.get('max_maintenance_concurrent', 6), 8),
            'emergency_reserve_minimum': max(constraints.get('emergency_reserve_minimum', 2), 2)
        })
        
        business_config['constraints'] = constraints
        return business_config
    
    def _analyze_optimization_result(self, result: Dict, optimization_type: str) -> Dict:
        """Analyze optimization results from business perspective"""
        try:
            summary = result.get('summary_statistics', {})
            
            analysis = {
                'optimization_type': optimization_type,
                'service_adequacy': self._assess_service_adequacy(summary),
                'efficiency_score': self._calculate_efficiency_score(summary),
                'risk_assessment': self._assess_operational_risk(summary),
                'business_kpis': self._calculate_business_kpis(summary)
            }
            
            return analysis
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _assess_service_adequacy(self, summary: Dict) -> Dict:
        """Assess if optimization meets service requirements"""
        service_trains = summary.get('service_trains', 0)
        
        if service_trains >= 15:
            adequacy = 'EXCELLENT'
        elif service_trains >= 12:
            adequacy = 'ADEQUATE'
        elif service_trains >= 10:
            adequacy = 'MARGINAL'
        else:
            adequacy = 'INADEQUATE'
        
        return {
            'level': adequacy,
            'service_trains': service_trains,
            'meets_minimum': service_trains >= 12
        }
    
    def _calculate_efficiency_score(self, summary: Dict) -> float:
        """Calculate operational efficiency score"""
        service_trains = summary.get('service_trains', 0)
        total_trains = summary.get('total_trains', 25)
        avg_readiness = summary.get('avg_readiness_score', 70)
        
        utilization_score = (service_trains / total_trains) * 100
        efficiency_score = (utilization_score * 0.6) + (avg_readiness * 0.4)
        
        return round(efficiency_score, 2)
    
    def _assess_operational_risk(self, summary: Dict) -> Dict:
        """Assess operational risks from optimization result"""
        service_trains = summary.get('service_trains', 0)
        maintenance_trains = summary.get('maintenance_trains', 0)
        
        risks = []
        risk_level = 'LOW'
        
        if service_trains < 12:
            risks.append('Service capacity below minimum requirement')
            risk_level = 'HIGH'
        
        if maintenance_trains > 8:
            risks.append('Too many trains in maintenance simultaneously')
            risk_level = 'MEDIUM' if risk_level == 'LOW' else risk_level
        
        if service_trains + maintenance_trains > 23:
            risks.append('Insufficient emergency reserve')
            risk_level = 'MEDIUM' if risk_level == 'LOW' else risk_level
        
        return {
            'level': risk_level,
            'identified_risks': risks,
            'risk_count': len(risks)
        }
    
    def _calculate_business_kpis(self, summary: Dict) -> Dict:
        """Calculate key business performance indicators"""
        return {
            'fleet_utilization_percentage': round((summary.get('service_trains', 0) / 25) * 100, 1),
            'maintenance_efficiency': round((summary.get('maintenance_trains', 0) / 8) * 100, 1),
            'operational_readiness': round(summary.get('avg_readiness_score', 70), 1),
            'service_reliability_score': min(100, summary.get('service_trains', 0) * 6.67)  # Max at 15 trains
        }


class SimulationService:
    """Service layer for what-if simulation operations"""
    
    def __init__(self, whatif_simulator):
        self.whatif_simulator = whatif_simulator
        self.logger = KMRLLogger()
    
    def run_simulation(self, base_data, scenario_config: Dict) -> Dict:
        """Run simulation with business context"""
        try:
            # Validate scenario configuration
            validated_config = self._validate_scenario_config(scenario_config)
            
            result = self.whatif_simulator.run_scenario(base_data, validated_config)
            
            if 'error' not in result:
                # Add business insights
                result['business_insights'] = self._generate_business_insights(result)
                result['action_plan'] = self._generate_action_plan(result)
                
                self.logger.info(f"Simulation completed: {validated_config.get('type')}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Simulation service error: {str(e)}")
            return {'error': str(e)}
    
    def _validate_scenario_config(self, config: Dict) -> Dict:
        """Validate and enrich scenario configuration"""
        validated = config.copy()
        
        # Ensure required fields
        if 'type' not in validated:
            validated['type'] = 'train_failure'
        
        # Add business context
        validated['business_context'] = {
            'simulation_time': datetime.now().isoformat(),
            'stakeholder_impact': self._assess_stakeholder_impact(validated),
            'priority_level': self._determine_priority_level(validated)
        }
        
        return validated
    
    def _assess_stakeholder_impact(self, config: Dict) -> Dict:
        """Assess impact on different stakeholders"""
        scenario_type = config.get('type', 'unknown')
        
        impact_matrix = {
            'train_failure': {
                'passengers': 'HIGH',
                'operations': 'HIGH',
                'maintenance': 'MEDIUM',
                'management': 'HIGH'
            },
            'weather_impact': {
                'passengers': 'MEDIUM',
                'operations': 'HIGH',
                'maintenance': 'LOW',
                'management': 'MEDIUM'
            },
            'peak_demand': {
                'passengers': 'HIGH',
                'operations': 'HIGH',
                'maintenance': 'LOW',
                'management': 'MEDIUM'
            }
        }
        
        return impact_matrix.get(scenario_type, {
            'passengers': 'MEDIUM',
            'operations': 'MEDIUM',
            'maintenance': 'MEDIUM',
            'management': 'MEDIUM'
        })
    
    def _determine_priority_level(self, config: Dict) -> str:
        """Determine simulation priority level"""
        scenario_type = config.get('type', 'unknown')
        severity = config.get('severity', 'medium')
        
        if scenario_type in ['train_failure', 'emergency_situation'] and severity in ['high', 'critical']:
            return 'CRITICAL'
        elif scenario_type in ['weather_impact', 'peak_demand'] and severity == 'high':
            return 'HIGH'
        elif severity == 'medium':
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_business_insights(self, simulation_result: Dict) -> Dict:
        """Generate business insights from simulation results"""
        try:
            impact_analysis = simulation_result.get('impact_analysis', {})
            
            insights = {
                'financial_impact_summary': self._summarize_financial_impact(impact_analysis),
                'operational_implications': self._analyze_operational_implications(simulation_result),
                'passenger_experience_impact': self._assess_passenger_impact(impact_analysis),
                'strategic_recommendations': self._generate_strategic_recommendations(simulation_result)
            }
            
            return insights
            
        except Exception as e:
            return {'error': f'Insight generation failed: {str(e)}'}
    
    def _summarize_financial_impact(self, impact_analysis: Dict) -> Dict:
        """Summarize financial implications"""
        financial = impact_analysis.get('financial_impact', {})
        
        return {
            'revenue_loss': financial.get('estimated_revenue_loss', 0),
            'operational_cost_increase': financial.get('operational_cost_increase', 0),
            'total_impact': financial.get('total_financial_impact', 0),
            'impact_severity': 'HIGH' if financial.get('total_financial_impact', 0) > 100000 else 'MEDIUM' if financial.get('total_financial_impact', 0) > 50000 else 'LOW'
        }
    
    def _analyze_operational_implications(self, simulation_result: Dict) -> List[str]:
        """Analyze operational implications"""
        implications = []
        
        scenario_type = simulation_result.get('scenario_type', 'unknown')
        impact_analysis = simulation_result.get('impact_analysis', {})
        
        service_change = impact_analysis.get('operational_impact', {}).get('service_trains_change', 0)
        
        if service_change < -3:
            implications.append("Significant service reduction requiring immediate backup deployment")
        elif service_change < 0:
            implications.append("Service capacity reduced - monitor passenger satisfaction")
        
        if scenario_type == 'weather_impact':
            implications.append("Weather protocols should be activated")
            implications.append("Increased maintenance monitoring required post-event")
        
        return implications
    
    def _assess_passenger_impact(self, impact_analysis: Dict) -> Dict:
        """Assess passenger experience impact"""
        passenger_impact = impact_analysis.get('passenger_impact', {})
        
        return {
            'affected_passengers': passenger_impact.get('affected_passengers_estimate', 0),
            'average_delay_per_passenger': passenger_impact.get('average_delay_per_passenger', 0),
            'impact_score': passenger_impact.get('impact_score', 0),
            'satisfaction_impact': 'HIGH' if passenger_impact.get('impact_score', 0) > 70 else 'MEDIUM' if passenger_impact.get('impact_score', 0) > 40 else 'LOW'
        }
    
    def _generate_strategic_recommendations(self, simulation_result: Dict) -> List[str]:
        """Generate strategic business recommendations"""
        recommendations = []
        
        recovery_strategies = simulation_result.get('recovery_strategies', {})
        scenario_type = simulation_result.get('scenario_type', 'unknown')
        
        recommendations.extend(recovery_strategies.get('immediate_actions', [])[:3])
        
        # Add strategic recommendations based on scenario
        if scenario_type == 'train_failure':
            recommendations.append("Invest in predictive maintenance systems")
            recommendations.append("Review spare parts inventory management")
        elif scenario_type == 'weather_impact':
            recommendations.append("Develop enhanced weather monitoring capabilities")
            recommendations.append("Create weather-specific operational protocols")
        
        return recommendations
    
    def _generate_action_plan(self, simulation_result: Dict) -> Dict:
        """Generate structured action plan"""
        recovery_strategies = simulation_result.get('recovery_strategies', {})
        
        return {
            'immediate_actions': recovery_strategies.get('immediate_actions', [])[:3],
            'short_term_recovery': recovery_strategies.get('short_term_recovery', [])[:3],
            'long_term_improvements': recovery_strategies.get('long_term_improvements', [])[:3],
            'resource_requirements': recovery_strategies.get('resource_allocation', []),
            'timeline': {
                'immediate': '0-1 hours',
                'short_term': '1-24 hours',
                'long_term': '1 week - 1 month'
            }
        }


class DataService:
    """Service layer for data management operations"""
    
    def __init__(self):
        self.logger = KMRLLogger()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def generate_train_data(self, readiness_model) -> List[Dict]:
        """Generate comprehensive train data using ML models"""
        try:
            cache_key = 'train_data'
            
            # Check cache
            if self._is_cached(cache_key):
                self.logger.info("Returning cached train data")
                return self.cache[cache_key]['data']
            
            # Generate new data
            train_df = readiness_model.generate_realistic_train_data(num_trains=25)
            
            trains_list = []
            for _, row in train_df.iterrows():
                train_data = self._build_train_record(row, readiness_model)
                trains_list.append(train_data)
            
            # Cache the results
            self._cache_data(cache_key, trains_list)
            
            self.logger.info(f"Generated fresh train data for {len(trains_list)} trains")
            return trains_list
            
        except Exception as e:
            self.logger.error(f"Train data generation failed: {str(e)}")
            return []
    
    def _build_train_record(self, row, readiness_model) -> Dict:
        """Build comprehensive train record"""
        # Get ML predictions
        readiness_result = readiness_model.predict_readiness(row.to_dict())
        
        # Build complete record
        train_data = {
            'train_id': row['TrainID'],
            'train_number': f"T{len(self.cache.get('train_data', {}).get('data', [])) + 1:03d}",
            'depot': row['Depot'],
            'current_location': self._get_random_station(),
            
            # ML-derived status
            'status': self._determine_status_from_readiness(readiness_result),
            'readiness_score': readiness_result.get('readiness_score', 50),
            'maintenance_priority': readiness_result.get('maintenance_priority', 'Low'),
            'operational_ready': readiness_result.get('operational_ready', True),
            'recommendations': readiness_result.get('recommendations', []),
            
            # Component data
            'brake_wear': row['BrakepadWear%'],
            'hvac_wear': row['HVACWear%'],
            'battery_health': row['BatteryHealth%'],
            'open_jobs': row['OpenJobCards'],
            'total_mileage': row['TotalMileageKM'],
            'service_mileage': row['MileageSinceLastServiceKM'],
            'branding_active': row['BrandingActive'],
            'cleaning_required': row['CleaningRequired'],
            
            # Fitness status
            'fitness_rolling': row['RollingStockFitnessStatus'],
            'fitness_signalling': row['SignallingFitnessStatus'],
            'fitness_telecom': row['TelecomFitnessStatus'],
            
            # Business metrics
            'deployment_priority': self._calculate_deployment_priority(readiness_result),
            'emergency_deployable': readiness_result.get('operational_ready', True) and row['BrakepadWear%'] < 85,
            
            # Timestamps
            'last_updated': datetime.now().isoformat(),
            'data_freshness': 'FRESH'
        }
        
        return train_data
    
    def _determine_status_from_readiness(self, readiness_result: Dict) -> str:
        """Determine status from readiness assessment"""
        if not readiness_result.get('operational_ready', True):
            return 'maintenance'
        elif readiness_result.get('maintenance_priority') == 'Critical':
            return 'maintenance'
        elif readiness_result.get('maintenance_priority') == 'High':
            return 'inspection'
        elif readiness_result.get('readiness_score', 50) > 85:
            return 'service'
        elif readiness_result.get('readiness_score', 50) > 70:
            return 'standby'
        else:
            return 'cleaning'
    
    def _calculate_deployment_priority(self, readiness_result: Dict) -> int:
        """Calculate deployment priority score"""
        base_score = readiness_result.get('readiness_score', 50)
        
        if readiness_result.get('maintenance_priority') == 'Low':
            base_score += 10
        elif readiness_result.get('maintenance_priority') == 'Critical':
            base_score -= 30
        
        return max(0, min(100, int(base_score)))
    
    def _get_random_station(self) -> str:
        """Get random KMRL station"""
        stations = [
            'Aluva', 'Kalamassery', 'Cusat', 'Edapally', 'Changampuzha Park',
            'Palarivattom', 'JLN Stadium', 'Kaloor', 'MG Road', 'Maharajas',
            'Ernakulam South', 'Kadavanthra', 'Petta', 'Thripunithura'
        ]
        return np.random.choice(stations)
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is cached and not expired"""
        if key not in self.cache:
            return False
        
        cache_entry = self.cache[key]
        cache_age = datetime.now().timestamp() - cache_entry['timestamp']
        
        return cache_age < self.cache_ttl
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now().timestamp()
        }
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.logger.info("Data cache cleared")
    
    def get_system_status(self, system_manager) -> Dict:
        """Get comprehensive system status"""
        try:
            # Model status
            delay_model_status = 'trained' if system_manager.delay_predictor.is_trained else 'not_trained'
            readiness_model_status = 'trained' if system_manager.readiness_model.is_trained else 'not_trained'
            
            # Data freshness
            train_data_age = 'fresh' if self._is_cached('train_data') else 'stale'
            
            # Train statistics
            trains_data = system_manager.trains_data or []
            status_counts = {}
            for train in trains_data:
                status = train.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                'success': True,
                'system_health': 'healthy',
                'total_trains': len(trains_data),
                'models_status': {
                    'delay_predictor': delay_model_status,
                    'readiness_model': readiness_model_status,
                    'genetic_optimizer': 'ready',
                    'moo_optimizer': 'ready',
                    'whatif_simulator': 'ready'
                },
                'data_status': {
                    'train_data_freshness': train_data_age,
                    'cache_size': len(self.cache),
                    'last_generation': system_manager.last_updated
                },
                'train_status_distribution': status_counts,
                'operational_metrics': self._calculate_operational_metrics(trains_data),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"System status check failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'system_health': 'degraded',
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_operational_metrics(self, trains_data: List[Dict]) -> Dict:
        """Calculate key operational metrics"""
        if not trains_data:
            return {}
        
        service_trains = [t for t in trains_data if t.get('status') == 'service']
        ready_trains = [t for t in trains_data if t.get('operational_ready', False)]
        
        avg_readiness = np.mean([t.get('readiness_score', 50) for t in trains_data])
        
        return {
            'service_capacity_percentage': round((len(service_trains) / len(trains_data)) * 100, 1),
            'operational_readiness_percentage': round((len(ready_trains) / len(trains_data)) * 100, 1),
            'average_fleet_readiness': round(avg_readiness, 1),
            'maintenance_backlog': len([t for t in trains_data if t.get('status') == 'maintenance']),
            'emergency_reserve': len([t for t in trains_data if t.get('emergency_deployable', False) and t.get('status') == 'standby'])
        }