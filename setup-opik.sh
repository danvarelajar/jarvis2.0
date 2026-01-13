#!/bin/bash

# Setup script for Opik Observability (Option 1: Separate Deployment)
# This script helps you set up Opik to run separately from your application

set -e

echo "🔧 Setting up Opik Observability Platform (Option 1)"
echo ""

# Check if Opik directory exists
OPIK_DIR="../opik"

if [ ! -d "$OPIK_DIR" ]; then
    echo "📦 Cloning Opik repository..."
    cd ..
    git clone https://github.com/comet-ml/opik.git
    cd opik
    echo "✅ Opik repository cloned"
else
    echo "✅ Opik directory already exists at $OPIK_DIR"
    cd "$OPIK_DIR"
fi

echo ""
echo "🚀 Starting Opik services..."
echo "   This will start Opik using Docker Compose"
echo ""

# Check if opik.sh exists and is executable
if [ -f "./opik.sh" ]; then
    chmod +x ./opik.sh
    echo "   Running: ./opik.sh"
    ./opik.sh
else
    echo "❌ Error: opik.sh not found in $OPIK_DIR"
    echo "   Please check the Opik repository structure"
    exit 1
fi

echo ""
echo "✅ Opik setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Verify Opik is running: docker ps | grep opik"
echo "   2. Access Opik dashboard: http://localhost:5173"
echo "   3. In your Jarvis2.0 directory, copy env.example to .env:"
echo "      cp env.example .env"
echo "   4. Start your application: docker-compose up --build"
echo ""
echo "💡 Tip: Keep this terminal open to see Opik logs"
echo "   Or run Opik in background: ./opik.sh &"
