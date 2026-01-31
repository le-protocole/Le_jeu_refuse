# Security Monitor - Setup Guide

## Quick Start (5 minutes)

### 1. Install Nmap
**Windows:**
```powershell
# Option A: Chocolatey
choco install nmap

# Option B: Download
# https://nmap.org/download.html#windows
```

**Linux:**
```bash
sudo apt-get install nmap
```

**macOS:**
```bash
brew install nmap
```

### 2. Install Python Dependencies
```bash
cd security_monitor
pip install -r requirements.txt
```

### 3. Run Your First Scan
```bash
python main.py example.com quick
```

---

## Project File Structure Explained

```
security_monitor/
│
├── core/
│   ├── config/
│   │   └── settings.py           # System configuration
│   │
│   ├── resolver/
│   │   └── dns.py                # DNS lookup, CDN detection
│   │
│   ├── scanner/
│   │   └── nmap.py               # Nmap wrapper & XML parser
│   │
│   ├── analysis/
│   │   └── rules.py              # Vulnerability rules engine
│   │
│   ├── risk/
│   │   └── scorer.py             # Risk score calculation
│   │
│   ├── fixes/
│   │   └── recommendations.py    # Hardening recommendations
│   │
│   ├── reports/
│   │   └── report.py             # JSON/HTML/TXT generation
│   │
│   └── audit/
│       └── audit.py              # Audit logging
│
├── db/
│   └── database.py               # SQLite management
│
├── cli/
│   └── cli.py                    # Command-line interface
│
├── reports/                      # Generated reports (auto-created)
├── logs/                         # Audit logs (auto-created)
├── db/                          # Database file (auto-created)
│
├── main.py                       # Main orchestrator
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## How Each Module Works

### DNS Resolver (`core/resolver/dns.py`)
**Purpose:** Convert domain names to IPs

**How:**
```python
resolver = DNSResolver()
result = resolver.resolve_domain("example.com")
# Returns: {
#   "ips": ["93.184.216.34"],
#   "cdn": True,
#   "cdn_provider": "Cloudflare",
#   ...
# }
```

**Detects:**
- A records (IPv4)
- AAAA records (IPv6)
- CNAME records
- CDN/proxy services
- MX, NS records

---

### Nmap Scanner (`core/scanner/nmap.py`)
**Purpose:** Discover open ports and services

**Three scan types:**

1. **Quick Scan** (2-5 minutes)
   - Common ports: 22, 80, 443, 3306, etc
   - Best for: Initial assessment

2. **Standard Scan** (5-15 minutes)
   - Top 10,000 ports
   - Service version detection
   - Best for: Most use cases

3. **Thorough Scan** (30+ minutes)
   - All 65,535 ports
   - OS detection
   - Advanced scripting
   - Best for: Deep security audits

**Output:**
```python
{
  "open_ports": [
    {
      "port": 22,
      "service": "ssh",
      "version": "OpenSSH 8.2p1",
      "state": "open"
    },
    ...
  ],
  "filtered_ports": [],
  "closed_ports": []
}
```

---

### Analysis Rules (`core/analysis/rules.py`)
**Purpose:** Detect security issues using static rules

**How it works:**
```python
analyzer = VulnerabilityRules()
findings = analyzer.analyze(scan_data)
# Returns list of Finding objects:
# [{
#   "severity": "CRITICAL",
#   "title": "MySQL exposed",
#   "description": "...",
#   "mitigation": ["Bind to localhost", ...]
# }, ...]
```

**Rules checked:**
- Port 22 (SSH) → password auth vulnerability
- Port 21 (FTP) → insecure protocol
- Port 3306 (MySQL) → database exposure
- Port 5432 (PostgreSQL) → database exposure
- Port 3389 (RDP) → ransomware risk
- Port 445 (SMB) → LAN exposure
- Port 11211 (Memcached) → DDoS amplification
- Port 27017 (MongoDB) → NoSQL injection risk
- Port 6379 (Redis) → unauthenticated access
- Outdated software versions
- No firewall / access restrictions

---

### Risk Scorer (`core/risk/scorer.py`)
**Purpose:** Calculate numerical risk score (0-100)

**How:**
- Each finding has severity weight (CRITICAL=30, HIGH=20, etc)
- Ports/service combinations add multipliers
- Special cases: DB + web = higher risk
- Multiple RPC ports = higher risk
- Both SSH and RDP open = higher risk

**Levels:**
- CRITICAL (81-100): Stop production use
- HIGH (61-80): Fix before deployment  
- MEDIUM (31-60): Plan fixes soon
- LOW (0-30): Address during maintenance

---

### Recommendations (`core/fixes/recommendations.py`)
**Purpose:** Provide actionable hardening steps

**Includes:**
- Step-by-step instructions
- Estimated time to fix
- Difficulty level (EASY/MEDIUM/HARD)
- Impact on security (LOW/MEDIUM/HIGH)
- Tools/skills needed
- Testing/verification steps

**Example:**
```python
Recommendation(
  title="Disable SSH Password Authentication",
  difficulty="EASY",
  impact="HIGH",
  steps=[
    "Connect via SSH",
    "Edit /etc/ssh/sshd_config",
    "Set: PasswordAuthentication no",
    "Restart SSH",
    "Test key auth works"
  ],
  estimated_time="15 minutes"
)
```

---

### Report Generator (`core/reports/report.py`)
**Purpose:** Create comprehensive reports

**Formats:**

1. **JSON** - Machine readable
   ```json
   {
     "metadata": {...},
     "findings": [...],
     "risk_analysis": {...}
   }
   ```

2. **HTML** - Visual, color-coded
   - Severity levels with colors
   - Tables for ports/findings
   - Risk gauge
   - Recommendations

3. **TXT** - Plain text
   - Summary + detailed findings
   - Easy to email/share
   - CLI-friendly

---

### Database (`db/database.py`)
**Purpose:** Store scan history

**Tables:**
- `targets` - Registered assessment targets
- `scans` - Scan execution records
- `findings` - Detected vulnerabilities
- `risk_assessments` - Risk scores
- `reports` - Generated report paths
- `audit_log` - Admin action trail

**Why:**
- Track changes over time
- Compliance documentation
- Trend analysis
- Rollback capability

---

### Audit Logger (`core/audit/audit.py`)
**Purpose:** Create compliance trail

**Logs:**
- Scan start/completion
- Who ran the assessment
- Target and results
- Timestamp
- Status (success/failure)

**Example log:**
```json
{
  "timestamp": "2026-01-31T12:30:45",
  "action": "SCAN_COMPLETED",
  "admin_user": "john.admin",
  "target": "api.example.com",
  "status": "success",
  "details": {
    "findings": 4,
    "risk_level": "MEDIUM",
    "risk_score": 55
  }
}
```

---

## Workflow Diagram

```
User runs: python main.py example.com quick
    ↓
