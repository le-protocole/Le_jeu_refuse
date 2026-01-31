"""
Technology Stack Detection
Identify CMS, frameworks, libraries, server software
"""

import requests
from typing import Dict, List, Any
import re

class TechStackDetector:
    """Detect technology stack used by website"""
    
    # Known tech signatures in headers and HTML
    TECH_SIGNATURES = {
        'CMS': {
            'WordPress': {
                'headers': ['x-pingback', 'wp-version'],
                'patterns': [r'/wp-content/', r'/wp-admin/', r'wp-json', r'wordpress'],
                'meta': ['generator.*wordpress']
            },
            'Drupal': {
                'patterns': [r'/sites/', r'drupal', r'/modules/'],
                'meta': ['generator.*drupal']
            },
            'Joomla': {
                'patterns': [r'/components/', r'joomla'],
                'meta': ['generator.*joomla']
            }
        },
        'Framework': {
            'Laravel': {
                'headers': ['x-powered-by.*laravel'],
                'patterns': [r'/storage/', r'app/Http']
            },
            'Django': {
                'headers': ['server.*django'],
                'patterns': [r'/admin/', r'django']
            },
            'Flask': {
                'headers': ['server.*flask'],
                'patterns': [r'werkzeug']
            }
        },
        'Server': {
            'Apache': {
                'headers': ['server.*apache']
            },
            'Nginx': {
                'headers': ['server.*nginx']
            },
            'IIS': {
                'headers': ['server.*iis', 'x-aspnet']
            }
        }
    }
    
    def __init__(self, timeout=5):
        self.timeout = timeout
    
    def detect_stack(self, domain: str) -> Dict[str, Any]:
        """Detect technology stack"""
        try:
            url = domain if domain.startswith('http') else f'https://{domain}'
            
            response = requests.get(url, timeout=self.timeout, verify=False)
            html = response.text
            headers = response.headers
            
            detected = {
                'domain': domain,
                'server': None,
                'cms': None,
                'frameworks': [],
                'languages': [],
                'technologies': []
            }
            
            # Check headers
            detected['server'] = self._detect_from_headers(headers)
            
            # Check HTML content
            detected['cms'] = self._detect_cms(html, headers)
            detected['frameworks'] = self._detect_frameworks(html, headers)
            detected['technologies'] = self._detect_technologies(html, headers)
            
            # Check meta tags
            detected['meta_info'] = self._extract_meta_info(html)
            
            return detected
            
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def _detect_from_headers(self, headers: Dict) -> str:
        """Detect server from headers"""
        server_header = headers.get('Server', '').lower()
        return server_header if server_header else 'Unknown'
    
    def _detect_cms(self, html: str, headers: Dict) -> str:
        """Detect CMS"""
        for cms, signatures in self.TECH_SIGNATURES['CMS'].items():
            # Check headers
            for header_sig in signatures.get('headers', []):
                for header, value in headers.items():
                    if re.search(header_sig, f'{header}:{value}', re.I):
                        return cms
            
            # Check patterns
            for pattern in signatures.get('patterns', []):
                if re.search(pattern, html, re.I):
                    return cms
        
        return None
    
    def _detect_frameworks(self, html: str, headers: Dict) -> List[str]:
        """Detect frameworks"""
        frameworks = []
        
        for fw, signatures in self.TECH_SIGNATURES['Framework'].items():
            for pattern in signatures.get('patterns', []):
                if re.search(pattern, html, re.I):
                    frameworks.append(fw)
                    break
        
        return frameworks
    
    def _detect_technologies(self, html: str, headers: Dict) -> List[str]:
        """Detect other technologies"""
        techs = []
        
        # Detect common technologies by patterns
        patterns = {
            'jQuery': r'jquery',
            'Bootstrap': r'bootstrap',
            'React': r'react',
            'Vue': r'vue',
            'Angular': r'angular'
        }
        
        for tech, pattern in patterns.items():
            if re.search(pattern, html, re.I):
                techs.append(tech)
        
        return techs
    
    def _extract_meta_info(self, html: str) -> Dict[str, str]:
        """Extract meta information"""
        meta = {}
        
        # Generator meta tag
        gen_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\']([^"\']+)["\']', html, re.I)
        if gen_match:
            meta['generator'] = gen_match.group(1)
        
        # Title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
        if title_match:
            meta['title'] = title_match.group(1)
        
        return meta
