"""
GeoIP and ASN Lookup
Get geographical location and network information
"""

from typing import Dict, Any, Optional
import socket
import subprocess
import json
import re

class GeoIPLookup:
    """Look up geographical information about IP addresses"""
    
    # Free GeoIP APIs (no API key required)
    GEOIP_APIS = [
        'https://ipapi.co/{ip}/json/',
        'https://ip-api.com/json/{ip}'
    ]
    
    def lookup(self, ip: str) -> Dict[str, Any]:
        """Look up IP geographical information"""
        try:
            import requests
            
            for api_url in self.GEOIP_APIS:
                try:
                    url = api_url.format(ip=ip)
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        return {
                            'ip': ip,
                            'country': data.get('country') or data.get('country_name'),
                            'region': data.get('region') or data.get('regionName'),
                            'city': data.get('city'),
                            'latitude': data.get('latitude') or data.get('lat'),
                            'longitude': data.get('longitude') or data.get('lon'),
                            'isp': data.get('isp') or data.get('org'),
                            'org': data.get('org') or data.get('as'),
                            'timezone': data.get('timezone')
                        }
                except:
                    continue
            
            return {'ip': ip, 'error': 'All GeoIP services failed'}
        
        except Exception as e:
            return {'ip': ip, 'error': str(e)}


class ASNLookup:
    """Look up Autonomous System Number information"""
    
    def lookup(self, ip: str) -> Dict[str, Any]:
        """Look up ASN for IP"""
        try:
            # Try whois command if available
            result = subprocess.run(
                ['whois', ip],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return self._parse_whois(result.stdout, ip)
            
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: try reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {
                'ip': ip,
                'hostname': hostname,
                'reverse_dns': hostname
            }
        except:
            return {'ip': ip, 'error': 'ASN lookup failed'}
    
    def _parse_whois(self, whois_output: str, ip: str) -> Dict[str, Any]:
        """Parse whois output"""
        data = {'ip': ip}
        
        # Extract ASN
        asn_match = re.search(r'AS(\d+)', whois_output)
        if asn_match:
            data['asn'] = f"AS{asn_match.group(1)}"
        
        # Extract organization
        org_match = re.search(r'Organization:\s+(.+)', whois_output, re.I)
        if org_match:
            data['organization'] = org_match.group(1).strip()
        
        # Extract country
        country_match = re.search(r'Country:\s+(.+)', whois_output, re.I)
        if country_match:
            data['country'] = country_match.group(1).strip()
        
        return data


class NetworkRecon:
    """Combined network reconnaissance"""
    
    def __init__(self):
        self.geoip = GeoIPLookup()
        self.asn = ASNLookup()
    
    def full_recon(self, ip: str) -> Dict[str, Any]:
        """Full network reconnaissance"""
        return {
            'ip': ip,
            'geo': self.geoip.lookup(ip),
            'asn': self.asn.lookup(ip)
        }
