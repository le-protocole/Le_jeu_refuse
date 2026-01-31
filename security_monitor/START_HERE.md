# 🚀 START HERE - Security Monitor Launcher

## ONE COMMAND TO START EVERYTHING

```bash
python launcher.py
```

---

## What You'll See

```
╔════════════════════════════════════════════╗
║  SECURITY MONITOR - MAIN MENU             ║
║  Version 1.0 - Production Ready           ║
╚════════════════════════════════════════════╝

SELECT YOUR MODE:

  1. 🖥️  Terminal CLI Interface
         • Interactive numbered menu
         • Text-based results
         • Best for: Scripts & automation

  2. 🌐 Web Browser Interface
         • Beautiful modern UI
         • Visual results with colors
         • Best for: Manual scanning & reports

  3. 🧪 Integration Test
         • Test all 8 modules
         • Full 7-step workflow demo
         • Best for: Verification

  4.  Quick DNS Test
         • Test DNS resolution
         • Test CDN detection
         • Best for: Diagnostics

  5. ❌ Exit

─────────────────────────────────────────────
Choose option (1-5): 
```

---

## Quick Decision Guide

### Want to scan from Terminal? 
→ **Select: 1 (Terminal CLI)**

```
You'll see:
  • "Enter target URL or IP:"
  • "Select scan type (1-3):"
  • Results in terminal
  • Report saved automatically
```

### Want to use Web Browser?
→ **Select: 2 (Web UI)**

```
You'll see:
  • Beautiful web interface opens
  • Enter target in browser
  • Click "Start Scan"
  • Beautiful colored results
  • Access: http://localhost:8000
```

### Want to verify everything works?
→ **Select: 3 (Integration Test)**

```
You'll see:
  • Automated test of all modules
  • Tests 3 domains
  • Shows all 8 components working
  • Best for: First-time verification
```

### Want to test DNS only?
→ **Select: 4 (Quick DNS Test)**

```
You'll see:
  • Test DNS resolution
  • Test CDN detection
  • Enter any domain
  • Fast diagnostics
```

---

## Choose Your Path

### Path 1: Terminal User
```bash
1. Run: python launcher.py
2. Select: 1 (Terminal CLI)
3. Enter target: google.com
4. Select scan: 1 (Quick)
5. View results in terminal
```

### Path 2: Web Browser User
```bash
1. Run: python launcher.py
2. Select: 2 (Web UI)
3. Browser opens automatically to http://localhost:8000
4. Enter target in web form
5. Click "Start Scan"
6. View beautiful results
```

### Path 3: Verification First
```bash
1. Run: python launcher.py
2. Select: 3 (Integration Test)
3. Watch automated test run
4. Verify all systems working
5. Then choose Terminal or Web mode
```

---

## System Requirements

✅ **Python:** 3.9+  
✅ **Installed:** All dependencies pre-installed  
✅ **Database:** SQLite (pre-configured)  
✅ **Optional:** Nmap (for enhanced port scanning)  

---

## File Locations

```
Reports:     reports/
Database:    db/security_monitor.db
Logs:        logs/
Config:      core/config/
```

---

## Next Steps

### First Time?
1. Run: `python launcher.py`
2. Select: `3` (Integration Test) - to verify everything
3. Then try: `1` (Terminal) or `2` (Web)

### Ready to Scan?
1. Run: `python launcher.py`
2. Select: `1` or `2` based on your preference
3. Follow the prompts!

### Need Help?
- Read: `README.md` - Overview & features
- Read: `COMPLETE_GUIDE.md` - Comprehensive manual
- Run: `python QUICK_START.py` - Interactive guide

---

## Common Tasks

### Scan google.com via Terminal
```bash
python launcher.py
→ 1 (Terminal CLI)
→ Target: google.com
→ Scan type: 1 (Quick)
→ Confirm: yes
```

### Scan google.com via Web
```bash
python launcher.py
→ 2 (Web UI)
→ Browser opens to http://localhost:8000
→ Enter: google.com
→ Click: Start Scan
```

### Verify System Works
```bash
python launcher.py
→ 3 (Integration Test)
→ Watch automated test
→ All 8 modules tested
```

### Test DNS Only
```bash
python launcher.py
→ 4 (DNS Demo)
→ Enter domain
→ See DNS + CDN info
```

---

## Architecture

```
┌─────────────────┐
│  launcher.py    │ ← You are here
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────┬───────┐
    │          │          │      │       │
    v          v          v      v       v
 ┌────────┐ ┌─────┐ ┌────────┐ ┌────┐ ┌─────┐
 │Terminal│ │ Web │ │  Test  │ │ DNS│ │Exit │
 │  CLI   │ │ UI  │ │ Suite  │ │    │ │     │
 └────────┘ └─────┘ └────────┘ └────┘ └─────┘
    ↓          ↓         ↓       ↓
 interactive web_server  ...   demo_dns
   .py      .py                .py
```

---

## You Are Ready! 🎯

```bash
python launcher.py
```

**That's it!** Everything is configured and ready to use.

Choose your interface, enter a target, and start scanning! 🚀

---

## Support

- **Questions?** Read `README.md`
- **Detailed guide?** Read `COMPLETE_GUIDE.md`
- **System info?** Run `python DELIVERY_SUMMARY.py`
- **Interactive guide?** Run `python QUICK_START.py`

