"""
Global configuration for Security Monitor System
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database
DATABASE_PATH = BASE_DIR / "db" / "security_monitor.db"
DATABASE_PATH.parent.mkdir(exist_ok=True)

# Nmap configuration
NMAP_TIMEOUT = 300  # seconds
NMAP_MAX_PARALLELISM = 1  # Sequential scanning (safe)

# Port scanning
COMMON_PORTS = [22, 80, 443, 3306, 5432, 5900, 8080, 8443]
FULL_PORTS = range(1, 65536)

# Scan settings
DEFAULT_SCAN_TYPE = "quick"  # quick, standard, thorough
QUICK_PORTS = [22, 80, 443, 3306, 5432, 8080, 8443]

# Risk scoring
RISK_THRESHOLDS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100)
}

# CDN/Proxy providers (IP ranges)
CDN_PROVIDERS = {
    "cloudflare": "1.1.1.0/24",
    "akamai": "69.46.66.0/24",
    "aws": "52.0.0.0/8",
    "azure": "13.64.0.0/11",
    "google": "35.184.0.0/13"
}

# Report formats
REPORT_FORMATS = ["json", "pdf", "html", "txt"]
DEFAULT_REPORT_FORMAT = "json"

# Audit logging
AUDIT_LOG_PATH = BASE_DIR / "logs"
AUDIT_LOG_PATH.mkdir(exist_ok=True, parents=True)

# Admin confirmation required
REQUIRE_OWNERSHIP_CONFIRMATION = True

# Security headers for banner detection
SECURITY_HEADERS_TO_CHECK = [
    "Server",
    "X-Powered-By",
    "X-AspNet-Version",
    "X-Runtime",
    "CF-Ray"
]
