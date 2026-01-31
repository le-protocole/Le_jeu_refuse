"""
DNS Resolution and IP Discovery Module
Purpose: Convert URL → IP, detect reverse proxies, identify CDNs
"""

import socket
import ipaddress
from typing import List, Dict, Optional
from urllib.parse import urlparse
import dns.resolver
import dns.rdatatype
import requests
from datetime import datetime

class DNSResolver:
    """
    Resolves domain names to IP addresses
    Detects CDN / reverse proxy usage
    """
    
    def __init__(self):
        # Force DNS resolver with Google and Cloudflare nameservers
        self.resolver = dns.resolver.Resolver(configure=False)
        self.resolver.nameservers = ["8.8.8.8", "1.1.1.1"]  # Google + Cloudflare DNS
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
    
    def _sanitize_url(self, url: str) -> str:
        """
        Sanitize URL by removing protocol, www, trailing slashes
        
        Examples:
        https://geekprank.com/ → geekprank.com
        www.example.com → example.com
        http://test.org:8080 → test.org
        """
        url = url.strip()
        
        # Remove protocol (http://, https://, ftp://, etc.)
        if "://" in url:
            url = url.split("://", 1)[1]
        
        # Remove www. prefix
        if url.startswith("www."):
            url = url[4:]
        
        # Remove port if present
        if ":" in url:
            url = url.split(":")[0]
        
        # Remove trailing slashes and paths
        url = url.split("/")[0]
        
        return url.lower().strip()
    
    def resolve_domain(self, domain: str) -> Dict:
        """
        Resolve domain to IPs and check for proxy/CDN
        
        Returns:
        {
            "target": "example.com",
            "ips": ["1.2.3.4"],
            "cdn": bool,
            "cdn_provider": Optional[str],
            "a_records": [...],
            "cname_records": [...],
            "timestamp": "2026-01-31T..."
        }
        """
        
        # Sanitize input URL first
        domain = self._sanitize_url(domain)
        
        result = {
            "target": domain,
            "ips": [],
            "cdn": False,
            "cdn_provider": None,
            "a_records": [],
            "cname_records": [],
            "mx_records": [],
            "ns_records": [],
            "timestamp": datetime.now().isoformat(),
            "errors": []
        }
        
        try:
            # Check if it's already an IP
            try:
                ipaddress.ip_address(domain)
                result["ips"] = [domain]
                return result
            except ValueError:
                pass
            
            # Resolve A records
            try:
                a_answers = self.resolver.resolve(domain, dns.rdatatype.A)
                for rdata in a_answers:
                    ip = str(rdata)
                    result["ips"].append(ip)
                    result["a_records"].append(ip)
            except Exception as e:
                result["errors"].append(f"A record lookup failed: {str(e)}")
            
            # Resolve AAAA records (IPv6)
            try:
                aaaa_answers = self.resolver.resolve(domain, dns.rdatatype.AAAA)
                for rdata in aaaa_answers:
                    ip = str(rdata)
                    result["ips"].append(ip)
            except:
                pass
            
            # Resolve CNAME records
            try:
                cname_answers = self.resolver.resolve(domain, dns.rdatatype.CNAME)
                for rdata in cname_answers:
                    cname = str(rdata).rstrip('.')
                    result["cname_records"].append(cname)
                    # Check if CNAME points to CDN
                    if self._is_cdn_cname(cname):
                        result["cdn"] = True
                        result["cdn_provider"] = self._detect_cdn_from_cname(cname)
            except:
                pass
            
            # Resolve MX records
            try:
                mx_answers = self.resolver.resolve(domain, dns.rdatatype.MX)
                for rdata in mx_answers:
                    result["mx_records"].append(str(rdata))
            except:
                pass
            
            # Resolve NS records
            try:
                ns_answers = self.resolver.resolve(domain, dns.rdatatype.NS)
                for rdata in ns_answers:
                    result["ns_records"].append(str(rdata).rstrip('.'))
            except:
                pass
            
            # Check HTTP headers for CDN indicators
            if not result["cdn"]:
                result["cdn"] = self._check_http_headers(domain)
                if result["cdn"]:
                    result["cdn_provider"] = "Unknown (HTTP header detected)"
            
            # Validation: Domain is valid if it has IPs OR CNAME records
            if not result["ips"] and not result["cname_records"]:
                result["errors"].append(f"Could not resolve {domain}")
        
        except Exception as e:
            result["errors"].append(f"Resolution failed: {str(e)}")
        
        return result
    
    def _is_cdn_cname(self, cname: str) -> bool:
        """Check if CNAME points to known CDN"""
        cdn_keywords = [
            "cloudflare",
            "akamai",
            "cdn",
            "edgecast",
            "aws",
            "azure",
            "fastly",
            "google"
        ]
        cname_lower = cname.lower()
        return any(keyword in cname_lower for keyword in cdn_keywords)
    
    def _detect_cdn_from_cname(self, cname: str) -> str:
        """Detect CDN provider from CNAME"""
        cname_lower = cname.lower()
        if "cloudflare" in cname_lower:
            return "Cloudflare"
        elif "akamai" in cname_lower:
            return "Akamai"
        elif "aws" in cname_lower or "cloudfront" in cname_lower:
            return "AWS CloudFront"
        elif "azure" in cname_lower:
            return "Azure CDN"
        elif "fastly" in cname_lower:
            return "Fastly"
        elif "google" in cname_lower:
            return "Google Cloud"
        return "Unknown"
    
    def _check_http_headers(self, domain: str) -> bool:
        """Check HTTP headers for CDN indicators"""
        try:
            headers = requests.head(
                f"http://{domain}",
                timeout=5,
                allow_redirects=True
            ).headers
            
            cdn_headers = ["cf-ray", "server", "x-cache"]
            for header in cdn_headers:
                if header in headers:
                    value = headers[header].lower()
                    if any(cdn in value for cdn in ["cloudflare", "akamai", "cdn"]):
                        return True
            return False
        except:
            return False
    
    def validate_ip(self, ip: str) -> bool:
        """Validate if string is valid IP"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def is_private_ip(self, ip: str) -> bool:
        """Check if IP is private (RFC 1918)"""
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False


# Example usage
if __name__ == "__main__":
    resolver = DNSResolver()
    
    # Test domains
    targets = [
        "example.com",
        "google.com",
        "cloudflare.com"
    ]
    
    for target in targets:
        result = resolver.resolve_domain(target)
        print(f"\n{target}:")
        print(f"  IPs: {result['ips']}")
        print(f"  CDN: {result['cdn']} ({result['cdn_provider']})")
        print(f"  CNAME: {result['cname_records']}")
