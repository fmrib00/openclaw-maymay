---
name: update-webserver
description: Simplify web server code updates and restarts. Pull latest code and restart backend services for maymay or heroweb. Also provides timezone configuration for Maymay Backend.
---

# Web Server Update

Quick update of backend servers by pulling latest code and restarting services.

## Supported Commands

- "update maymay server" or "更新maymay网站" - Update and restart Maymay Backend
- "update hero server" or "更新hero网站" - Update and restart Heroweb Backend
- "update maymay" or "更新maymay" - Update Maymay Backend (includes timezone setup)
- "update hero" or "更新hero" - Update and restart Heroweb Backend (includes timezone setup)
- "update webserver" or "更新网站" - Update both backends (Maymay includes timezone setup)
- "update all" or "全部更新" - Update both backends
- "set-timezone maymay" or "设置maymay时区" - Set timezone for Maymay Backend to Asia/Taipei

## Usage Examples

**English:**
- "Update maymay server"
- "Update hero website"
- "Update webserver"
- "Update all"
- "Set timezone for maymay"

**Chinese:**
- "更新maymay网站"
- "更新hero网站"
- "更新网站"
- "全部更新"
- "设置maymay时区"

## How It Works

1. **Pull Latest Code** - Runs `git pull` in the project directory to fetch latest changes
2. **Stop Processes** - Stops all existing Python processes for the backend
3. **Start Server** - Starts the backend service in background mode
4. **Wait & Verify** - Waits for startup and checks if service is listening on the correct port

## Setting Timezone

For Maymay Backend, you can set the timezone to Asia/Taipei. This will:
- Add `TZ=Asia/Taipei` to the systemd service configuration
- Reload systemd daemon
- Restart the service

To configure timezone, use: `设置maymay时区` or `set-timezone maymay`

## Notes

- The script automatically handles both Maymay (port 8000) and Heroweb (port 8001) backends
- Heroweb timezone uses system default (UTC)
- Timezone changes persist across service restarts

## Project Paths

- **Maymay Backend:** `/home/yongyue/maymay-backend/`
- **Heroweb Backend:** `/home/yongyue/heroweb-backend/`
- **Set-Timezone Script:** `/home/yongyue/.openclaw/workspace/set-timezone/set-tz.sh`
