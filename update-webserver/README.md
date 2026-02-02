# Update Webserver

A skill for quickly updating and restarting web servers.

## What It Does

- Pulls the latest code from Git
- Stops existing processes
- Starts the backend service
- Verifies the service is running

## Commands

**English:**
- `update maymay server` - Update Maymay Backend (port 8000)
- `update hero server` - Update Heroweb Backend (port 8001)
- `update webserver` - Update both backends
- `update all` - Update both backends

**Chinese:**
- `更新maymay网站` - 更新 Maymay 网站
- `更新hero网站` - 更新 Hero 网站
- `更新网站` - 更新所有网站
- `全部更新` - 更新全部

## Usage

Simply say the command to this skill. For example:

> Update maymay server

Or in Chinese:

> 更新maymay网站

The skill will automatically:
1. Navigate to the project directory
2. Pull the latest code from Git
3. Stop any existing processes
4. Start the backend service
5. Verify the service is running

## Project Paths

- **Maymay Backend:** `/home/yongyue/maymay-backend/`
- **Heroweb Backend:** `/home/yongyue/heroweb-backend/`

## Setting Timezone

To set timezone to Asia/Taipei for Maymay Backend, run:

```bash
set-tz maymay
```

This will add `TZ=Asia/Taipei` to the systemd service configuration and restart the service.
