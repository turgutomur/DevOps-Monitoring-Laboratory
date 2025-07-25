#!/bin/bash

# Test Environment Variables
# Author: turgutomur
# Date: 2025-07-24

echo "🧪 Testing Environment Variables..."
echo "=================================="

# Load .env file
if [ -f .env ]; then
    echo "✅ .env file found"
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

echo ""
echo "📊 Grafana Settings:"
echo "  Admin User: ${GF_SECURITY_ADMIN_USER}"
echo "  Admin Password: [HIDDEN]"
echo "  Theme: ${GF_USERS_DEFAULT_THEME}"
echo "  Log Level: ${GF_LOG_LEVEL}"

echo ""
echo "🎯 Prometheus Settings:"
echo "  Retention Time: ${PROMETHEUS_RETENTION_TIME}"
echo "  Retention Size: ${PROMETHEUS_RETENTION_SIZE}"
echo "  Scrape Interval: ${PROMETHEUS_SCRAPE_INTERVAL}"

echo ""
echo "🌐 Application Settings:"
echo "  App Port: ${APP_PORT}"
echo "  App Name: ${APP_NAME}"
echo "  App Version: ${APP_VERSION}"
echo "  Debug Mode: ${DEBUG_MODE}"

echo ""
echo "🐳 Docker Settings:"
echo "  Project Name: ${COMPOSE_PROJECT_NAME}"
echo "  BuildKit: ${DOCKER_BUILDKIT}"

echo ""
echo "✅ Environment variables test completed!"