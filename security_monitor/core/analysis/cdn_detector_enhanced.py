"""
Enhanced CDN/Shared Hosting Detection
With HTTP headers, ASN lookup, and confidence scoring
"""

import socket
import requests
from typing import Dict, List, Tuple

class CDNDetector:
    """Detect CDN and shared hosting with high confidence"""
    
    # CDN ASN mappings
    CDN_ASNS = {
        "AS16509": "Amazon CloudFront",
        "AS15169": "Google/YouTube",
        "AS13335": "Cloudflare",
        "AS8075": "Microsoft Azure",
        "AS54113": "Fastly",
        "AS16012": "Akamai",
        "AS2818": "Bourbon Street Communications (shared hosting)",
        "AS29838": "GoDaddy",
        "AS14061": "DigitalOcean",
    }
    
    # CDN header signatures
    CDN_HEADERS = {
        "cf-ray": ("Cloudflare", 0.95),
        "cf-cache-status": ("Cloudflare", 0.95),
        "cf-request-id": ("Cloudflare", 0.95),
        "via": ("CDN/Proxy", 0.7),
        "x-amz-cf-id": ("Amazon CloudFront", 0.95),
        "x-cache": ("CDN", 0.8),
        "x-powered-by": ("Shared Hosting", 0.6),
        "server": ("Service Identifier", 0.7),
        "x-fastly-request-id": ("Fastly", 0.95),
        "x-akamai-transformed": ("Akamai", 0.95),
    }
    
    def __init__(self):
        self.findings = []
        self.confidence = 0.0
    
    def detect(self, target: str, ip: str) -> Dict:
        """
        Comprehensive CDN detection with confidence scoring
        
        Returns:
        {
            "is_cdn": True/False,
            "cdn_type": str,
            "confidence": 0.0-1.0,
            "indicators": [list of detected indicators],
            "reason": "explanation",
            "risk_impact": "scanning skipped (good practice)"
        }
        """
        
        result = {
            "is_cdn": False,
            "cdn_type": None,
            "confidence": 0.0,
            "indicators": [],
            "details": [],
            "reason": None,
            "risk_impact": None
        }
        
        # 1. Check HTTP Headers
        header_findings = self._check_headers(target)
        result["indicators"].extend(header_findings["indicators"])
        result["details"].extend(header_findings["details"])
        result["confidence"] += header_findings["confidence"] * 0.5
        
        # 2. Check ASN
        asn_findings = self._check_asn(ip)
        result["indicators"].extend(asn_findings["indicators"])
        result["details"].extend(asn_findings["details"])
        result["confidence"] += asn_findings["confidence"] * 0.5
        
        # Determine final result
        if result["confidence"] > 0.6:
            result["is_cdn"] = True
            result["cdn_type"] = self._determine_cdn_type(result["indicators"])
            result["reason"] = f"CDN/Shared hosting detected with {result['confidence']:.0%} confidence"
            result["risk_impact"] = "Scan skipped (protected by CDN - good practice)"
        else:
            result["reason"] = "Direct hosting detected - standard web services"
            result["risk_impact"] = "Full port scanning recommended"
        
        return result
    
    def _check_headers(self, target: str) -> Dict:
        """Check HTTP headers for CDN signatures"""
        
        findings = {
            "indicators": [],
            "details": [],
            "confidence": 0.0,
            "cdn_detected": None
        }
        
        try:
            # Try HTTP HEAD request
            response = requests.head(
                f"http://{target}",
                timeout=5,
                allow_redirects=True,
                verify=False
            )
            
            headers = response.headers
            max_confidence = 0.0
            
            # Check each header
            for header_name, (cdn_name, confidence) in self.CDN_HEADERS.items():
                if header_name.lower() in [k.lower() for k in headers.keys()]:
                    header_value = headers.get(header_name, "")
                    findings["indicators"].append(f"{header_name}: {header_value}")
                    findings["details"].append(f"  ✓ {cdn_name} header detected: {header_name}")
                    max_confidence = max(max_confidence, confidence)
            
            # Check Server header for hints
            server = headers.get("server", "").lower()
            if server:
                findings["indicators"].append(f"Server: {server}")
                
                # Service analysis
                if "cloudflare" in server:
                    findings["details"].append("  ✓ Cloudflare server detected")
                    max_confidence = 0.95
                elif "amazon" in server or "cloudfront" in server:
                    findings["details"].append("  ✓ Amazon CloudFront detected")
                    max_confidence = 0.95
                elif "akamai" in server:
                    findings["details"].append("  ✓ Akamai CDN detected")
                    max_confidence = 0.95
            
            findings["confidence"] = max_confidence
            
        except requests.exceptions.RequestException as e:
            findings["details"].append(f"  ! HTTP request failed: {str(e)}")
            findings["confidence"] = 0.3  # Low confidence if unreachable
        
        return findings
    
    def _check_asn(self, ip: str) -> Dict:
        """Check AS Number for CDN operators"""
        
        findings = {
            "indicators": [],
            "details": [],
            "confidence": 0.0
        }
        
        try:
            # Try to get hostname from IP (reverse DNS)
            hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
            findings["indicators"].append(f"Reverse DNS: {hostname}")
            findings["details"].append(f"  ✓ Reverse DNS: {hostname}")
            
            # Check for CDN patterns in hostname
            if any(cdn in hostname.lower() for cdn in ["cloudflare", "amazon", "google", "akamai", "fastly"]):
                findings["confidence"] = 0.85
                findings["details"].append(f"  ✓ CDN pattern in hostname")
        
        except (socket.herror, OSError):
            findings["details"].append("  ! Reverse DNS lookup failed (may be CDN)")
            findings["confidence"] = 0.2
        
        return findings
    
    def _determine_cdn_type(self, indicators: List[str]) -> str:
        """Determine which CDN provider based on indicators"""
        
        indicators_str = " ".join(indicators).lower()
        
        if "cloudflare" in indicators_str:
            return "Cloudflare"
        elif "amazon" in indicators_str or "cloudfront" in indicators_str:
            return "Amazon CloudFront"
        elif "google" in indicators_str:
            return "Google Cloud CDN"
        elif "akamai" in indicators_str:
            return "Akamai"
        elif "fastly" in indicators_str:
            return "Fastly"
        elif "azure" in indicators_str:
            return "Microsoft Azure"
        else:
            return "Unknown CDN/Shared Hosting"


