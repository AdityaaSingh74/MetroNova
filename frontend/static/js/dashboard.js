/**
 * 🚇 KMRL Dashboard JavaScript
 * Main functionality for the train scheduling dashboard
 */

class KMRLDashboard {
    constructor() {
        this.socket = null;
        this.charts = {};
        this.currentSchedule = null;
        this.systemStatus = {
            last_update: null,
            active_trains: 0,
            maintenance_trains: 0,
            standby_trains: 0,
            avg_delay: 0.0,
            system_health: 'Good'
        };
        
        this.init();
    }

    init() {
        console.log('🚇 Initializing KMRL Dashboard...');
        
        // Initialize Socket.IO connection
        this.initSocket();
        
        // Initialize charts
        this.initCharts();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start real-time updates
        this.startRealTimeUpdates();
        
        // Load initial data
        this.loadInitialData();
        
        console.log('✅ Dashboard initialized successfully');
    }

    initSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('🔌 Connected to server');
            this.updateConnectionStatus(true);
            showNotification('Connected to KMRL server', 'success');
        });

        this.socket.on('disconnect', () => {
            console.log('🔌 Disconnected from server');
            this.updateConnectionStatus(false);
            showNotification('Disconnected from server', 'warning');
        });

        this.socket.on('schedule_updated', (data) => {
            console.log('📋 Schedule updated', data);
            this.updateScheduleTable(data.schedule);
            this.updateSystemStats(data.status);
            showNotification('Schedule updated successfully', 'success');
        });

        this.socket.on('live_update', (data) => {
            this.updateSystemStats(data.system_status);
            this.updateCharts();
        });

        this.socket.on('status', (data) => {
            console.log('📊 Status update:', data);
        });
    }

    initCharts() {
        // Distribution Chart (Pie)
        const distributionCtx = document.getElementById('distributionChart');
        if (distributionCtx) {
            this.charts.distribution = new Chart(distributionCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Active', 'Standby', 'Maintenance'],
                    datasets: [{
                        data: [0, 0, 0],
                        backgroundColor: [
                            '#10b981', // Green for active
                            '#f59e0b', // Yellow for standby
                            '#06b6d4'  // Blue for maintenance
                        ],
                        borderColor: '#1e293b',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#cbd5e1',
                                padding: 20
                            }
                        }
                    }
                }
            });
        }

        // Metrics Chart (Line)
        const metricsCtx = document.getElementById('metricsChart');
        if (metricsCtx) {
            this.charts.metrics = new Chart(metricsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Average Delay (min)',
                        data: [],
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    }, {
                        label: 'Active Trains',
                        data: [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            ticks: { color: '#cbd5e1' },
                            grid: { color: '#334155' }
                        },
                        y: {
                            ticks: { color: '#cbd5e1' },
                            grid: { color: '#334155' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#cbd5e1' }
                        }
                    }
                }
            });
        }
    }

    setupEventListeners() {
        // Update time display
        setInterval(() => {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-IN', {
                timeZone: 'Asia/Kolkata',
                hour12: true,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            
            const timeElement = document.getElementById('currentTime');
            if (timeElement) {
                timeElement.textContent = timeString;
            }
        }, 1000);

        // Add click handlers for dynamic elements
        document.addEventListener('click', (e) => {
            if (e.target.matches('.train-action-btn')) {
                this.handleTrainAction(e.target);
            }
        });
    }

    startRealTimeUpdates() {
        // Update charts every 30 seconds
        setInterval(() => {
            this.updateCharts();
        }, 30000);

        // Update system status every 10 seconds
        setInterval(() => {
            this.fetchSystemStatus();
        }, 10000);
    }

    async loadInitialData() {
        try {
            showLoading(true);
            
            // Load system status
            await this.fetchSystemStatus();
            
            // Load current schedule if available
            await this.fetchCurrentSchedule();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            showNotification('Failed to load initial data', 'error');
        } finally {
            showLoading(false);
        }
    }

    async fetchSystemStatus() {
        try {
            const response = await fetch('/api/system-status');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updateSystemStats(data.system_status);
            }
        } catch (error) {
            console.error('Error fetching system status:', error);
        }
    }

    async fetchCurrentSchedule() {
        try {
            const response = await fetch('/api/current-schedule');
            if (response.ok) {
                const data = await response.json();
                if (data.schedule) {
                    this.updateScheduleTable(data.schedule);
                }
            }
        } catch (error) {
            console.error('Error fetching current schedule:', error);
        }
    }

    updateSystemStats(status) {
        if (!status) return;
        
        this.systemStatus = { ...this.systemStatus, ...status };
        
        // Update stat cards
        document.getElementById('activeTrainsCount').textContent = status.active_trains || 0;
        document.getElementById('standbyTrainsCount').textContent = status.standby_trains || 0;
        document.getElementById('maintenanceTrainsCount').textContent = status.maintenance_trains || 0;
        document.getElementById('avgDelay').textContent = (status.avg_delay || 0).toFixed(1);
        
        // Update system health indicator
        const healthElement = document.getElementById('systemStatus');
        const indicator = healthElement.querySelector('.status-indicator');
        const text = healthElement.querySelector('.status-text');
        
        if (status.system_health === 'Good') {
            indicator.className = 'status-indicator good';
            text.textContent = 'System Operational';
        } else if (status.system_health === 'Warning') {
            indicator.className = 'status-indicator warning';
            text.textContent = 'Attention Required';
        } else {
            indicator.className = 'status-indicator danger';
            text.textContent = 'System Issues';
        }
        
        // Update charts
        this.updateDistributionChart();
        this.updateMetricsChart();
    }

    updateDistributionChart() {
        if (!this.charts.distribution) return;
        
        const data = [
            this.systemStatus.active_trains,
            this.systemStatus.standby_trains,
            this.systemStatus.maintenance_trains
        ];
        
        this.charts.distribution.data.datasets[0].data = data;
        this.charts.distribution.update('none');
    }

    updateMetricsChart() {
        if (!this.charts.metrics) return;
        
        const now = new Date();
        const timeLabel = now.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Keep only last 20 data points
        const maxPoints = 20;
        const chart = this.charts.metrics;
        
        if (chart.data.labels.length >= maxPoints) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
            chart.data.datasets[1].data.shift();
        }
        
        chart.data.labels.push(timeLabel);
        chart.data.datasets[0].data.push(this.systemStatus.avg_delay || 0);
        chart.data.datasets[1].data.push(this.systemStatus.active_trains || 0);
        
        chart.update('none');
    }

    updateScheduleTable(scheduleData) {
        const tbody = document.getElementById('scheduleTableBody');
        if (!tbody || !scheduleData || !Array.isArray(scheduleData)) {
            return;
        }
        
        this.currentSchedule = scheduleData;
        
        if (scheduleData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="no-data">No schedule data available</td></tr>';
            return;
        }
        
        tbody.innerHTML = scheduleData.map(train => `
            <tr>
                <td><strong>${train.TrainID || 'N/A'}</strong></td>
                <td><span class="status-badge status-${train.OperationalStatus || 'unknown'}">${train.OperationalStatus || 'Unknown'}</span></td>
                <td>${(train.Score || 0).toFixed(1)}</td>
                <td>${train.RollingStockFitnessStatus ? '✅' : '❌'}</td>
                <td>${train.OpenJobCards || 0}</td>
                <td>${train.BrandingActive ? '🎯' : '—'}</td>
                <td>${(train.PredictedDelayMinutes || 0).toFixed(1)}</td>
                <td>
                    <button class="btn-small primary train-action-btn" data-train="${train.TrainID}" data-action="details">
                        Details
                    </button>
                </td>
            </tr>
        `).join('');
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connectionStatus');
        if (connected) {
            statusElement.innerHTML = '<i class="fas fa-wifi"></i> Connected';
            statusElement.style.color = '#10b981';
        } else {
            statusElement.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Disconnected';
            statusElement.style.color = '#ef4444';
        }
    }

    updateCharts() {
        this.updateDistributionChart();
        this.updateMetricsChart();
    }

    handleTrainAction(button) {
        const trainId = button.dataset.train;
        const action = button.dataset.action;
        
        if (action === 'details' && trainId) {
            this.showTrainDetails(trainId);
        }
    }

    showTrainDetails(trainId) {
        const train = this.currentSchedule?.find(t => t.TrainID === trainId);
        if (!train) {
            showNotification('Train details not found', 'error');
            return;
        }
        
        const details = `
            <h4>🚇 ${train.TrainID} Details</h4>
            <p><strong>Status:</strong> ${train.OperationalStatus}</p>
            <p><strong>Score:</strong> ${train.Score?.toFixed(2)}</p>
            <p><strong>Fitness Status:</strong> ${train.RollingStockFitnessStatus ? 'Valid' : 'Invalid'}</p>
            <p><strong>Open Job Cards:</strong> ${train.OpenJobCards || 0}</p>
            <p><strong>Total Mileage:</strong> ${train.TotalMileageKM || 'N/A'} km</p>
            <p><strong>Brake Wear:</strong> ${train['BrakepadWear%'] || 'N/A'}%</p>
            <p><strong>HVAC Wear:</strong> ${train['HVACWear%'] || 'N/A'}%</p>
            <p><strong>Predicted Delay:</strong> ${train.PredictedDelayMinutes?.toFixed(1) || 0} min</p>
        `;
        
        showModal('Train Details', details);
    }
}

