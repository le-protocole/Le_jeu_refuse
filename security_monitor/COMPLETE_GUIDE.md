# 🛡️ SECURITY MONITORING SYSTEM - COMPLETE GUIDE

## Quick Start

### Option 1: Terminal CLI (Interactive Menu)
```bash
python interactive.py
```

**Features:**
- Numbered menu (1-6 options)
- Input prompts for target URL/IP
- Scan type selection (Quick/Standard/Deep)
- Real-time progress display
- Detailed results with risk scores
- Report generation

**Workflow:**
```
Main Menu
  ↓
1. Enter target (google.com)
  ↓
2. Choose scan type
  ↓
3. Confirm start
  ↓
4. View results (Risk Score, Ports, Vulnerabilities)
  ↓
5. Report saved
```

---

### Option 2: Web UI (FastAPI + Browser)
```bash
python web_server.py
```

**Access:**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

**Features:**
- Modern web interface
- Real-time scanning
- Visual risk indicators
- Previous reports history
- API-based backend

**Workflow:**
```
Browser → http://localhost:8000
  ↓
Enter target URL
  ↓
Select scan type
  ↓
Click "Start Scan"
  ↓
View results (colors, risk meter)
  ↓
View Full Report (JSON)
```

---

## Full System Architecture

### 1. DNS Resolution
```
URL Input: https://google.com/
    ↓
Sanitize: google.com
    ↓
Resolve: 142.250.197.110 (IPv4)
          2404:6800:4005:81b::200e (IPv6)
    ↓
Check CDN: No
```

### 2. Port Scanning
```
IP: 142.250.197.110
    ↓
Scan: TCP ports (Nmap)
    ↓
Results:
  - Port 80: open (http)
  - Port 443: open (https)
```

### 3. Vulnerability Analysis
```
Open Ports Data
    ↓
Apply Rules (20+ checks)
    ↓
Findings:
  - SSH password auth → HIGH
  - MySQL public → CRITICAL
  - RDP open → HIGH
```

### 4. Risk Scoring
```
Findings Count + Severity
    ↓
Calculate Score (0-100)
    ↓
Risk Levels:
  - 0-30: LOW
  - 31-60: MEDIUM
  - 61-80: HIGH
  - 81-100: CRITICAL
```

### 5. Recommendations
```
Each Finding
    ↓
Get Fix Steps (30+ templates)
    ↓
Output:
  - Disable SSH password auth
  - Bind database to localhost
  - Enable firewall
```

### 6. Report Generation
```
All Data
    ↓
Generate Formats:
  - JSON (machine-readable)
  - HTML (visual)
  - TXT (email-friendly)
    ↓
Store in Database
```

---

## File Structure

```
security_monitor/
├── core/
│   ├── config/
│   │   └── settings.py          # Configuration
│   ├── resolver/
│   │   └── dns.py               # DNS resolution + CDN detection
│   ├── scanner/
│   │   └── nmap.py              # Port scanning wrapper
│   ├── analysis/
│   │   └── rules.py             # 20+ vulnerability rules
│   ├── risk/
│   │   └── scorer.py            # Risk scoring (0-100)
│   ├── fixes/
│   │   └── recommendations.py   # 30+ hardening guides
│   ├── reports/
│   │   └── report.py            # Report generation
│   └── audit/
│       └── audit.py             # Compliance logging
├── db/
│   └── database.py              # SQLite persistence
├── cli/
│   └── cli.py                   # CLI interface
├── interactive.py               # Terminal menu system
├── web_server.py                # FastAPI web server
├── integration_test.py          # Full system test
├── demo_dns.py                  # DNS demo
└── reports/                     # Generated reports (JSON)
```

---

## Usage Examples

### Terminal CLI - Step by Step

```bash
$ python interactive.py

================================================================================
  SECURITY MONITORING SYSTEM - INTERACTIVE MODE
================================================================================

MAIN MENU - Choose an option:
1. Scan a website or IP address
2. View previous scan results
3. Generate security report
4. View vulnerability database
5. System settings & configuration
6. Exit

Enter your choice (1-6): 1

================================================================================
  SCAN TARGET - Website or IP Address
================================================================================

Enter target URL or IP address: google.com

  Resolving: google.com...
  ✓ Resolved: google.com
    IP Address: 142.250.197.110
    [!] Behind CDN: No

SELECT SCAN TYPE:
1. Quick scan (fast, common ports only) - ~2 minutes
2. Standard scan (thorough, top 10k ports) - ~10 minutes
3. Deep scan (comprehensive, all ports) - ~30 minutes

Choose scan type (1-3): 1

SCAN SUMMARY:
Target: google.com (142.250.197.110)
Scan Type: Quick Scan
CDN: No

Start scan? (yes/no): yes

Running quick scan...
✓ Scan complete! Found 2 open port(s)
  → Port 80: open (http)
  → Port 443: open (https)

Analyzing vulnerabilities...
✓ Found 1 issue(s)
  → [LOW] No public services detected

Calculating risk score...
✓ Risk Score: 3/100 (LOW)

Generating recommendations...
✓ Generated 0 recommendation(s)

Generating report...
✓ Report saved: reports/google.com_20260201_143022.json

================================================================================
  SCAN COMPLETE
================================================================================
Target: google.com (142.250.197.110)
Open Ports: 2
Vulnerabilities: 1
Risk Level: LOW
Report: reports/google.com_20260201_143022.json
================================================================================
```

