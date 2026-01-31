"""
Rule Confidence Scoring - Confidence levels for findings
Professional Finding Wording - Enterprise-grade descriptions
Scan Policy Engine - Control scan behavior
"""

from enum import Enum
from typing import Dict, List

class Confidence(Enum):
    """Confidence levels for findings"""
    DEFINITE = 0.95  # 95-100%
    HIGH = 0.85      # 85-95%
    MEDIUM = 0.70    # 70-85%
    LOW = 0.50       # 50-70%
    UNCERTAIN = 0.30 # 30-50%

class RuleConfidenceScorer:
    """Score confidence of each finding"""
    
    def score_finding(self, finding: Dict) -> Dict:
        """
        Add confidence score to finding
        
        Returns finding with:
        {
            "title": "...",
            "severity": "HIGH",
            "confidence": 0.85,
            "confidence_level": "HIGH",
            "confidence_reasons": [...]
        }
        """
        
        confidence_score = 0.5
        reasons = []
        
        # Open port detection = high confidence
        if "port" in finding and finding["port"]:
            confidence_score = 0.95
            reasons.append("Port actively responding")
        
        # Service detection from banner = high confidence
        if finding.get("detection_method") == "banner_grab":
            confidence_score = 0.90
            reasons.append("Service identified via banner grab")
        
        # Version detection = high confidence
        if finding.get("version"):
            confidence_score = 0.85
            reasons.append(f"Service version confirmed: {finding.get('version')}")
        
        # Known vulnerability (CVE) = definite
        if "cve" in finding:
            confidence_score = 0.95
            reasons.append(f"Known vulnerability: {finding.get('cve')}")
        
        # Missing headers = medium-high
        if "header" in finding:
            confidence_score = 0.75
            reasons.append("Security header analysis")
        
        # Weak crypto = high
        if "cipher" in finding or "ssl" in finding:
            confidence_score = 0.80
            reasons.append("Cryptographic analysis")
        
        # Add to finding
        finding["confidence"] = confidence_score
        finding["confidence_level"] = self._get_confidence_level(confidence_score)
        finding["confidence_reasons"] = reasons
        
        return finding
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert score to level name"""
        if score >= 0.90:
            return "DEFINITE"
        elif score >= 0.80:
            return "HIGH"
        elif score >= 0.65:
            return "MEDIUM"
        elif score >= 0.50:
            return "LOW"
        else:
            return "UNCERTAIN"


class ProfessionalWording:
    """Generate professional, enterprise-grade finding descriptions"""
    
    # Mapping from technical findings to professional wording
    PROFESSIONAL_DESCRIPTIONS = {
        "No public services detected": "Only standard web services exposed (HTTP/HTTPS)",
        "Open port 22": "SSH service available on standard port",
        "No open ports": "No additional services detected beyond web interface",
        "Missing security header": "Recommended security header not implemented",
        "Weak SSL": "SSL/TLS configuration requires hardening",
        "Outdated service": "Service version should be updated",
        "CDN": "Content delivery network in use - managed security provider",
    }
    
    def professionalize(self, finding: Dict) -> Dict:
        """
        Convert technical finding to professional wording
        
        Before: "No public services detected"
        After: "Only standard web services exposed (HTTP/HTTPS) - appropriate for web application"
        """
        
        title = finding.get("title", "")
        severity = finding.get("severity", "INFO")
        
        # Replace generic wording
        if title == "No public services detected":
            finding["title"] = "Minimal service exposure"
            finding["description"] = "Only standard web services (HTTP/HTTPS) are exposed. This is appropriate security posture for a web application."
            finding["business_impact"] = "Reduced attack surface"
        
        elif "open port" in title.lower():
            port = finding.get("port", "unknown")
            service = finding.get("service", "service")
            finding["title"] = f"Network service identified: {service}"
            finding["description"] = f"Port {port}/{finding.get('protocol', 'tcp')} is actively serving {service}. This is expected and operational."
            finding["business_impact"] = "Normal operation"
        
        elif "missing" in title.lower() and "header" in title.lower():
            header = finding.get("header", "header")
            finding["title"] = f"Security header enhancement: {header}"
            finding["description"] = f"The {header} header is not currently implemented. Consider adding for defense-in-depth."
            finding["business_impact"] = "Minor - recommended but not critical"
        
        elif "ssl" in title.lower() or "tls" in title.lower():
            if "weak" in title.lower():
                finding["title"] = "SSL/TLS configuration hardening recommended"
                finding["description"] = "Current SSL/TLS configuration uses supported but older standards. Consider upgrading to TLSv1.3."
                finding["business_impact"] = "Medium - affects encryption strength"
            else:
                finding["title"] = "SSL/TLS properly configured"
                finding["description"] = "Secure communication channels are properly implemented."
                finding["business_impact"] = "Positive"
        
        elif "cdn" in title.lower():
            finding["title"] = "CDN/Shared hosting platform detected"
            finding["description"] = "Target is served through a content delivery network or shared hosting platform. This provides additional DDoS protection and performance optimization."
            finding["business_impact"] = "Positive - enhanced security and performance"
        
        # Add confidence context
        if finding.get("confidence"):
            finding["confidence_note"] = f"Finding confidence: {finding.get('confidence_level')} ({finding.get('confidence', 0):.0%})"
        
        return finding
    
    def get_bullet_summary(self, findings: List[Dict]) -> List[str]:
        """Generate professional bullet point summary"""
        
        bullets = []
        
        # Categorize
        critical = [f for f in findings if f.get("severity") == "CRITICAL"]
        high = [f for f in findings if f.get("severity") == "HIGH"]
        medium = [f for f in findings if f.get("severity") == "MEDIUM"]
        
        # Generate bullets
        if critical:
            bullets.append(f"• {len(critical)} critical issue(s) requiring immediate attention")
        
        if high:
            bullets.append(f"• {len(high)} high-priority finding(s)")
        
        if medium:
            bullets.append(f"• {len(medium)} medium-priority enhancement(s)")
        
        if not bullets:
            bullets.append("• No significant security issues detected")
        
        return bullets


class ScanPolicyEngine:
    """Control scan behavior based on policy"""
    
    POLICIES = {
        "strict": {
            "description": "Deep comprehensive scan - maximum coverage",
            "port_range": "1-65535",
            "scan_timeout": 600,
            "service_detection": True,
            "os_detection": True,
            "script_scanning": True,
            "use_case": "Security audits, penetration testing"
        },
        "standard": {
            "description": "Balanced scan - common ports and services",
            "port_range": "1-10000",
            "scan_timeout": 300,
            "service_detection": True,
            "os_detection": False,
            "script_scanning": False,
            "use_case": "Regular monitoring, vulnerability assessment"
        },
        "demo": {
            "description": "Quick scan - fast results for demonstration",
            "port_range": "80,443,22,3306",
            "scan_timeout": 60,
            "service_detection": True,
            "os_detection": False,
            "script_scanning": False,
            "use_case": "Quick assessments, demonstrations"
        },
        "internal": {
            "description": "Internal audit - full coverage for corporate networks",
            "port_range": "1-65535",
            "scan_timeout": 900,
            "service_detection": True,
            "os_detection": True,
            "script_scanning": True,
            "use_case": "Internal security audits, asset discovery"
        },
        "light": {
            "description": "Minimal impact - monitoring only",
            "port_range": "80,443",
            "scan_timeout": 30,
            "service_detection": False,
            "os_detection": False,
            "script_scanning": False,
            "use_case": "Continuous monitoring, uptime checks"
        }
    }
    
    def get_policy(self, policy_name: str) -> Dict:
        """Get policy configuration"""
        return self.POLICIES.get(policy_name, self.POLICIES["standard"])
    
    def validate_policy(self, policy_name: str) -> bool:
        """Check if policy exists"""
        return policy_name in self.POLICIES
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return list(self.POLICIES.keys())
    
    def describe_policies(self) -> Dict:
        """Get full policy descriptions"""
        return {
            name: {
                "description": policy["description"],
                "use_case": policy["use_case"],
                "timeout": policy["scan_timeout"]
            }
            for name, policy in self.POLICIES.items()
        }


# Example usage
if __name__ == "__main__":
    
    # Test confidence scoring
    print("="*70)
    print("CONFIDENCE SCORING TEST")
    print("="*70 + "\n")
    
    scorer = RuleConfidenceScorer()
    
    finding = {
        "title": "HTTP service detected",
        "severity": "INFO",
        "port": 80,
        "detection_method": "banner_grab",
        "version": "Apache 2.4.41"
    }
    
    scored = scorer.score_finding(finding)
    print(f"Finding: {scored['title']}")
    print(f"Confidence: {scored['confidence']:.0%} ({scored['confidence_level']})")
    print(f"Reasons:")
    for reason in scored['confidence_reasons']:
        print(f"  • {reason}")
    
    # Test professional wording
    print("\n" + "="*70)
    print("PROFESSIONAL WORDING TEST")
    print("="*70 + "\n")
    
    wording = ProfessionalWording()
    
    findings = [
        {"title": "No public services detected", "severity": "INFO"},
        {"title": "Missing X-Frame-Options header", "severity": "MEDIUM", "header": "X-Frame-Options"},
        {"title": "CDN detected", "severity": "INFO"}
    ]
    
    for finding in findings:
        prof = wording.professionalize(finding)
        print(f"Original: {finding['title']}")
        print(f"Professional: {prof['title']}")
        print(f"Description: {prof['description']}")
        print()
    
    # Test scan policies
    print("="*70)
    print("SCAN POLICY ENGINE TEST")
    print("="*70 + "\n")
    
    policy_engine = ScanPolicyEngine()
    
    for policy_name in policy_engine.list_policies():
        policy = policy_engine.get_policy(policy_name)
        print(f"{policy_name.upper()}:")
        print(f"  Description: {policy['description']}")
        print(f"  Timeout: {policy['scan_timeout']}s")
        print(f"  Service Detection: {policy['service_detection']}")
        print()