// Global functions for button handlers
async function generateData() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/generate-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num_trains: 25,
                include_delays: true
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showNotification('Data generated successfully', 'success');
        } else {
            showNotification(data.message || 'Failed to generate data', 'error');
        }
        
    } catch (error) {
        console.error('Error generating data:', error);
        showNotification('Failed to generate data', 'error');
    } finally {
        showLoading(false);
    }
}

async function refreshData() {
    showNotification('Refreshing data...', 'info');
    window.dashboard.loadInitialData();
}

async function runOptimization(algorithm) {
    try {
        showLoading(true);
        showNotification(`Running ${algorithm} optimization...`, 'info');
        
        const response = await fetch('/api/optimize-schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                algorithm: algorithm,
                constraints: {
                    service_quota: 13,
                    max_maintenance: 8
                }
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showNotification(`${algorithm} optimization completed successfully`, 'success');
            window.dashboard.updateScheduleTable(data.schedule_preview);
            window.dashboard.fetchSystemStatus();
        } else {
            showNotification(data.message || 'Optimization failed', 'error');
        }
        
    } catch (error) {
        console.error('Error running optimization:', error);
        showNotification('Optimization failed', 'error');
    } finally {
        showLoading(false);
    }
}

async function predictDelay() {
    try {
        const dwellTime = parseFloat(document.getElementById('dwellTime').value) || 60;
        const distance = parseFloat(document.getElementById('distance').value) || 8.5;
        const loadFactor = parseFloat(document.getElementById('loadFactor').value) || 0.7;
        
        const response = await fetch('/api/predict-delays', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dwell_time: dwellTime,
                distance: distance,
                load_factor: loadFactor
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const resultDiv = document.getElementById('delayResult');
            const prediction = data.prediction;
            
            resultDiv.innerHTML = `
                <h5>🔮 Delay Prediction Results</h5>
                <p><strong>Category:</strong> ${prediction['Predicted Delay Category']}</p>
                <p><strong>Minutes:</strong> ${prediction['Predicted Delay Minutes']}</p>
                <p><strong>Service Pattern:</strong> ${prediction['Predicted Service Pattern']}</p>
                <p><strong>Day Type:</strong> ${prediction['Predicted Day Type']}</p>
                ${prediction.Confidence ? `<p><strong>Confidence:</strong> ${prediction.Confidence}%</p>` : ''}
                ${prediction.Recommendations ? `<div><strong>Recommendations:</strong><ul>${prediction.Recommendations.map(r => `<li>${r}</li>`).join('')}</ul></div>` : ''}
            `;
            
            resultDiv.style.display = 'block';
            showNotification('Delay prediction completed', 'success');
            
        } else {
            showNotification(data.message || 'Prediction failed', 'error');
        }
        
    } catch (error) {
        console.error('Error predicting delay:', error);
        showNotification('Prediction failed', 'error');
    }
}

