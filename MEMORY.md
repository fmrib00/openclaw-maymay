# MEMORY.md - Long-term Memory

## Projects & Services

### Heroweb Backend
- **Location:** `/home/yongyue/heroweb-backend/`
- **Port:** 8001
- **PID:** 19006 (as of 2026-02-01)
- **Virtual environment:** `env/`
- **Start command:** `source env/bin/activate && python main.py` (from project root)
- **Description:** Game-related backend with character management, dungeons, lottery, job scheduling
- **Backend URL:** https://wulinhero.dpdns.org (Cloudflare proxy → Nginx → 127.0.0.1:8001)
- **Key files:** main.py, character.py, dungeon.py, pvehall.py, lottery.py, job_scheduler.py

### Maymay Backend
- **Location:** `/home/yongyue/maymay-backend/`
- **Port:** 8000
- **PID:** 19103 (as of 2026-02-01)
- **Virtual environment:** `env/`
- **Start command:** `source env/bin/activate && python app/main.py` (from project root)
- **Description:** Maymay穿戴甲销售平台后端 (maymaynail.com)
  - LINE Pay集成
  - 后台任务处理（多进程worker，各~315MB内存）
  - 仪表盘统计
- **Frontend:** https://maymaynail.com (Vercel/Next.js)
- **Backend URL:** https://maymay.dpdns.org/api/v1 (Cloudflare proxy → Nginx → 127.0.0.1:8000)
- **Key files:** app/app.py, app/main.py, glm_vision_client.py

## Critical Tasks

### 🔴 Primary: Monitor & Maintain Backends
- **Status:** MOST IMPORTANT TASK
- **Scope:** Keep both heroweb-backend (8001) and maymay-backend (8000) running smoothly
- **Actions to take:**
  - Regular health checks
  - Monitor logs for errors
  - Restart services if they crash
  - Watch for performance issues
  - Check disk space/memory usage
  - Verify both ports are listening

## Service Management - CRITICAL RULES

### ✅ Correct Way to Restart Services

**Maymay Backend (systemd managed):**
```bash
systemctl restart maymay-backend.service
systemctl status maymay-backend.service
```

**Heroweb Backend (manual process):**
```bash
# Find and kill existing process
ps aux | grep "python.*main.py" | grep heroweb
kill <PID>

# Start fresh
cd /home/yongyue/heroweb-backend
source env/bin/activate && python main.py &
```

### ❌ NEVER DO THIS

**Problem:** Never manually start Maymay backend using direct python commands:
```bash
# WRONG! This creates a process that conflicts with systemd
cd /home/yongyue/maymay-backend && source env/bin/activate && python app/main.py &
```

**Consequence:** Manual process binds port 8000 → systemd restart fails with:
```
ERROR: [Errno 98] Address already in use
```

**What happened (2026-02-02):**
- Manually started maymay processes (PIDs 41001, 41006, 41007)
- systemd repeatedly tried to restart, failing with port conflict
- Logs filled with: `ERROR: [Errno 98] Address already in use`
- Had to manually kill processes before systemd could take over

**Lesson learned:** Always use `systemctl restart` for systemd-managed services. If you see a PID on a managed port that systemd can't control, kill it first.

### Service Status Quick Check

```bash
# Check both services and ports
systemctl status maymay-backend.service
ps aux | grep "python.*main.py" | grep -v grep
ss -tlnp | grep -E ':(8000|8001)\s'
```

---

Last updated: 2026-02-02
