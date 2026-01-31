#!/usr/bin/env python3
"""
QUICK START GUIDE - How to use the Interactive System
"""

INSTRUCTIONS = """
================================================================================
  SECURITY MONITORING SYSTEM - QUICK START GUIDE
================================================================================

1. START INTERACTIVE MODE
   Command: python interactive.py
   
   This opens the main menu where you can:
   
   MAIN MENU:
   1. Scan a website or IP address
   2. View previous scan results
   3. Generate security report
   4. View vulnerability database
   5. System settings & configuration
   6. Exit

2. SCANNING WORKFLOW (Option 1)
   
   When you choose "1. Scan a website or IP address":
   
   Step 1: Enter target
     → Enter target URL or IP address: google.com
     → (System resolves DNS, detects CDN, etc.)
   
   Step 2: Choose scan type
     → 1. Quick scan (2 minutes)
     → 2. Standard scan (10 minutes)  
     → 3. Deep scan (30 minutes)
   
   Step 3: Confirm
     → Start scan? (yes/no): yes
   
   Step 4: View results
     → Open ports found
     → Vulnerabilities detected
     → Risk score calculated
     → Report generated
   
3. EXAMPLE USAGE
   
   Interactive Session:
   
   Enter your choice (1-6): 1
   
   Enter target URL or IP address: example.com
   ✓ Resolved: example.com
   IP Address: 104.18.27.120
   [!] Behind CDN: Unknown (HTTP header detected)
   
   SELECT SCAN TYPE:
   1. Quick scan (fast, common ports only) - ~2 minutes
   2. Standard scan (thorough, top 10k ports) - ~10 minutes
   3. Deep scan (comprehensive, all ports) - ~30 minutes
   
   Choose scan type (1-3): 1
   
   SCAN SUMMARY:
   Target: example.com (104.18.27.120)
   Scan Type: Quick Scan
   CDN: Yes
   
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
   ✓ Report saved: reports/example.com_20260201_143022.json
   
   SCAN COMPLETE
   ========================
   Target: example.com (104.18.27.120)
   Open Ports: 2
   Vulnerabilities: 1
   Risk Level: LOW
   Report: reports/example.com_20260201_143022.json
   ========================

4. VIEWING RESULTS (Option 2)
   
   View all previous reports in reports/ folder
   Each report contains:
   - Target and IP address
   - CDN detection
   - Open ports
   - Vulnerabilities found
   - Risk score
   - Recommendations

5. SYSTEM ARCHITECTURE
   
   URL/IP Input
        ↓
   DNS Resolution (resolve domain, detect CDN)
        ↓
   Port Scanning (discover open ports)
        ↓
   Vulnerability Analysis (check for security issues)
        ↓
   Risk Scoring (calculate 0-100 risk score)
        ↓
   Generate Recommendations (hardening advice)
        ↓
   Generate Report (JSON, HTML, TXT)
        ↓
   Store in Database (persistence)

6. COMMAND REFERENCE
   
   Start Interactive Mode:
   $ python interactive.py
   
   Run Integration Test:
   $ python integration_test.py
   
   Run DNS Demo:
   $ python demo_dns.py
   
   View Database:
   $ sqlite3 db/security_monitor.db
   
   View Reports:
   $ ls reports/

7. FEATURES
   
   ✓ URL & IP resolution with CDN detection
   ✓ Port scanning (TCP, service detection)
   ✓ Vulnerability analysis (20+ rules)
   ✓ Risk scoring (0-100 scale)
   ✓ Hardening recommendations (30+ guides)
   ✓ Multi-format reporting (JSON, HTML, TXT)
   ✓ Database persistence
   ✓ Audit logging for compliance
   ✓ Admin-only access
   ✓ Ownership confirmation

8. NOTES
   
   • System is admin-only by design
   • Requires ownership confirmation for scanning
   • Nmap must be installed for port scanning
   • Reports are saved in reports/ folder
   • Database persists all scan history
   • Audit logs track all actions

================================================================================
  Questions? Run: python interactive.py
================================================================================
"""

if __name__ == "__main__":
    print(INSTRUCTIONS)