[Main Orchestrator]
    ↓
1. Resolver.resolve_domain("example.com")
   → Returns: {"ips": ["1.2.3.4"], "cdn": true, ...}
    ↓
2. Scanner.quick_scan("1.2.3.4")
   → Runs: nmap -Pn -sS -T4 -p 22,80,443,...
   → Returns: {"open_ports": [...], ...}
    ↓
3. Analyzer.analyze(scan_results)
   → Runs rules against ports/services
   → Returns: [Finding(...), Finding(...), ...]
    ↓
4. RiskScorer.calculate_score(findings)
   → Sums finding weights
   → Returns: {"score": 65, "level": "HIGH", ...}
    ↓
5. RecommendationEngine.get_recommendations()
   → Maps findings to fixes
   → Returns: [Recommendation(...), ...]
    ↓
6. ReportGenerator.generate_full_report()
   → Creates JSON, HTML, TXT
   → Returns: {"json": "path", "html": "path", ...}
    ↓
7. AuditLogger.log()
   → Records action for compliance
   → Stores in audit_log table and file
    ↓
Print Summary → Done
```

---

## Configuration File (`core/config/settings.py`)

Key settings you can modify:

```python
# Nmap execution
NMAP_TIMEOUT = 300                 # Scan timeout in seconds
NMAP_MAX_PARALLELISM = 1          # Run scans sequentially (safe)

# Port scanning
COMMON_PORTS = [22, 80, 443, ...]  # Quick scan targets
DEFAULT_SCAN_TYPE = "quick"        # Default: quick/standard/thorough

# Risk levels
RISK_THRESHOLDS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100)
}

# Database
DATABASE_PATH = BASE_DIR / "db" / "security_monitor.db"

# Report location
REPORT_FORMATS = ["json", "pdf", "html", "txt"]
```

---

## Data Flow Examples

### Example 1: Scanning example.com

```
INPUT: example.com

RESOLVER:
- DNS lookup example.com
- Found: 93.184.216.34
- Not behind CDN
- Output: {"ips": ["93.184.216.34"]}

SCANNER (quick):
- Run: nmap -Pn -sS -T4 -p 22,80,443,... 93.184.216.34
- Found ports: 80, 443
- Output: {
    "open_ports": [
      {"port": 80, "service": "http"},
      {"port": 443, "service": "https"}
    ]
  }

ANALYZER:
- Check port 80: HTTP without HTTPS → Finding (MEDIUM)
- Check port 443: HTTPS (good)
- Output: [
    {
      "severity": "MEDIUM",
      "title": "Unencrypted HTTP",
      ...
    }
  ]

RISK SCORER:
- Count findings: 1 MEDIUM
- Calculate: 10 points = MEDIUM (31-60)
- Output: {"score": 15, "level": "LOW"}

RECOMMENDATIONS:
- Enable HTTPS redirect
- Add HSTS header
- Output: [Recommendation(...)]

REPORTER:
- Generate JSON/HTML/TXT with all data
- Output: {"json": "path/to/report.json", ...}

AUDIT:
- Log: "Scan completed for example.com, 1 finding, LOW risk"

FINAL OUTPUT:
Risk Level: LOW (15/100)
Findings: 1 (1 MEDIUM, 0 HIGH, 0 CRITICAL)
Reports: 3 (JSON, HTML, TXT)
```

---

## Testing

### Test DNS Resolver
```python
from core.resolver.dns import DNSResolver
r = DNSResolver()
print(r.resolve_domain("google.com"))
```

### Test Scanner
```python
from core.scanner.nmap import NmapScanner
s = NmapScanner()
print(s.quick_scan("127.0.0.1"))
```

### Test Rules
```python
from core.analysis.rules import VulnerabilityRules
a = VulnerabilityRules()
findings = a.analyze({"open_ports": [{"port": 3306}]})
print(findings)
```

---

## Performance Notes

- **Quick scan:** 2-5 minutes (most targets)
- **Standard scan:** 5-15 minutes (recommended)
- **Thorough scan:** 30+ minutes (full audit)

Network speed, firewall, and target complexity affect timing.

---

## Security Best Practices

1. **Only assess authorized systems**
2. **Keep audit logs secure**
3. **Restrict access to reports** (contain vulnerabilities)
4. **Run from secure network** (not internet-facing)
5. **Update tools regularly** (Nmap, Python packages)
6. **Document all assessments** (legal protection)
7. **Test in staging first** (if automation planned)

---

**For more details, see [README.md](README.md)**
