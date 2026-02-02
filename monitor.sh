#!/bin/bash
# Monitor script for backends, Redis, and system resources
# Send alerts via OpenClaw message tool

LOG_FILE="/home/yongyue/.openclaw/workspace/monitor.log"
ALERT_FILE="/home/yongyue/.openclaw/workspace/alert.tmp"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Clear previous alerts
> "$ALERT_FILE"

echo "=== Check at $TIMESTAMP ===" >> "$LOG_FILE"

# Function to add alert
add_alert() {
    echo "$1" >> "$ALERT_FILE"
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Check Maymay Backend (port 8000)
if ! ss -tlnp | grep -q ":8000 "; then
    add_alert "🔴 CRITICAL: Maymay Backend (port 8000) is DOWN!"
elif ! curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    add_alert "🔴 CRITICAL: Maymay Backend health check failed!"
else
    echo "✓ Maymay Backend OK" >> "$LOG_FILE"
fi

# Check Heroweb Backend (port 8001)
if ! ss -tlnp | grep -q ":8001 "; then
    add_alert "🔴 CRITICAL: Heroweb Backend (port 8001) is DOWN!"
else
    echo "✓ Heroweb Backend OK" >> "$LOG_FILE"
fi

# Check Redis
if ! ss -tlnp | grep -q ":6379 " || ! ps aux | grep redis-server | grep -v grep > /dev/null; then
    add_alert "🔴 CRITICAL: Redis is DOWN!"
else
    echo "✓ Redis OK" >> "$LOG_FILE"
fi

# Check Nginx
if ! systemctl is-active --quiet nginx; then
    add_alert "🔴 CRITICAL: Nginx is DOWN!"
else
    echo "✓ Nginx OK" >> "$LOG_FILE"
fi

# Check disk usage
DISK_USAGE=$(df /home/yongyue | tail -1 | awk '{print $5}' | sed 's/%//')
DISK_GB_USED=$(df /home/yongyue | tail -1 | awk '{print $3}')
DISK_GB_TOTAL=$(df /home/yongyue | tail -1 | awk '{print $2}')

echo "Disk: ${DISK_USAGE}% (${DISK_GB_USED}GB / ${DISK_GB_TOTAL}GB)" >> "$LOG_FILE"

if [ "$DISK_USAGE" -gt 80 ]; then
    add_alert "🟡 WARNING: Disk usage at ${DISK_USAGE}%!"
elif [ "$DISK_USAGE" -gt 90 ]; then
    add_alert "🔴 CRITICAL: Disk usage at ${DISK_USAGE}%!"
fi

# Check memory usage
MEM_PERCENT=$(free | awk '/Mem/{printf("%.0f", $3/$2*100)}')
MEM_GB_USED=$(free -h | awk '/Mem/{print $3}')
MEM_GB_TOTAL=$(free -h | awk '/Mem/{print $2}')

echo "Memory: ${MEM_PERCENT}% (${MEM_GB_USED} / ${MEM_GB_TOTAL})" >> "$LOG_FILE"

if [ "$MEM_PERCENT" -gt 80 ]; then
    add_alert "🟡 WARNING: Memory usage at ${MEM_PERCENT}%!"
elif [ "$MEM_PERCENT" -gt 90 ]; then
    add_alert "🔴 CRITICAL: Memory usage at ${MEM_PERCENT}%!"
fi

# Check load average
LOAD_1=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
LOAD_5=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $2}' | sed 's/,//')

echo "Load: ${LOAD_1} (1min), ${LOAD_5} (5min)" >> "$LOG_FILE"

# Send alerts via OpenClaw
if [ -s "$ALERT_FILE" ]; then
    # Create alert file for OpenClaw to read
    ALERT_TEXT=$(cat "$ALERT_FILE")
    echo "⚠️ SYSTEM ALERT ⚠️" > "/home/yongyue/.openclaw/workspace/ALERT_TO_SEND.txt"
    echo "" >> "/home/yongyue/.openclaw/workspace/ALERT_TO_SEND.txt"
    echo "$ALERT_TEXT" >> "/home/yongyue/.openclaw/workspace/ALERT_TO_SEND.txt"
    echo "Alerts queued!" >> "$LOG_FILE"
else
    echo "No alerts - all systems normal" >> "$LOG_FILE"
fi

echo "========================================" >> "$LOG_FILE"

# Keep log file manageable
tail -1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