function updateChart(chartType) {
    if (window.dashboard) {
        window.dashboard.updateCharts();
        showNotification(`${chartType} chart updated`, 'info');
    }
}

async function exportSchedule() {
    try {
        const response = await fetch('/api/download-schedule');
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `kmrl_schedule_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            showNotification('Schedule exported successfully', 'success');
        } else {
            showNotification('Failed to export schedule', 'error');
        }
        
    } catch (error) {
        console.error('Error exporting schedule:', error);
        showNotification('Export failed', 'error');
    }
}

function refreshSchedule() {
    if (window.dashboard) {
        window.dashboard.fetchCurrentSchedule();
        showNotification('Schedule refreshed', 'info');
    }
}

function toggleWhatIf() {
    const section = document.querySelector('.whatif-section');
    if (section.style.display === 'none') {
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }
}

async function runWhatIf() {
    try {
        showLoading(true);
        
        const scenarioType = document.getElementById('scenarioType').value;
        const affectedTrains = document.getElementById('affectedTrains').value;
        
        const scenario = {
            type: scenarioType,
            affected_trains: affectedTrains.split(',').map(t => t.trim()).filter(t => t)
        };
        
        const response = await fetch('/api/whatif-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ scenario })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const resultsDiv = document.getElementById('whatifResults');
            resultsDiv.innerHTML = `
                <h5>📊 What-If Analysis Results</h5>
                <pre>${JSON.stringify(data.scenario_results, null, 2)}</pre>
            `;
            resultsDiv.style.display = 'block';
            
            showNotification('What-if analysis completed', 'success');
        } else {
            showNotification(data.message || 'Analysis failed', 'error');
        }
        
    } catch (error) {
        console.error('Error running what-if analysis:', error);
        showNotification('Analysis failed', 'error');
    } finally {
        showLoading(false);
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => {
            container.removeChild(notification);
        }, 300);
    }, 5000);
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

function showModal(title, content) {
    // Simple modal implementation
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${title}</h3>
                <button onclick="this.closest('.modal-overlay').remove()">&times;</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Remove on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
    }
    
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(15, 23, 42, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 3000;
    }
    
    .modal-content {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        max-width: 500px;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .modal-header {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .modal-header h3 {
        margin: 0;
        color: var(--text-primary);
    }
    
    .modal-header button {
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--text-secondary);
        cursor: pointer;
    }
    
    .modal-body {
        padding: 1.5rem;
        color: var(--text-secondary);
    }
    
    .modal-body h4 {
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .modal-body p {
        margin-bottom: 0.5rem;
    }
`;
document.head.appendChild(style);

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new KMRLDashboard();
});