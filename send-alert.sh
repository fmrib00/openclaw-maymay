#!/bin/bash
# Check and send alerts via OpenClaw
ALERT_FILE="/home/yongyue/.openclaw/workspace/ALERT_TO_SEND.txt"

if [ -f "$ALERT_FILE" ] && [ -s "$ALERT_FILE" ]; then
    # Send alert via OpenClaw (will be handled by the agent)
    ALERT_TEXT=$(cat "$ALERT_FILE")
    echo "ALERT_PENDING: $ALERT_TEXT" > "/tmp/openclaw-alert.msg"
    # Move to processed to avoid duplicate sends
    mv "$ALERT_FILE" "/home/yongyue/.openclaw/workspace/ALERT_SENT.txt"
fi
