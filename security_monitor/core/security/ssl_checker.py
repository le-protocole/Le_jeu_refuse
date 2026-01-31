"""
SSL/TLS Certificate Analysis
Extract and analyze SSL certificates from target domain
"""

import socket
import ssl
from datetime import datetime
from typing import Dict, Any, Optional

class SSLChecker:
    """Analyze SSL/TLS certificates"""
    
    def __init__(self, timeout=5):
        self.timeout = timeout
    
    def get_certificate(self, domain: str, port: int = 443) -> Optional[Dict[str, Any]]:
        """Get SSL certificate information"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((domain, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cert_bin = ssock.getpeercert(binary_form=True)
                    
                    if not cert:
                        return None
                    
                    return {
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'san': cert.get('subjectAltName', []),
                        'status': self._check_certificate_status(cert)
                    }
        except (socket.timeout, ssl.SSLError, OSError) as e:
            return {'error': str(e)}
    
    def _check_certificate_status(self, cert: Dict) -> Dict[str, Any]:
        """Check certificate validity and expiration"""
        try:
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            now = datetime.utcnow()
            
            days_left = (not_after - now).days
            
            return {
                'valid': days_left > 0,
                'expires_in_days': days_left,
                'expiration_date': not_after.isoformat(),
                'warning': 'Expiring soon' if 0 < days_left < 30 else ('Expired' if days_left <= 0 else '')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_certificate(self, domain: str) -> Dict[str, Any]:
        """Complete certificate analysis"""
        cert = self.get_certificate(domain)
        
        if not cert or 'error' in cert:
            return {
                'domain': domain,
                'ssl_enabled': False,
                'error': cert.get('error') if cert else 'Failed to connect'
            }
        
        return {
            'domain': domain,
            'ssl_enabled': True,
            'subject': cert.get('subject'),
            'issuer': cert.get('issuer'),
            'not_before': cert.get('not_before'),
            'not_after': cert.get('not_after'),
            'san': cert.get('san'),
            'status': cert.get('status'),
            'vulnerabilities': self._check_vulnerabilities(cert)
        }
    
    def _check_vulnerabilities(self, cert: Dict) -> list:
        """Check for known SSL vulnerabilities"""
        vulns = []
        
        status = cert.get('status', {})
        
        # Check expiration
        if status.get('expires_in_days') is not None:
            if status['expires_in_days'] <= 0:
                vulns.append({
                    'type': 'CRITICAL',
                    'issue': 'Certificate expired',
                    'description': f"Certificate expired {abs(status['expires_in_days'])} days ago"
                })
            elif status['expires_in_days'] < 30:
                vulns.append({
                    'type': 'WARNING',
                    'issue': 'Certificate expiring soon',
                    'description': f"Certificate expires in {status['expires_in_days']} days"
                })
        
        # Check for self-signed
        issuer = cert.get('issuer', {})
        subject = cert.get('subject', {})
        
        if issuer.get('commonName') == subject.get('commonName'):
            vulns.append({
                'type': 'WARNING',
                'issue': 'Self-signed certificate',
                'description': 'Certificate is self-signed, not signed by trusted CA'
            })
        
        return vulns