### Web UI - Browser

1. **Start Server:**
   ```bash
   python web_server.py
   ```
   Output:
   ```
   ================================================================================
     SECURITY MONITORING SYSTEM - WEB SERVER
   ================================================================================
   
   [*] Starting FastAPI server...
   
   Web Interface: http://localhost:8000
   API Docs: http://localhost:8000/docs
   Status: http://localhost:8000/api/health
   ```

2. **Open Browser:**
   - Visit: http://localhost:8000
   - Enter: `google.com`
   - Select: `Quick Scan`
   - Click: `Start Scan`

3. **View Results:**
   - Risk Score: 3/100
   - Risk Level: LOW (green)
   - Open Ports: 2
   - Vulnerabilities: 1

---

## Commands Reference

### Terminal Mode
```bash
# Start interactive CLI
python interactive.py

# Run integration test
python integration_test.py

# Quick DNS test
python demo_dns.py

# Show quick start guide
python QUICK_START.py
```

### Web Server
```bash
# Start web server (port 8000)
python web_server.py

# Access in browser
http://localhost:8000
http://localhost:8000/docs  # API documentation
```

### Database
```bash
# View database
sqlite3 db/security_monitor.db
sqlite> SELECT * FROM targets;
sqlite> SELECT * FROM scans;
```

### Reports
```bash
# List all reports
ls reports/

# View specific report
cat reports/google.com_report.json
```

---

## API Endpoints (Web Server)

### Start Scan
```bash
POST /api/scan
Content-Type: application/json

{
  "target": "google.com",
  "scan_type": "quick"  # quick, standard, thorough
}

Response:
{
  "target": "google.com",
  "ip_address": "142.250.197.110",
  "behind_cdn": false,
  "open_ports": 2,
  "vulnerabilities": 1,
  "risk_score": 3,
  "risk_level": "LOW",
  "report_file": "reports/google.com_report.json"
}
```

### List Reports
```bash
GET /api/reports

Response:
{
  "reports": [
    {
      "file": "google.com_report.json",
      "target": "google.com",
      "ip": "142.250.197.110",
      "risk_score": 3,
      "risk_level": "LOW",
      "scan_date": "2026-02-01T14:30:22"
    }
  ]
}
```

### Get Report
```bash
GET /api/report/{report_name}

Response: Full report JSON
```

### Health Check
```bash
GET /api/health

Response:
{
  "status": "ok",
  "version": "1.0"
}
```

---

## Features Comparison

| Feature | Terminal CLI | Web UI |
|---------|-------------|--------|
| Interactive Menu | ✅ | ✅ |
| Scan Target | ✅ | ✅ |
| View Reports | ✅ | ✅ |
| Risk Score | ✅ | ✅ |
| Recommendations | ✅ | ✅ |
| Database Persistence | ✅ | ✅ |
| User Friendly | ✅ | ✅ |
| Beautiful UI | ❌ | ✅ |
| Mobile Friendly | ❌ | ✅ |
| API Endpoints | ❌ | ✅ |

---

## Troubleshooting

### Nmap Not Found
```
Error: Nmap not available
Solution: Install Nmap from https://nmap.org/download.html
```

### Module Import Error
```
Error: ModuleNotFoundError
Solution: Install dependencies:
  pip install dnspython requests typer rich jinja2 reportlab fastapi uvicorn
```

### Port Already in Use
```
Error: Address already in use (port 8000)
Solution: Change port in web_server.py:
  uvicorn.run(app, host="0.0.0.0", port=8001)
```

---

## Security Notes

✅ Admin-only system (no user login required)  
✅ Ownership confirmation for targets  
✅ No exploitation code (rule-based analysis only)  
✅ Audit logging for compliance  
✅ SQLite database for data persistence  
✅ Safe mode by default  

---

## Next Steps

1. **Install Nmap** (for full port scanning):
   - Download: https://nmap.org/download.html
   - Verify: `nmap --version`

2. **Customize Rules** (add more vulnerability checks):
   - Edit: `core/analysis/rules.py`
   - Add custom detection logic

3. **Deploy** (production use):
   - Run web server on dedicated port
   - Add SSL/TLS certificate
   - Set up scheduled scans (cron)

4. **Integrate** (with other tools):
   - Use API endpoints for automation
   - Parse JSON reports for processing
   - Connect to SIEM/monitoring

---

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. View audit trail: `db/security_monitor.db`
3. Review generated reports in `reports/`

---

**Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** February 1, 2026
