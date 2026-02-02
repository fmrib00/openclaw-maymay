#!/bin/bash

# Update and restart web server script
# Usage: update-server.sh [maymay|hero|all]

set -e

PROJECT_DIR=""
SERVICE_NAME=""
SERVER_NAME=""

case "$1" in
  maymay|maymay-backend)
    PROJECT_DIR="/home/yongyue/maymay-backend"
    SERVICE_NAME="maymay-backend"
    SERVER_NAME="Maymay"
    ;;
  hero|heroweb|heroweb-backend)
    PROJECT_DIR="/home/yongyue/heroweb-backend"
    SERVICE_NAME="heroweb-backend"
    SERVER_NAME="Heroweb"
    ;;
  all|both)
    echo "Updating all servers..."
    "$0" hero
    "$0" maymay
    exit 0
    ;;
  *)
    echo "Updating all servers..."
    "$0" hero
    "$0" maymay
    ;;
esac

echo "========================================"
echo "Updating $SERVER_NAME Backend"
echo "========================================"

cd "$PROJECT_DIR" || exit 1

echo "Step 1: Pulling latest code..."
git pull || {
  echo "Error: Git pull failed"
  exit 1
}

echo "Step 2: Restarting service..."
if [ "$SERVICE_NAME" = "maymay-backend" ]; then
  systemctl restart maymay-backend || {
    echo "Error: Failed to restart maymay-backend service"
    exit 1
  }
else
  systemctl restart heroweb-backend || {
    echo "Error: Failed to restart heroweb-backend service"
    exit 1
  }
fi

echo "Step 3: Waiting for service to start..."
sleep 5

echo "Step 4: Checking status..."
PORT_CHECK=""
if [ "$SERVICE_NAME" = "heroweb-backend" ]; then
  PORT_CHECK=":8001"
else
  PORT_CHECK=":8000"
fi

if ss -tlnp | grep -q "$PORT_CHECK"; then
  echo "✅ $SERVER_NAME Backend restarted successfully!"
  echo "Port $PORT_CHECK is listening"
else
  echo "❌ $SERVER_NAME Backend failed to start"
  echo "Port $PORT_CHECK is not listening"
  exit 1
fi

echo "========================================"
echo "Update complete!"
echo "========================================"
