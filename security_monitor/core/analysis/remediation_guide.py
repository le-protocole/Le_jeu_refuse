"""
Remediation Guide Generator - Security Fix Recommendations
Generates prioritized remediation steps for identified vulnerabilities
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class RemediationStep:
    """Single remediation step"""
    priority: int  # 1-5, 1 being highest
    action: str
    description: str
    estimated_effort: str  # Low, Medium, High
    risk_reduction: int  # 0-100
    resources: List[str]


class RemediationGuide:
    """Generate remediation recommendations"""
    
    # Knowledge base of remediation steps
    REMEDIATION_KB = {
        "missing_ssl": {
            "priority": 1,
            "action": "Install and Configure SSL/TLS Certificate",
            "description": "Obtain an SSL/TLS certificate from a trusted certificate authority and install it on the web server",
            "steps": [
                "1. Purchase or obtain a certificate (Let's Encrypt is free)",
                "2. Install certificate on web server",
                "3. Configure server to use HTTPS on port 443",
                "4. Redirect HTTP traffic to HTTPS",
                "5. Test certificate validity with SSL checker"
            ],
            "estimated_effort": "Medium",
            "risk_reduction": 90,
            "resources": [
                "Let's Encrypt (https://letsencrypt.org)",
                "Mozilla SSL Configuration Generator",
                "OWASP: Transport Layer Protection"
            ]
        },
        "weak_ssl": {
            "priority": 1,
            "action": "Upgrade TLS Version and Cipher Suites",
            "description": "Ensure minimum TLS 1.2+ and remove weak ciphers",
            "steps": [
                "1. Update server configuration to require TLS 1.2 minimum",
                "2. Remove SSLv2, SSLv3, TLS 1.0, TLS 1.1",
                "3. Remove weak ciphers (DES, RC4, MD5-based)",
                "4. Enable only strong ciphers with forward secrecy",
                "5. Test with SSL Labs (https://www.ssllabs.com)"
            ],
            "estimated_effort": "Low",
            "risk_reduction": 85,
            "resources": [
                "Mozilla SSL Configuration Generator",
                "SSL Labs Best Practices",
                "NIST Guidelines on Cryptography"
            ]
        },
        "missing_hsts": {
            "priority": 2,
            "action": "Implement HSTS Header",
            "description": "Add HTTP Strict-Transport-Security header to force HTTPS",
            "steps": [
                "1. Add header: Strict-Transport-Security: max-age=31536000",
                "2. Include subdomains: includeSubDomains",
                "3. Consider preload: preload",
                "4. Start with lower max-age for testing",
                "5. Gradually increase after validation"
            ],
            "estimated_effort": "Low",
            "risk_reduction": 70,
            "resources": [
                "OWASP: HTTP Strict Transport Security",
                "MDN: HSTS Documentation",
                "HSTS Preload List"
            ]
        },
        "missing_csp": {
            "priority": 2,
            "action": "Implement Content Security Policy (CSP)",
            "description": "Add CSP header to prevent XSS attacks",
            "steps": [
                "1. Start with report-only mode: Content-Security-Policy-Report-Only",
                "2. Define default-src policy",
                "3. Restrict script-src to same-origin",
                "4. Disable unsafe-inline and unsafe-eval",
                "5. Monitor reports and refine policy",
                "6. Switch to enforcement mode"
            ],
            "estimated_effort": "Medium",
            "risk_reduction": 75,
            "resources": [
                "OWASP: Content Security Policy",
                "MDN: CSP Documentation",
                "CSP Evaluator Tool"
            ]
        },
        "missing_xfo": {
            "priority": 2,
            "action": "Add X-Frame-Options Header",
            "description": "Prevent clickjacking attacks",
            "steps": [
                "1. Add header: X-Frame-Options: DENY",
                "2. Use SAMEORIGIN if framing is necessary",
                "3. Combine with CSP frame-ancestors directive",
                "4. Test with browser developer tools",
                "5. Verify in all HTTP responses"
            ],
            "estimated_effort": "Low",
            "risk_reduction": 70,
            "resources": [
                "OWASP: Clickjacking",
                "MDN: X-Frame-Options"
            ]
        },
        "exposed_ftp": {
            "priority": 1,
            "action": "Disable or Secure FTP Service",
            "description": "FTP transmits credentials in plaintext - use SFTP/FTPS instead",
            "steps": [
                "1. Audit: Determine FTP usage necessity",
                "2. If needed, replace with SFTP (SSH File Transfer Protocol)",
                "3. Disable FTP service: systemctl disable vsftpd",
                "4. Remove FTP user accounts if no longer needed",
                "5. Use SSH keys instead of passwords",
                "6. Monitor SSH access logs"
            ],
            "estimated_effort": "Medium",
            "risk_reduction": 95,
            "resources": [
                "OWASP: FTP Security",
                "CIS Benchmarks",
                "NIST SP 800-53: AC-2 (Account Management)"
            ]
        },
        "weak_password_policy": {
            "priority": 2,
            "action": "Implement Strong Password Policy",
            "description": "Enforce password complexity and rotation requirements",
            "steps": [
                "1. Require minimum 12-character passwords",
                "2. Require uppercase, lowercase, numbers, and symbols",
                "3. Implement password history (prevent reuse)",
                "4. Enforce password expiration (90 days max)",
                "5. Lock accounts after 5 failed attempts",
                "6. Require MFA for administrative accounts"
            ],
            "estimated_effort": "Low",
            "risk_reduction": 65,
            "resources": [
                "NIST SP 800-63B: Authentication",
                "CIS Password Policy Controls",
                "OWASP: Password Storage Cheat Sheet"
            ]
        },
        "sql_injection_risk": {
            "priority": 1,
            "action": "Prevent SQL Injection Attacks",
            "description": "Use parameterized queries and input validation",
            "steps": [
                "1. Replace all dynamic SQL with parameterized queries",
                "2. Use prepared statements for all database queries",
                "3. Implement input validation and sanitization",
                "4. Use ORM frameworks when possible",
                "5. Run security code review of all SQL code",
                "6. Implement Web Application Firewall (WAF)"
            ],
            "estimated_effort": "High",
            "risk_reduction": 95,
            "resources": [
                "OWASP: SQL Injection Prevention",
                "CWE-89: SQL Injection",
                "NIST: Secure Software Development Framework"
            ]
        },
        "xss_risk": {
            "priority": 1,
            "action": "Prevent Cross-Site Scripting (XSS)",
            "description": "Implement proper output encoding and CSP",
            "steps": [
                "1. Implement Content Security Policy (CSP)",
                "2. HTML-encode all user input before output",
                "3. JavaScript-encode for JavaScript contexts",
                "4. Use templating engines with auto-escaping",
                "5. Avoid eval() and similar functions",
                "6. Implement input validation"
            ],
            "estimated_effort": "High",
            "risk_reduction": 90,
            "resources": [
                "OWASP: XSS Prevention Cheat Sheet",
                "CWE-79: Cross-site Scripting",
                "OWASP Top 10: A03:2021 – Injection"
            ]
        },
        "outdated_software": {
            "priority": 2,
            "action": "Update Software and Dependencies",
            "description": "Apply security patches and upgrade to latest stable versions",
            "steps": [
                "1. Inventory all software and libraries",
                "2. Check for known vulnerabilities (CVE database)",
                "3. Plan updates in testing environment first",
                "4. Apply patches in order of criticality",
                "5. Test functionality after updates",
                "6. Document all changes"
            ],
            "estimated_effort": "Medium",
            "risk_reduction": 80,
            "resources": [
                "NVD: Vulnerability Database",
                "Dependabot for GitHub",
                "OWASP: Dependency Check"
            ]
        },
        "default_credentials": {
            "priority": 1,
            "action": "Change Default Credentials",
            "description": "Replace all default usernames and passwords",
            "steps": [
                "1. Identify all accounts with default credentials",
                "2. Change admin/administrator passwords",
                "3. Change default database passwords",
                "4. Change default service account passwords",
                "5. Disable guest and anonymous accounts",
                "6. Enable MFA for administrative access"
            ],
            "estimated_effort": "Low",
            "risk_reduction": 95,
            "resources": [
                "NIST SP 800-53: AC-2",
                "CIS Benchmark Controls",
                "OWASP: Default Credentials"
            ]
        }
    }
    
    def __init__(self):
        pass
    
    def generate_remediation_plan(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive remediation plan"""
        findings = []
        
        # Analyze scan data for common issues
        issues = self._identify_issues(scan_data)
        
        # Generate remediation steps for each issue
        remediation_steps = []
        total_risk_reduction = 0
        
        for issue in issues:
            if issue in self.REMEDIATION_KB:
                step_data = self.REMEDIATION_KB[issue].copy()
                remediation_steps.append({
                    "issue": issue,
                    "priority": step_data["priority"],
                    "action": step_data["action"],
                    "description": step_data["description"],
                    "steps": step_data["steps"],
                    "estimated_effort": step_data["estimated_effort"],
                    "risk_reduction": step_data["risk_reduction"],
                    "resources": step_data["resources"]
                })
                total_risk_reduction += step_data["risk_reduction"]
        
        # Sort by priority
        remediation_steps.sort(key=lambda x: x["priority"])
        
        return {
            "domain": scan_data.get("domain", "Unknown"),
            "scan_date": scan_data.get("timestamp", "Unknown"),
            "current_risk_score": scan_data.get("risk_score", 0),
            "issues_found": len(remediation_steps),
            "total_risk_reduction_potential": min(total_risk_reduction, 100),
            "estimated_new_risk_score": max(0, scan_data.get("risk_score", 0) - (total_risk_reduction // len(remediation_steps) if remediation_steps else 0)),
            "remediation_steps": remediation_steps,
            "executive_summary": self._generate_summary(remediation_steps)
        }
    
    def _identify_issues(self, scan_data: Dict[str, Any]) -> List[str]:
        """Identify issues from scan results"""
        issues = []
        
        # Check SSL
        ssl_analysis = scan_data.get("ssl_analysis", {})
        if not ssl_analysis.get("certificate_valid"):
            issues.append("missing_ssl")
        if ssl_analysis.get("tls_version"):
            if "TLS 1.0" in str(ssl_analysis.get("tls_version")) or "TLS 1.1" in str(ssl_analysis.get("tls_version")):
                issues.append("weak_ssl")
        
        # Check headers
        headers = scan_data.get("headers_analysis", {})
        if "strict-transport-security" not in str(headers).lower():
            issues.append("missing_hsts")
        if "content-security-policy" not in str(headers).lower():
            issues.append("missing_csp")
        if "x-frame-options" not in str(headers).lower():
            issues.append("missing_xfo")
        
        # Check vulnerabilities
        vulnerabilities = scan_data.get("findings", [])
        for vuln in vulnerabilities:
            vuln_str = str(vuln).lower()
            if "ftp" in vuln_str and "exposed" in vuln_str:
                issues.append("exposed_ftp")
            if "sql" in vuln_str:
                issues.append("sql_injection_risk")
            if "xss" in vuln_str or "cross-site" in vuln_str:
                issues.append("xss_risk")
        
        # Check tech stack for outdated software
        tech_stack = scan_data.get("tech_stack", {})
        if tech_stack:
            issues.append("outdated_software")
        
        return list(set(issues))  # Remove duplicates
    
    def _generate_summary(self, steps: List[Dict[str, Any]]) -> str:
        """Generate executive summary"""
        if not steps:
            return "No significant security issues identified."
        
        critical = sum(1 for s in steps if s["priority"] == 1)
        high = sum(1 for s in steps if s["priority"] == 2)
        medium = sum(1 for s in steps if s["priority"] <= 3)
        
        summary = f"Identified {len(steps)} security issue(s): {critical} critical, {high} high, {medium - high} medium. "
        summary += f"Implementing all recommendations could reduce risk by up to {sum(s['risk_reduction'] for s in steps) // len(steps) if steps else 0}%."
        
        return summary
    
    def generate_roadmap(self, remediation_plan: Dict[str, Any], timeframe: str = "quarterly") -> Dict[str, Any]:
        """Generate implementation roadmap"""
        steps = remediation_plan.get("remediation_steps", [])
        
        # Phase 1: Critical (Priority 1)
        phase1 = [s for s in steps if s["priority"] == 1]
        # Phase 2: High (Priority 2)
        phase2 = [s for s in steps if s["priority"] == 2]
        # Phase 3: Medium (Priority 3)
        phase3 = [s for s in steps if s["priority"] >= 3]
        
        return {
            "domain": remediation_plan.get("domain"),
            "timeframe": timeframe,
            "phases": [
                {
                    "phase": "Phase 1: Critical (Immediate)",
                    "timeline": "1-2 weeks",
                    "items": phase1,
                    "count": len(phase1)
                },
                {
                    "phase": "Phase 2: High Priority",
                    "timeline": "2-4 weeks",
                    "items": phase2,
                    "count": len(phase2)
                },
                {
                    "phase": "Phase 3: Medium Priority",
                    "timeline": "1-3 months",
                    "items": phase3,
                    "count": len(phase3)
                }
            ],
            "total_effort_estimate": self._estimate_effort(steps),
            "success_metrics": [
                "Risk score reduced by 30%+ after Phase 1",
                "All critical vulnerabilities remediated within 2 weeks",
                "Compliance score improved to 70%+",
                "Zero high-severity vulnerabilities remaining"
            ]
        }
    
    def _estimate_effort(self, steps: List[Dict[str, Any]]) -> str:
        """Estimate total implementation effort"""
        effort_scores = {"Low": 1, "Medium": 2, "High": 3}
        total = sum(effort_scores.get(s.get("estimated_effort", "Medium"), 2) for s in steps)
        
        if total <= len(steps):
            return "1-2 weeks"
        elif total <= 2 * len(steps):
            return "2-4 weeks"
        else:
            return "1-3 months"


def generate_remediation(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Quick function to generate remediation plan"""
    guide = RemediationGuide()
    return guide.generate_remediation_plan(scan_data)
