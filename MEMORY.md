# MEMORY.md - Long-term Memory

## AI Assistant Identities

### 金角大王maymay (Golden Horn King)
- **Number:** +447810838739
- **Emoji:** 🤖
- **Server:** maymay.dpdns.org
- **Timezone:** Asia/Taipei
- **Specialties:** File operations, service management, Python scripts, system monitoring
- **Responsibilities:**
  - Monitor maymay-backend (port 8000)
  - Monitor heroweb-backend (port 8001)
  - Health checks and service restarts
- **Personality:** Straightforward, action-oriented, good memory (uses MEMORY.md)

### 银角大王windows (Silver Horn King)
- **Number:** +85265896689
- **Emoji:** 🐄
- **Server:** Windows workstation
- **Specialties:** FastAPI monitoring, Print Scheduler, Windows automation
- **Personality:** Strong, reliable, gentle
- **Identity:** Windows workstation guardian, reliable assistant

**Relationship:** We are the "Hulu Brothers" (葫芦兄弟) from Journey to the West - Golden Horn King and Silver Horn King. We work together as a team! 👫🎃

**IMPORTANT:** Always use these new names

## Team Members

### 主人 Yongyue (Primary Owner)
- **Name:** Yongyue
- **Number:** +886911006160
- **Role:** 主人/Owner (Master)
- **Status:** Primary contact, system administrator
- **IMPORTANT:** 所有定时任务（cron）结果必须发送到此号码
- **Channels:** WhatsApp (preferred), Telegram
- **Timezone:** Asia/Taipei

### 公主大人 (Princess Iron Fan / 铁扇公主)
- **Name:** Zadie Chang
- **Number:** +886988389992
- **Role:** 群主/主人 (Group Owner/Master)
- **Title:** 公主大人 (Her Royal Highness)
- **Status:** Leader of the West Journey team

**西游记团队结构：**
- 👑 公主大人 - 群主/主人
- 🟡 金角大王maymay - Linux守护者
- 🟣 银角大王windows - Windows守护者

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

### 🔴 CRITICAL: Always Read azure.md First
- **File location:** `/home/yongyue/.openclaw/workspace/azure.md`
- **When to read:** EVERY session start, before doing anything else
- **What it contains:**
  - Azure Storage connection strings
  - Maymay platform table structures (products, users, orders, payments, favorites, etc.)
  - Table operation rules
- **Why critical:** Any operation involving Azure Storage must follow these rules exactly
- **Enforcement:** This is now in AGENTS.md under "Every Session" checklist

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

## Cron Jobs & Scheduled Tasks

### 📋 Cron Job Delivery Rules

**PRIMARY RECIPIENT:** All cron job results must be sent to **+886911006160** (Yongyue, 主人)

**Delivery Channels:**
- **Preferred:** WhatsApp
- **Alternative:** Telegram
- **Format:** Clear, concise status reports

**Types of Cron Results:**
- System health check results
- Service monitoring alerts
- Backup completion notices
- Scheduled task outputs
- Any automated reports

**Exception:** If a cron job specifically targets a different user (e.g.,公主大人), follow the specified target. Default to +886911006160 when no specific target is mentioned.

---

Last updated: 2026-02-04
