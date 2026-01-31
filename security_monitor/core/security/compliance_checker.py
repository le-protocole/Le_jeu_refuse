"""
Compliance Checker - CIS, OWASP, PCI-DSS Standards
Evaluates website security against major compliance frameworks
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ComplianceCheck:
    """Represents a single compliance check"""
    control_id: str
    control_name: str
    framework: str
    status: str  # PASS, FAIL, PARTIAL, NOT_APPLICABLE
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    evidence: str
    remediation: str


class ComplianceChecker:
    """Check website security against compliance frameworks"""
    
    def __init__(self):
        self.checks = []
    
    def check_cis_controls(self, scan_data: Dict[str, Any]) -> List[ComplianceCheck]:
        """Check CIS (Center for Internet Security) Controls"""
        checks = []
        
        # CIS Control 1: Inventory of Authorized Software
        if "tech_stack" in scan_data and scan_data["tech_stack"].get("server"):
            checks.append(ComplianceCheck(
                control_id="CIS-1",
                control_name="Inventory of Authorized Software",
                framework="CIS",
                status="PASS",
                severity="MEDIUM",
                evidence=f"Server identified: {scan_data['tech_stack'].get('server')}",
                remediation="Maintain inventory of all software in use"
            ))
        
        # CIS Control 3: Data Protection
        ssl_info = scan_data.get("ssl_analysis", {})
        if ssl_info.get("certificate_valid"):
            checks.append(ComplianceCheck(
                control_id="CIS-3",
                control_name="Data Protection",
                framework="CIS",
                status="PASS",
                severity="CRITICAL",
                evidence="Valid SSL certificate found",
                remediation="Continue monitoring SSL/TLS certificate validity"
            ))
        else:
            checks.append(ComplianceCheck(
                control_id="CIS-3",
                control_name="Data Protection",
                framework="CIS",
                status="FAIL",
                severity="CRITICAL",
                evidence="SSL certificate invalid or missing",
                remediation="Install valid SSL/TLS certificate immediately"
            ))
        
        # CIS Control 6: Security Configuration Management
        headers = scan_data.get("headers_analysis", {})
        has_hsts = "strict-transport-security" in str(headers).lower()
        
        if has_hsts:
            checks.append(ComplianceCheck(
                control_id="CIS-6",
                control_name="Security Configuration Management",
                framework="CIS",
                status="PASS",
                severity="HIGH",
                evidence="HSTS header present",
                remediation="Continue enforcing secure HTTP configuration"
            ))
        else:
            checks.append(ComplianceCheck(
                control_id="CIS-6",
                control_name="Security Configuration Management",
                framework="CIS",
                status="PARTIAL",
                severity="HIGH",
                evidence="HSTS header missing",
                remediation="Implement HSTS header with min-age=31536000"
            ))
        
        return checks
    
    def check_owasp_standards(self, scan_data: Dict[str, Any]) -> List[ComplianceCheck]:
        """Check OWASP Top 10 standards"""
        checks = []
        
        # A01: Broken Access Control
        checks.append(ComplianceCheck(
            control_id="OWASP-A01",
            control_name="Broken Access Control",
            framework="OWASP",
            status="NOT_APPLICABLE",
            severity="CRITICAL",
            evidence="Unable to verify from external scan",
            remediation="Review access control implementation and enforce principle of least privilege"
        ))
        
        # A02: Cryptographic Failures
        ssl_info = scan_data.get("ssl_analysis", {})
        tls_version = ssl_info.get("tls_version", "Unknown")
        
        if "TLS 1.2" in str(tls_version) or "TLS 1.3" in str(tls_version):
            checks.append(ComplianceCheck(
                control_id="OWASP-A02",
                control_name="Cryptographic Failures",
                framework="OWASP",
                status="PASS",
                severity="CRITICAL",
                evidence=f"Strong TLS version: {tls_version}",
                remediation="Continue using TLS 1.2+ with strong ciphers"
            ))
        
        # A03: Injection
        checks.append(ComplianceCheck(
            control_id="OWASP-A03",
            control_name="Injection",
            framework="OWASP",
            status="PARTIAL",
            severity="CRITICAL",
            evidence="Input validation not fully testable from external scan",
            remediation="Implement parameterized queries and input validation"
        ))
        
        # A05: Broken Access Control via CORS
        headers = scan_data.get("headers_analysis", {})
        if "access-control-allow-origin" in str(headers).lower():
            checks.append(ComplianceCheck(
                control_id="OWASP-A05",
                control_name="Broken Access Control (CORS)",
                framework="OWASP",
                status="PARTIAL",
                severity="HIGH",
                evidence="CORS headers detected",
                remediation="Restrict CORS to specific, trusted origins"
            ))
        
        # A07: XSS - Check for security headers
        has_csp = "content-security-policy" in str(headers).lower()
        has_xfo = "x-frame-options" in str(headers).lower()
        
        if has_csp and has_xfo:
            checks.append(ComplianceCheck(
                control_id="OWASP-A07",
                control_name="Cross-Site Scripting (XSS)",
                framework="OWASP",
                status="PASS",
                severity="HIGH",
                evidence="CSP and X-Frame-Options headers present",
                remediation="Continue enforcing XSS protection headers"
            ))
        else:
            checks.append(ComplianceCheck(
                control_id="OWASP-A07",
                control_name="Cross-Site Scripting (XSS)",
                framework="OWASP",
                status="PARTIAL",
                severity="HIGH",
                evidence="Missing XSS protection headers",
                remediation="Implement Content-Security-Policy and X-Frame-Options headers"
            ))
        
        return checks
    
    def check_pci_dss(self, scan_data: Dict[str, Any]) -> List[ComplianceCheck]:
        """Check PCI DSS (Payment Card Industry Data Security Standard) compliance"""
        checks = []
        
        # Requirement 2: Change default vendor-supplied passwords
        checks.append(ComplianceCheck(
            control_id="PCI-2",
            control_name="Default Credentials",
            framework="PCI-DSS",
            status="NOT_APPLICABLE",
            severity="CRITICAL",
            evidence="Unable to test from external scan",
            remediation="Disable or change all default accounts and passwords"
        ))
        
        # Requirement 4: Encryption of Data in Transit
        ssl_info = scan_data.get("ssl_analysis", {})
        if ssl_info.get("certificate_valid"):
            checks.append(ComplianceCheck(
                control_id="PCI-4",
                control_name="Encryption of Data in Transit",
                framework="PCI-DSS",
                status="PASS",
                severity="CRITICAL",
                evidence="Valid SSL/TLS certificate present",
                remediation="Continue using minimum TLS 1.2 for all cardholder data"
            ))
        else:
            checks.append(ComplianceCheck(
                control_id="PCI-4",
                control_name="Encryption of Data in Transit",
                framework="PCI-DSS",
                status="FAIL",
                severity="CRITICAL",
                evidence="No valid SSL/TLS certificate",
                remediation="Implement TLS 1.2 or higher immediately"
            ))
        
        # Requirement 6.2: Security Patches
        checks.append(ComplianceCheck(
            control_id="PCI-6.2",
            control_name="Security Patches and Updates",
            framework="PCI-DSS",
            status="PARTIAL",
            severity="HIGH",
            evidence="Outdated software detection not fully available",
            remediation="Ensure all software is current with security patches"
        ))
        
        # Requirement 8: User ID and Access Control
        checks.append(ComplianceCheck(
            control_id="PCI-8",
            control_name="User ID and Access Control",
            framework="PCI-DSS",
            status="NOT_APPLICABLE",
            severity="HIGH",
            evidence="Unable to test from external scan",
            remediation="Implement strong user authentication and access control"
        ))
        
        return checks
    
    def evaluate_all(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate against all compliance frameworks"""
        cis_checks = self.check_cis_controls(scan_data)
        owasp_checks = self.check_owasp_standards(scan_data)
        pci_checks = self.check_pci_dss(scan_data)
        
        all_checks = cis_checks + owasp_checks + pci_checks
        
        # Calculate compliance scores
        cis_score = self._calculate_score(cis_checks)
        owasp_score = self._calculate_score(owasp_checks)
        pci_score = self._calculate_score(pci_checks)
        overall_score = (cis_score + owasp_score + pci_score) / 3
        
        return {
            "cis_controls": [asdict(c) for c in cis_checks],
            "cis_score": cis_score,
            "owasp_standards": [asdict(c) for c in owasp_checks],
            "owasp_score": owasp_score,
            "pci_dss": [asdict(c) for c in pci_checks],
            "pci_score": pci_score,
            "overall_compliance_score": overall_score,
            "total_checks": len(all_checks),
            "passed": sum(1 for c in all_checks if c.status == "PASS"),
            "failed": sum(1 for c in all_checks if c.status == "FAIL"),
            "partial": sum(1 for c in all_checks if c.status == "PARTIAL"),
            "not_applicable": sum(1 for c in all_checks if c.status == "NOT_APPLICABLE")
        }
    
    def _calculate_score(self, checks: List[ComplianceCheck]) -> int:
        """Calculate compliance score as percentage"""
        if not checks:
            return 0
        
        passed = sum(1 for c in checks if c.status == "PASS")
        total_applicable = sum(1 for c in checks if c.status != "NOT_APPLICABLE")
        
        if total_applicable == 0:
            return 0
        
        return int((passed / total_applicable) * 100)
