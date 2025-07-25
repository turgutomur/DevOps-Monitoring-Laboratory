from flask import Flask, jsonify, render_template_string
import os
import time
import random
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('webapp_requests_total', 'Total webapp requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('webapp_request_duration_seconds', 'Request latency')
ACTIVE_USERS = Gauge('webapp_active_users', 'Number of active users')

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .info { background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .metrics { background: #f0f8f0; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .btn { display: inline-block; padding: 10px 20px; background: #007cba; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        .btn:hover { background: #005a87; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ app_name }}</h1>
            <p>Version: {{ app_version }}</p>
        </div>
        
        <div class="info">
            <h3>🚀 DevOps Monitoring Laboratory</h3>
            <p>This is a sample web application for demonstrating DevOps monitoring practices with:</p>
            <ul>
                <li><strong>Prometheus</strong> - Metrics collection and monitoring</li>
                <li><strong>Grafana</strong> - Visualization and dashboards</li>
                <li><strong>Nginx</strong> - Web server and reverse proxy</li>
                <li><strong>Docker</strong> - Containerization</li>
            </ul>
        </div>

        <div class="metrics">
            <h3>📊 Application Metrics</h3>
            <p>This application exposes Prometheus metrics at <code>/metrics</code> endpoint.</p>
            <p>Current active users: <strong>{{ active_users }}</strong></p>
            <p>Debug mode: <strong>{{ debug_mode }}</strong></p>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/health" class="btn">Health Check</a>
            <a href="/metrics" class="btn">View Metrics</a>
            <a href="/api/status" class="btn">API Status</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    
    # Simulate some active users
    ACTIVE_USERS.set(random.randint(1, 50))
    
    return render_template_string(HTML_TEMPLATE,
        app_name=os.getenv('APP_NAME', 'DevOps Monitoring WebApp'),
        app_version=os.getenv('APP_VERSION', '1.0.0'),
        debug_mode=os.getenv('DEBUG_MODE', 'false'),
        active_users=random.randint(1, 50)
    )

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'uptime': time.time()
    })

@app.route('/api/status')
def api_status():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/status').inc()
    
    return jsonify({
        'application': {
            'name': os.getenv('APP_NAME', 'DevOps Monitoring WebApp'),
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'debug': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
            'status': 'running'
        },
        'system': {
            'timestamp': time.time(),
            'active_users': random.randint(1, 50),
            'memory_usage': f"{random.randint(50, 200)}MB",
            'cpu_usage': f"{random.randint(10, 80)}%"
        }
    })

@app.route('/metrics')
def metrics():
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics').inc()
    
    # Update some metrics
    ACTIVE_USERS.set(random.randint(1, 50))
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.errorhandler(404)
def not_found(error):
    REQUEST_COUNT.labels(method='GET', endpoint='404').inc()
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    REQUEST_COUNT.labels(method='GET', endpoint='500').inc()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7070))
    debug = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    print(f"Starting {os.getenv('APP_NAME', 'DevOps Monitoring WebApp')} v{os.getenv('APP_VERSION', '1.0.0')}")
    print(f"Server running on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
