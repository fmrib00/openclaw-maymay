#!/bin/bash

# Set timezone for Maymay Backend
# This script adds TZ environment variable to systemd service file

SERVICE_FILE="/etc/systemd/system/maymay-backend.service"
TZ_VALUE="Asia/Taipei"

echo "========================================"
echo "Setting timezone for Maymay Backend"
echo "========================================"

# Check if service file exists
if [ ! -f "$SERVICE_FILE" ]; then
  echo "Error: Service file not found at $SERVICE_FILE"
  exit 1
fi

# Check if Environment= line already exists
if grep -q "^Environment=" "$SERVICE_FILE"; then
  echo "Environment line already exists. Updating TZ value..."
  sed -i "s/^Environment=.*/Environment=\"TZ=$TZ_VALUE\"/" "$SERVICE_FILE"
else
  echo "Adding new Environment line with TZ..."
  sed -i "/^\[Service\]/a\\Environment=\"TZ=$TZ_VALUE\"/" "$SERVICE_FILE"
fi

echo "✅ Timezone set to: $TZ_VALUE"
echo ""
echo "Reloading systemd configuration..."
systemctl daemon-reload || {
  echo "Error: Failed to reload systemd daemon"
  exit 1
}

echo "Restarting Maymay Backend service..."
systemctl restart maymay-backend || {
  echo "Error: Failed to restart service"
  exit 1
}

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo "Verifying service is running..."
sleep 5
if systemctl is-active --quiet maymay-backend; then
  echo "✅ Maymay Backend is running with timezone: $TZ_VALUE"
  echo ""
  echo "Service status:"
  systemctl status maymay-backend --no-pager -l
else
  echo "❌ Maymay Backend failed to start"
  echo ""
  echo "Service status:"
  systemctl status maymay-backend --no-pager -l
  exit 1
fi
