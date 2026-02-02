---
name: update-webserver
description: Simplify web server code updates and restarts. Pull latest code and restart backend services for maymay or heroweb.
---

# Web Server Update

Quick update of backend servers by pulling latest code and restarting services.

## Supported Commands

- "update maymay server" or "更新maymay网站" - Update and restart Maymay Backend
- "update hero server" or "更新hero网站" - Update and restart Heroweb Backend
- "update maymay" or "更新maymay" - Update and restart Maymay Backend
- "update hero" or "更新hero" - Update and restart Heroweb Backend
- "update webserver" or "更新网站" - Update both backends
- "update all" or "全部更新" - Update both backends

## Usage Examples

**English:**
- "Update maymay server"
- "Update hero website"
- "Update webserver"
- "Update all"

**Chinese:**
- "更新maymay网站"
- "更新hero网站"
- "更新网站"
- "全部更新"

## How It Works

1. **Pull Latest Code** - Runs `git pull` in the project directory to fetch latest changes
2. **Restart Service** - Restarts the systemd service for the backend
3. **Wait & Verify** - Waits for startup and checks if the service is listening on the correct port

## Notes

- The script automatically handles both Maymay (port 8000) and Heroweb (port 8001) backends
- Timezone is configured at the system level and does not need to be set during updates
- Requires sudo password for systemctl commands (unless configured in sudoers)

## Project Paths

- **Maymay Backend:** `/home/yongyue/maymay-backend/`
- **Heroweb Backend:** `/home/yongyue/heroweb-backend/`
