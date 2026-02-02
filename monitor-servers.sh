#!/bin/bash
# Monitor script for web servers
# Usage: ./monitor-servers.sh

LOG_FILE="/home/yongyue/.openclaw/workspace/server-monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Server Status Check [$TIMESTAMP] ===" >> "$LOG_FILE"

# Check maymay-backend (port 8000)
echo "" >> "$LOG_FILE"
echo "=== Maymay Backend (port 8000) ===" >> "$LOG_FILE"
if ss -tlnp | grep -q ":8000 "; then
    echo "✓ Port 8000 is listening" >> "$LOG_FILE"
    curl -s -o /dev/null -w "✓ HTTP Status: %{http_code}\n" http://localhost:8000/api/v1 >> "$LOG_FILE" 2>&1
else
    echo "✗ Port 8000 NOT listening!" >> "$LOG_FILE"
fi

# Check heroweb-backend (port 8001)
echo "" >> "$LOG_FILE"
echo "=== Heroweb Backend (port 8001) ===" >> "$LOG_FILE"
if ss -tlnp | grep -q ":8001 "; then
    echo "✓ Port 8001 is listening" >> "$LOG_FILE"
    curl -s -o /dev/null -w "✓ HTTP Status: %{http_code}\n" http://localhost:8001 >> "$LOG_FILE" 2>&1
else
    echo "✗ Port 8001 NOT listening!" >> "$LOG_FILE"
fi

# Check running processes
echo "" >> "$LOG_FILE"
echo "=== Running Processes ===" >> "$LOG_FILE"
ps aux | grep -E "(main.py|app/main.py)" | grep -v grep >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Show recent alerts
echo ""
echo "Recent alerts:"
tail -30 "$LOG_FILE"
