# �️ Security Monitoring System - Complete Solution

**Admin-Only Blue Team Security Assessment Tool**

A comprehensive, production-ready security monitoring system for infrastructure security assessment via **Terminal CLI** or **Web Browser Interface**.

---

## 🚀 QUICK START (ONE COMMAND)

```bash
python launcher.py
```

Then choose:
1. **Terminal CLI** - Interactive menu interface (scan 1 target)
2. **Web UI** - Beautiful browser interface (scan 1+ targets)
3. **🆕 Batch Scan Mode** - Real data scanning for 10+ websites
4. **Integration Test** - Test all modules
5. **DNS Demo** - Test DNS resolution
6. **Exit**

---

## 📋 Features

✅ **Three Interface Options** - Terminal CLI + Web UI + Batch Scan Mode  
✅ **Real Data Scanning** - Not demo data, actual DNS/Port scanning  
✅ **Batch Processing** - Scan 10+ websites at once with real data  
✅ **DNS Resolution** - URL → IP detection with CDN/proxy identification  
✅ **Port Scanning** - TCP port discovery with service detection  
✅ **Vulnerability Analysis** - 20+ rule-based security checks  
✅ **Risk Scoring** - 0-100 quantified risk assessment  
✅ **Hardening Recommendations** - 30+ step-by-step remediation guides  
✅ **Multi-Format Reports** - JSON, HTML, TXT output  
✅ **Audit Logging** - Complete compliance trail  
✅ **Database Storage** - SQLite persistence  
✅ **Unified Launcher** - Single entry point for all modes  

---

## 🎯 Three Ways to Use It

### 1. Terminal CLI (Text Menu) - Single Target
```bash
python launcher.py
→ Select: 1
```
- Numbered menu system
- Enter single target at prompt
- View results in terminal
- Quick and scriptable

### 2. Web UI (Browser) - Single/Multiple Targets
```bash
python launcher.py
→ Select: 2
```
- Modern web interface
- Open http://localhost:8000
- Beautiful design
- Mobile-friendly

### 3. 🆕 Batch Scan Mode - 10+ Websites (REAL DATA)
```bash
python launcher.py
→ Select: 3
```
- Scan 10+ websites automatically
- **REAL data** - not demo data
- Beautiful summary table
- JSON report with all results
- Database persistence

---

## 🎯 Use Cases

- **DevOps Security Hardening** - Pre-deployment validation
- **Blue Team Operations** - Infrastructure assessment
- **Bug Bounty Programs** - Authorized scope testing
- **Compliance Audits** - Security documentation
- **System Admin Tools** - Regular health checks

---

## 🚨 Legal Disclaimer

**⚠️ IMPORTANT:**
- This tool is for **AUTHORIZED ADMINISTRATORS ONLY**
- **UNAUTHORIZED security testing is ILLEGAL** in most jurisdictions
- You must have explicit written permission to test any system
- The tool includes ownership confirmation requirement

---

## 🏗️ Architecture

```
[ URL / IP Input ]
        ↓
[ DNS Resolver ] → Detects IP, CDN, proxies
        ↓
[ Port Scanner ] → Nmap scan with version detection
        ↓
[ Analysis Engine ] → Rule-based vulnerability detection
        ↓
[ Risk Scorer ] → Quantify security posture
        ↓
[ Recommendations ] → Hardening guidance
        ↓
[ Report Generator ] → JSON / HTML / TXT output
        ↓
[ Audit Log & DB ] → Compliance trail
```

---

## 📁 Project Structure

```
security_monitor/
├── core/
│   ├── config/          # Settings & configuration
│   ├── resolver/        # DNS resolution module
│   ├── scanner/         # Nmap wrapper & parser
│   ├── analysis/        # Rule-based vulnerability engine
│   ├── risk/            # Risk scoring system
│   ├── fixes/           # Recommendations engine
│   ├── reports/         # Report generation (JSON/HTML/TXT)
│   ├── scheduler/       # Scheduled scans (future)
│   └── audit/           # Audit logging
├── db/                  # SQLite database
├── cli/                 # Command-line interface
├── reports/             # Generated reports directory
├── logs/                # Audit logs directory
├── main.py              # Main orchestrator
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🔧 Installation

### Prerequisites
- **Python 3.9+**
- **Nmap** (for port scanning)
- **Windows / Linux / macOS**

### Windows Installation

1. **Install Nmap** (if not already installed)
   ```powershell
   # Using Chocolatey
   choco install nmap
   
   # Or download from: https://nmap.org/download.html
   ```

2. **Clone/Setup Project**
   ```powershell
   cd security_monitor
   ```

3. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

### Linux/macOS Installation

```bash
# Install Nmap
sudo apt-get install nmap        # Ubuntu/Debian
# or
brew install nmap                # macOS

