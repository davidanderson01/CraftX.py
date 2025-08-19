"""
Analytics Dashboard API Endpoints for CraftX
Provides web interface for viewing user analytics and tracking data
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional
import json
from datetime import datetime, timedelta


def add_analytics_routes(app: FastAPI, analytics_instance):
    """Add analytics routes to the FastAPI app"""

    @app.get("/admin/analytics", response_class=HTMLResponse)
    async def analytics_dashboard():
        """Render analytics dashboard HTML"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CraftX Analytics Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: #2196F3; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
                .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .stat-number { font-size: 2em; font-weight: bold; color: #2196F3; }
                .stat-label { color: #666; margin-top: 5px; }
                .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
                .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                .loading { text-align: center; padding: 40px; color: #666; }
                .refresh-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
                .export-btn { background: #FF9800; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-left: 10px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                .user-table { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 CraftX Analytics Dashboard</h1>
                    <p>Real-time user authentication and usage analytics</p>
                    <button class="refresh-btn" onclick="loadAnalytics()">🔄 Refresh Data</button>
                    <button class="export-btn" onclick="exportData()">📊 Export Data</button>
                </div>
                
                <div id="loading" class="loading">Loading analytics data...</div>
                
                <div id="dashboard" style="display: none;">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number" id="total-users">-</div>
                            <div class="stat-label">Total Users</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="new-users">-</div>
                            <div class="stat-label">New Users (30d)</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="active-sessions">-</div>
                            <div class="stat-label">Active Sessions (24h)</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="total-downloads">-</div>
                            <div class="stat-label">Total Downloads</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="top-provider">-</div>
                            <div class="stat-label">Top Auth Provider</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="top-country">-</div>
                            <div class="stat-label">Top Country</div>
                        </div>
                    </div>
                    
                    <div class="chart-grid">
                        <div class="chart-container">
                            <h3>📈 Daily Activity (Last 7 Days)</h3>
                            <canvas id="activityChart"></canvas>
                        </div>
                        <div class="chart-container">
                            <h3>🔐 Auth Provider Distribution</h3>
                            <canvas id="providerChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="chart-grid">
                        <div class="chart-container">
                            <h3>📱 Device Type Distribution</h3>
                            <canvas id="deviceChart"></canvas>
                        </div>
                        <div class="chart-container">
                            <h3>🌍 Geographic Distribution</h3>
                            <div id="geographic-data"></div>
                        </div>
                    </div>
                    
                    <div class="user-table">
                        <h3>👥 Recent User Activity</h3>
                        <table id="recent-users">
                            <thead>
                                <tr>
                                    <th>User ID</th>
                                    <th>Provider</th>
                                    <th>Country</th>
                                    <th>Device</th>
                                    <th>Downloads</th>
                                    <th>Last Seen</th>
                                </tr>
                            </thead>
                            <tbody id="users-tbody">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <script>
                let analyticsData = null;
                let activityChart = null;
                let providerChart = null;
                let deviceChart = null;
                
                async function loadAnalytics() {
                    try {
                        document.getElementById('loading').style.display = 'block';
                        document.getElementById('dashboard').style.display = 'none';
                        
                        const response = await fetch('/admin/analytics/data');
                        analyticsData = await response.json();
                        
                        updateDashboard();
                        
                        document.getElementById('loading').style.display = 'none';
                        document.getElementById('dashboard').style.display = 'block';
                    } catch (error) {
                        console.error('Error loading analytics:', error);
                        document.getElementById('loading').innerHTML = 'Error loading analytics data';
                    }
                }
                
                function updateDashboard() {
                    const summary = analyticsData.summary;
                    
                    // Update summary stats
                    document.getElementById('total-users').textContent = summary.total_users.toLocaleString();
                    document.getElementById('new-users').textContent = summary.new_users.toLocaleString();
                    document.getElementById('active-sessions').textContent = summary.active_sessions.toLocaleString();
                    document.getElementById('total-downloads').textContent = summary.total_downloads.toLocaleString();
                    document.getElementById('top-provider').textContent = summary.top_provider;
                    document.getElementById('top-country').textContent = summary.top_country;
                    
                    // Update charts
                    updateActivityChart();
                    updateProviderChart();
                    updateDeviceChart();
                    updateUserTable();
                }
                
                function updateActivityChart() {
                    const ctx = document.getElementById('activityChart').getContext('2d');
                    
                    if (activityChart) {
                        activityChart.destroy();
                    }
                    
                    const dates = Object.keys(analyticsData.recent_activity).reverse();
                    const values = dates.map(date => analyticsData.recent_activity[date]);
                    
                    activityChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: dates.map(date => new Date(date).toLocaleDateString()),
                            datasets: [{
                                label: 'Authentication Events',
                                data: values,
                                borderColor: '#2196F3',
                                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                                tension: 0.1
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
                
                function updateProviderChart() {
                    const ctx = document.getElementById('providerChart').getContext('2d');
                    
                    if (providerChart) {
                        providerChart.destroy();
                    }
                    
                    const providers = Object.keys(analyticsData.provider_breakdown);
                    const counts = Object.values(analyticsData.provider_breakdown);
                    
                    providerChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: providers,
                            datasets: [{
                                data: counts,
                                backgroundColor: [
                                    '#4285F4', '#34A853', '#FBBC05', '#EA4335',
                                    '#9C27B0', '#FF9800', '#795548', '#607D8B'
                                ]
                            }]
                        },
                        options: {
                            responsive: true
                        }
                    });
                }
                
                function updateDeviceChart() {
                    const ctx = document.getElementById('deviceChart').getContext('2d');
                    
                    if (deviceChart) {
                        deviceChart.destroy();
                    }
                    
                    const devices = Object.keys(analyticsData.device_breakdown);
                    const counts = Object.values(analyticsData.device_breakdown);
                    
                    deviceChart = new Chart(ctx, {
                        type: 'pie',
                        data: {
                            labels: devices,
                            datasets: [{
                                data: counts,
                                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
                            }]
                        },
                        options: {
                            responsive: true
                        }
                    });
                }
                
                async function updateUserTable() {
                    try {
                        const response = await fetch('/admin/analytics/recent-users');
                        const users = await response.json();
                        
                        const tbody = document.getElementById('users-tbody');
                        tbody.innerHTML = '';
                        
                        users.forEach(user => {
                            const row = tbody.insertRow();
                            row.innerHTML = `
                                <td>${user.user_id.substring(0, 8)}...</td>
                                <td>${user.provider}</td>
                                <td>${user.country || 'Unknown'}</td>
                                <td>${user.preferred_device || 'Unknown'}</td>
                                <td>${user.total_downloads}</td>
                                <td>${new Date(user.last_seen).toLocaleString()}</td>
                            `;
                        });
                    } catch (error) {
                        console.error('Error loading recent users:', error);
                    }
                }
                
                async function exportData() {
                    try {
                        const response = await fetch('/admin/analytics/export');
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = `craftx-analytics-${new Date().toISOString().split('T')[0]}.json`;
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    } catch (error) {
                        console.error('Error exporting data:', error);
                        alert('Error exporting data');
                    }
                }
                
                // Load analytics on page load
                loadAnalytics();
                
                // Auto-refresh every 5 minutes
                setInterval(loadAnalytics, 5 * 60 * 1000);
            </script>
        </body>
        </html>
        """

    @app.get("/admin/analytics/data")
    async def get_analytics_data(days: int = 30):
        """Get analytics summary data"""
        try:
            summary = analytics_instance.get_analytics_summary(days)
            return JSONResponse(content=summary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/admin/analytics/recent-users")
    async def get_recent_users(limit: int = 50):
        """Get recent user data for table display"""
        try:
            import sqlite3
            conn = sqlite3.connect(analytics_instance.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT user_id, provider, country, preferred_device, 
                       total_downloads, last_seen
                FROM users 
                ORDER BY last_seen DESC 
                LIMIT ?
            """, (limit,))

            users = []
            for row in cursor.fetchall():
                users.append({
                    "user_id": row[0],
                    "provider": row[1],
                    "country": row[2],
                    "preferred_device": row[3],
                    "total_downloads": row[4],
                    "last_seen": row[5]
                })

            conn.close()
            return JSONResponse(content=users)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/admin/analytics/export")
    async def export_analytics_data(format: str = "json"):
        """Export analytics data"""
        try:
            data = analytics_instance.export_analytics(format)

            if format.lower() == "json":
                return JSONResponse(
                    content=json.loads(data),
                    headers={
                        "Content-Disposition": "attachment; filename=analytics.json"}
                )
            else:
                from fastapi.responses import PlainTextResponse
                return PlainTextResponse(
                    content=data,
                    headers={
                        "Content-Disposition": "attachment; filename=analytics.csv"}
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/admin/analytics/user/{user_id}")
    async def get_user_details(user_id: str):
        """Get detailed information about a specific user"""
        try:
            details = analytics_instance.get_user_details(user_id)
            if not details:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(content=details)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
