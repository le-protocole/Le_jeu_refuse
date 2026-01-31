"""
HTTP Security Headers Analyzer
Check for missing or weak security headers
"""

import requests
from typing import Dict, List, Any

class HeadersAnalyzer:
    """Analyze HTTP security headers"""
    
    # Important security headers
    IMPORTANT_HEADERS = {
        'Strict-Transport-Security': {
            'severity': 'HIGH',
            'description': 'Forces HTTPS connections',
            'recommendation': 'Add: Strict-Transport-Security: max-age=31536000; includeSubDomains'
        },
        'X-Content-Type-Options': {
            'severity': 'HIGH',
            'description': 'Prevents MIME-type sniffing',
            'recommendation': 'Add: X-Content-Type-Options: nosniff'
        },
        'X-Frame-Options': {
            'severity': 'MEDIUM',
            'description': 'Prevents clickjacking attacks',
            'recommendation': 'Add: X-Frame-Options: DENY'
        },
        'Content-Security-Policy': {
            'severity': 'HIGH',
            'description': 'Controls resource loading',
            'recommendation': 'Add: Content-Security-Policy: default-src \'self\''
        },
        'X-XSS-Protection': {
            'severity': 'MEDIUM',
            'description': 'Protects against XSS attacks',
            'recommendation': 'Add: X-XSS-Protection: 1; mode=block'
        },
        'Referrer-Policy': {
            'severity': 'LOW',
            'description': 'Controls referrer information',
            'recommendation': 'Add: Referrer-Policy: strict-origin-when-cross-origin'
        }
    }
    
    def __init__(self, timeout=5):
        self.timeout = timeout
    
    def check_headers(self, domain: str) -> Dict[str, Any]:
        """Check HTTP security headers"""
        try:
            # Add https:// if not present
            url = domain if domain.startswith('http') else f'https://{domain}'
            
            response = requests.head(url, timeout=self.timeout, allow_redirects=True, verify=False)
            headers = response.headers
            
            findings = {
                'domain': domain,
                'status_code': response.status_code,
                'headers_found': {},
                'headers_missing': [],
                'weak_values': []
            }
            
            # Check for present headers
            for header_name, header_info in self.IMPORTANT_HEADERS.items():
                if header_name in headers:
                    findings['headers_found'][header_name] = headers[header_name]
                else:
                    findings['headers_missing'].append({
                        'header': header_name,
                        'severity': header_info['severity'],
                        'description': header_info['description'],
                        'recommendation': header_info['recommendation']
                    })
            
            # Check for weak values
            weak = self._check_weak_values(headers)
            if weak:
                findings['weak_values'] = weak
            
            # Overall score
            findings['security_score'] = self._calculate_score(findings)
            
            return findings
            
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def _check_weak_values(self, headers: Dict) -> List[Dict]:
        """Check for weak header values"""
        weak = []
        
        # Check HSTS
        if 'Strict-Transport-Security' in headers:
            hsts = headers['Strict-Transport-Security']
            if 'max-age=0' in hsts or 'max-age=' not in hsts:
                weak.append({
                    'header': 'Strict-Transport-Security',
                    'issue': 'Weak configuration',
                    'value': hsts,
                    'recommendation': 'Set max-age to at least 31536000 (1 year)'
                })
        
        # Check CSP
        if 'Content-Security-Policy' in headers:
            csp = headers['Content-Security-Policy']
            if 'unsafe-inline' in csp or 'unsafe-eval' in csp:
                weak.append({
                    'header': 'Content-Security-Policy',
                    'issue': 'Contains unsafe directives',
                    'value': csp,
                    'recommendation': 'Remove unsafe-inline and unsafe-eval'
                })
        
        return weak
    
    def _calculate_score(self, findings: Dict) -> int:
        """Calculate security score (0-100)"""
        total = len(self.IMPORTANT_HEADERS)
        found = len(findings['headers_found'])
        weak = len(findings['weak_values'])
        
        # Base score from found headers
        score = (found / total) * 100
        
        # Deduct for weak values
        score -= weak * 10
        
        return max(0, min(100, int(score)))