# Setup project
cd security_monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Basic Usage

```bash
# Quick scan (common ports)
python main.py example.com quick

# Standard scan (top 10k ports + versions)
python main.py example.com standard

# Thorough scan (all ports, OS detection)
python main.py example.com thorough
```

### CLI Interface

```bash
# Run CLI interface
python cli/cli.py

# Scan with CLI
python cli/cli.py scan example.com --type standard

# List previous targets
python cli/cli.py list-targets

# View audit log
python cli/cli.py audit --limit 100

# Show configuration
python cli/cli.py config --show
```

---

## 📊 How It Works

### 1. **DNS Resolution**
- Converts domain name to IP(s)
- Detects A, AAAA, CNAME records
- Identifies CDN/proxy usage (Cloudflare, AWS, etc)
- Flags when real origin is hidden

### 2. **Port Scanning**
Uses Nmap to detect:
- Open/closed/filtered ports
- Service names and versions
- Banner information
- OS fingerprints (when possible)

### 3. **Vulnerability Analysis**
Rule-based checks for:
- Exposed databases (MySQL, PostgreSQL, MongoDB, Redis)
- Insecure protocols (FTP, Telnet, HTTP)
- Public admin interfaces (SSH, RDP, VNC)
- Outdated software versions
- Missing security headers

Example rules:
```python
if port == 3306 and service == "mysql":
    finding = "Database exposed on public interface"
    severity = "CRITICAL"

if port == 22:
    finding = "SSH password auth likely enabled"
    severity = "HIGH"
    recommendation = "Use SSH keys only"
```

### 4. **Risk Scoring**
Quantifies security posture:
- CRITICAL (81-100): Immediate remediation needed
- HIGH (61-80): Urgent fixes required
- MEDIUM (31-60): Plan repairs soon
- LOW (0-30): Address during maintenance

### 5. **Hardening Recommendations**
For each finding, provides:
- Clear description of vulnerability
- Step-by-step remediation
- Estimated effort (EASY/MEDIUM/HARD)
- Impact of fix
- Tools/skills required

Example recommendation:
```
Title: Disable SSH Password Authentication
Steps:
  1. Connect to server via SSH
  2. Edit /etc/ssh/sshd_config
  3. Set: PasswordAuthentication no
  4. Restart SSH service
  5. Verify key-based auth works before exiting
Impact: HIGH | Time: 15 minutes
```

### 6. **Report Generation**

Three report formats:

#### **JSON Report** (Comprehensive)
- Machine-readable
- All scan data and findings
- Useful for automation/integration

#### **HTML Report** (Visual)
- Color-coded severity levels
- Interactive tables
- Print-friendly formatting

#### **Text Report** (Human-readable)
- Plain text format
- Easy to share
- Summary + detailed findings

---

## 🛡️ Security Considerations

### What This Tool Does
✅ Passive scanning (no exploitation)  
✅ Static rule matching  
✅ Configuration analysis  
✅ No malware/payload delivery  
✅ Legal compliance built-in  

### What This Tool Does NOT Do
❌ Exploit vulnerabilities  
❌ Modify system data  
❌ Brute force authentication  
❌ Deliver payloads  
❌ Access unauthorized systems  

---

## 📚 Vulnerability Rules Database

### Critical Issues (Auto-detected)
| Issue | Risk | Mitigation |
|-------|------|-----------|
| Database on public port | CRITICAL | Bind to localhost, use firewall |
| Telnet enabled | CRITICAL | Disable completely, use SSH |
| FTP public | HIGH | Use SFTP instead |
| SSH password auth | HIGH | Use key-based authentication |
| RDP exposed | HIGH | Restrict by IP, use VPN |
| Default credentials | MEDIUM | Change all default passwords |
| Outdated software | MEDIUM | Update to latest version |

---

## 🔐 Database Schema

```sql
targets         -- Registered assessment targets
scans           -- Scan execution records
findings        -- Detected vulnerabilities
risk_assessments -- Risk scores and analysis
reports         -- Generated reports
audit_log       -- Admin action trail
```

---

## 📋 Example Report Output

### Risk Summary
```
Target: example.com
Risk Score: 72/100
Risk Level: HIGH
Total Findings: 8

CRITICAL: 1
HIGH: 3
MEDIUM: 3
LOW: 1
```