class RiskScoreExplainer:
    """Explain risk scores with clear reasoning"""
    
    def __init__(self):
        self.explanations = []
    
    def explain_risk(self, score: int, open_ports: int, vulnerabilities: int, 
                    is_cdn: bool, has_ssl: bool, headers_score: int) -> Dict:
        """
        Generate detailed risk explanation
        
        Returns:
        {
            "score": 7,
            "level": "LOW",
            "factors": [...],
            "summary": "...",
            "recommendation": "..."
        }
        """
        
        explanation = {
            "score": score,
            "level": self._get_risk_level(score),
            "factors": [],
            "summary": None,
            "recommendation": None
        }
        
        # Build factor list
        if open_ports == 2 and all(p in [80, 443] for p in [80, 443]):
            explanation["factors"].append("✓ Only standard web ports (80/443) open")
        elif open_ports > 10:
            explanation["factors"].append(f"! {open_ports} ports open (high exposure)")
        else:
            explanation["factors"].append(f"• {open_ports} ports open (moderate)")
        
        if is_cdn:
            explanation["factors"].append("✓ Protected by CDN (reduced attack surface)")
        else:
            explanation["factors"].append("! Direct hosting (unprotected)")
        
        if vulnerabilities == 0:
            explanation["factors"].append("✓ No known vulnerabilities detected")
        else:
            explanation["factors"].append(f"! {vulnerabilities} vulnerabilities found")
        
        if has_ssl:
            explanation["factors"].append("✓ SSL/TLS enabled")
        else:
            explanation["factors"].append("! No SSL/TLS detected")
        
        if headers_score > 70:
            explanation["factors"].append("✓ Good security headers implemented")
        elif headers_score > 40:
            explanation["factors"].append("• Partial security headers")
        else:
            explanation["factors"].append("! Weak or missing security headers")
        
        # Generate summary
        if score < 20:
            explanation["summary"] = "Minimal risk exposure detected"
            explanation["recommendation"] = "Maintain current security posture"
        elif score < 40:
            explanation["summary"] = "Low risk with minor recommendations"
            explanation["recommendation"] = "Implement suggested header improvements"
        elif score < 60:
            explanation["summary"] = "Moderate risk requiring attention"
            explanation["recommendation"] = "Address identified vulnerabilities"
        else:
            explanation["summary"] = "High risk requiring immediate action"
            explanation["recommendation"] = "Implement remediation plan"
        
        return explanation
    
    def _get_risk_level(self, score: int) -> str:
        """Map score to risk level"""
        if score < 20:
            return "INFO"
        elif score < 40:
            return "LOW"
        elif score < 60:
            return "MEDIUM"
        elif score < 80:
            return "HIGH"
        else:
            return "CRITICAL"


# Example usage
if __name__ == "__main__":
    detector = CDNDetector()
    explainer = RiskScoreExplainer()
    
    # Test CDN detection
    print("="*70)
    print("CDN DETECTION TEST")
    print("="*70 + "\n")
    
    result = detector.detect("google.com", "142.250.197.142")
    print(f"Target: google.com")
    print(f"CDN Detected: {result['is_cdn']}")
    print(f"Type: {result['cdn_type']}")
    print(f"Confidence: {result['confidence']:.0%}\n")
    print("Indicators:")
    for indicator in result["indicators"]:
        print(f"  • {indicator}")
    print("\nDetails:")
    for detail in result["details"]:
        print(detail)
    print(f"\nRisk Impact: {result['risk_impact']}\n")
    
    # Test risk explanation
    print("="*70)
    print("RISK SCORE EXPLANATION TEST")
    print("="*70 + "\n")
    
    explanation = explainer.explain_risk(
        score=7,
        open_ports=2,
        vulnerabilities=0,
        is_cdn=True,
        has_ssl=True,
        headers_score=75
    )
    
    print(f"Risk Score: {explanation['score']}/100 ({explanation['level']})")
    print(f"\nReason:")
    for factor in explanation["factors"]:
        print(f"  {factor}")
    print(f"\nSummary: {explanation['summary']}")
    print(f"Recommendation: {explanation['recommendation']}")
