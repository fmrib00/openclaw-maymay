# HEARTBEAT.md - Heartbeat Tasks

## Check for system alerts
If /home/yongyue/.openclaw/workspace/ALERT_TO_SEND.txt exists and is not empty:
1. Read the alert content
2. Send it via message tool to telegram
3. Delete or rename the file after sending

## System health monitoring (rotate checks every heartbeat)
- Backend services status (ports 8000, 8001)
- Redis status (port 6379)
- Memory usage
- Disk space