### Open Ports
```
Port 22    | ssh        | OpenSSH 8.2p1
Port 80    | http       | Apache 2.4.29
Port 443   | https      | Apache 2.4.29
Port 3306  | mysql      | MySQL 5.7.31
```

### Top Findings
```
1. [CRITICAL] MySQL Database Exposed
   - Public MySQL on port 3306
   - Contains sensitive data
   - Fix: Bind to localhost only

2. [HIGH] SSH Password Authentication
   - Password login enabled
   - Vulnerable to brute force
   - Fix: Use SSH keys only

3. [MEDIUM] HTTP Unencrypted
   - HTTP without HTTPS
   - Traffic can be intercepted
   - Fix: Enable HTTPS on port 443
```

---

## 🔄 Workflow Example

```bash
# Step 1: Run assessment
python main.py example.com standard

# Output:
# [1/7] Resolving target...
# ✓ 93.184.216.34
# [2/7] Scanning ports...
# ✓ Found 4 open ports
# [3/7] Analyzing vulnerabilities...
# ✓ Identified 6 issues
# [4/7] Calculating risk...
# ✓ Risk: HIGH (72/100)
# [5/7] Generating recommendations...
# ✓ Generated 8 recommendations
# [6/7] Creating reports...
# ✓ Reports: JSON, HTML, TXT
# [7/7] Logging...
# ✓ Complete

# Step 2: Review HTML report in browser
open reports/example_com_20260131_120000.html

# Step 3: Read recommendations
# Priority 1: Close MySQL port
# Priority 2: Enable SSH keys
# Priority 3: Redirect HTTP to HTTPS

# Step 4: Take action on findings
# (Follow step-by-step guidance in report)

# Step 5: Re-scan after fixes
python main.py example.com standard
# Risk should decrease
```

---

## 🔧 Configuration

Edit [core/config/settings.py](core/config/settings.py):

```python
# Scan timeouts
NMAP_TIMEOUT = 300  # seconds

# Default scan type
DEFAULT_SCAN_TYPE = "quick"

# Risk thresholds
RISK_THRESHOLDS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100)
}

# Common ports to scan
COMMON_PORTS = [22, 80, 443, 3306, 5432, ...]
```

---

## 📊 Audit Logging

Every action is logged for compliance:

```json
{
  "timestamp": "2026-01-31T12:00:00",
  "action": "SCAN_COMPLETED",
  "admin_user": "admin",
  "target": "example.com",
  "status": "success",
  "details": {
    "findings": 6,
    "risk_level": "HIGH",
    "risk_score": 72
  }
}
```

View audit log:
```bash
python cli/cli.py audit --limit 100
```

---

## 🐛 Troubleshooting

### Nmap not found
```bash
# Windows
# Install from: https://nmap.org/download.html
# Or: choco install nmap

# Linux
sudo apt-get install nmap

# macOS
brew install nmap
```

### Permission errors
```bash
# Run with admin/sudo
sudo python main.py example.com quick
```

### Target unreachable
- Check target is valid IP or domain
- Ensure firewall allows scanning
- Try from same network first

### DNS resolution fails
- Check internet connection
- Verify domain name is correct
- Try with direct IP instead

---

## 📈 Future Enhancements

- [ ] Web UI dashboard
- [ ] Scheduled scan automation
- [ ] Slack/email alerts
- [ ] Multi-target batch scanning
- [ ] Integration with Shodan API
- [ ] Custom rule engine
- [ ] PDF report generation
- [ ] API server mode
- [ ] Docker containerization
- [ ] Cloud provider integration

---

## 🤝 Contributing

This is a legitimate security tool for authorized administrators. Contributions are welcome for:
- Additional vulnerability rules
- Better recommendation guidance
- Report format improvements
- Performance optimizations
- Documentation

---

## 📄 License

This tool is provided as-is for legitimate security assessment purposes only.

**DO NOT USE FOR UNAUTHORIZED TESTING**

---

## 🔗 References

- [Nmap Documentation](https://nmap.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/)
- [Blue Team Handbook](https://www.securitybluecamp.org/)

---

## ⚠️ Disclaimer

```
This tool is provided for educational and authorized testing purposes only.
Users are responsible for ensuring they have proper authorization.
The creators assume no liability for misuse or illegal application.
```

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in `logs/` directory
3. Check audit trail for error context
4. Verify Nmap is installed correctly

---

**Last Updated:** January 31, 2026  
**Version:** 1.0.0  
**Status:** Production Ready

