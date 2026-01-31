"""
Cloud Provider Detection
Identify AWS, Azure, GCP, Cloudflare, Akamai usage
"""

from typing import Dict, Any, Tuple
import socket

class CloudDetector:
    """Detect cloud providers and CDN usage"""
    
    # Known cloud provider IP ranges and patterns
    CLOUD_PATTERNS = {
        'AWS': {
            'names': ['ec2', 'amazon', 'aws', 'amazonaws'],
            'cnames': ['cloudfront', 'amazonaws.com', 'aws.amazon.com'],
            'asn': ['16509', '14061']
        },
        'Azure': {
            'names': ['azure', 'microsoft', 'azurewebsites', 'cloudapp'],
            'cnames': ['azurewebsites', 'cloudapp.azure.com', 'azure.microsoft.com'],
            'asn': ['8075', '14707']
        },
        'GCP': {
            'names': ['google', 'gcp', 'appspot', 'googleapis'],
            'cnames': ['c.storage.googleapis.com', 'goog', 'appengine'],
            'asn': ['15169']
        },
        'Cloudflare': {
            'names': ['cloudflare', 'cflare'],
            'cnames': ['cloudflare', 'cf-ns'],
            'asn': ['13335']
        },
        'Akamai': {
            'names': ['akamai', 'akamaitechnologies'],
            'cnames': ['akamaized.net', 'akamaitech'],
            'asn': ['16625']
        }
    }
    
    def detect_cloud(self, domain: str, dns_result: Dict = None) -> Dict[str, Any]:
        """Detect cloud providers used by domain"""
        findings = {
            'domain': domain,
            'providers': [],
            'details': {}
        }
        
        if dns_result:
            # Check CNAME records
            cnames = dns_result.get('cname_records', [])
            for cname in cnames:
                provider = self._identify_by_cname(cname)
                if provider:
                    findings['providers'].append(provider)
                    findings['details'][provider] = {'evidence': f'CNAME: {cname}'}
        
        # Try reverse DNS
        try:
            ip = socket.gethostbyname(domain)
            provider = self._identify_by_ip(ip)
            if provider and provider not in findings['providers']:
                findings['providers'].append(provider)
                findings['details'][provider] = {'evidence': f'IP: {ip}'}
        except:
            pass
        
        return findings
    
    def _identify_by_cname(self, cname: str) -> str:
        """Identify provider by CNAME"""
        cname_lower = cname.lower()
        
        for provider, patterns in self.CLOUD_PATTERNS.items():
            for pattern in patterns['cnames']:
                if pattern in cname_lower:
                    return provider
        
        for provider, patterns in self.CLOUD_PATTERNS.items():
            for pattern in patterns['names']:
                if pattern in cname_lower:
                    return provider
        
        return None
    
    def _identify_by_ip(self, ip: str) -> str:
        """Identify provider by IP (reverse DNS)"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return self._identify_by_cname(hostname)
        except:
            return None
    
    def get_risk_assessment(self, providers: list) -> Dict[str, Any]:
        """Get risk assessment for detected providers"""
        assessment = {
            'count': len(providers),
            'vendors': providers,
            'distribution': 'Good - using CDN/Cloud' if len(providers) > 0 else 'Self-hosted - No CDN',
            'risks': []
        }
        
        # Multiple providers might indicate complexity
        if len(providers) > 2:
            assessment['risks'].append({
                'severity': 'MEDIUM',
                'issue': 'Multiple cloud providers detected',
                'description': 'Managing multiple vendors increases complexity',
                'recommendation': 'Standardize on fewer providers'
            })
        
        return assessment
