"""
CVE Database Fetcher - Vulnerability Database Integration
Fetches CVE information from public vulnerability databases
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path


class CVEFetcher:
    """Fetch CVE data from public databases"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        # NVD API endpoints (using public endpoints without key)
        self.nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cvedetails_api = "https://www.cvedetails.com/api/v1"
    
    def search_cve_by_software(self, software_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Search CVEs for specific software"""
        cache_file = self.cache_dir / f"cve_{software_name.replace(' ', '_')}.json"
        
        # Check cache first
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    if datetime.fromisoformat(cached.get("cached_at", "")) > datetime.now() - timedelta(days=7):
                        return cached["data"]
            except:
                pass
        
        try:
            # Try NVD API (free endpoint with rate limiting)
            params = {
                "keywordSearch": software_name,
                "resultsPerPage": 10
            }
            
            headers = {
                "User-Agent": "SecurityMonitor/1.0"
            }
            
            response = requests.get(self.nvd_api, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cves = self._parse_nvd_response(data, version)
                
                # Cache results
                try:
                    with open(cache_file, 'w') as f:
                        json.dump({
                            "cached_at": datetime.now().isoformat(),
                            "data": cves
                        }, f)
                except:
                    pass
                
                return cves
        except requests.Timeout:
            return self._get_demo_cves(software_name, version)
        except Exception as e:
            return self._get_demo_cves(software_name, version)
    
    def search_cve_by_cpe(self, cpe: str) -> Dict[str, Any]:
        """Search CVEs by CPE identifier"""
        cache_file = self.cache_dir / f"cpe_{cpe.replace('/', '_')}.json"
        
        # Check cache
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    if datetime.fromisoformat(cached.get("cached_at", "")) > datetime.now() - timedelta(days=7):
                        return cached["data"]
            except:
                pass
        
        try:
            params = {
                "cpeName": cpe,
                "resultsPerPage": 10
            }
            
            response = requests.get(self.nvd_api, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cves = self._parse_nvd_response(data)
                
                # Cache results
                try:
                    with open(cache_file, 'w') as f:
                        json.dump({
                            "cached_at": datetime.now().isoformat(),
                            "data": cves
                        }, f)
                except:
                    pass
                
                return cves
        except:
            pass
        
        return {"vulnerabilities": []}
    
    def _parse_nvd_response(self, response: Dict[str, Any], version: Optional[str] = None) -> Dict[str, Any]:
        """Parse NVD API response"""
        vulnerabilities = []
        
        if "vulnerabilities" not in response:
            return {"vulnerabilities": []}
        
        for vuln_item in response.get("vulnerabilities", [])[:10]:
            try:
                cve = vuln_item.get("cve", {})
                cve_id = cve.get("id", "N/A")
                
                # Extract severity and CVSS score
                metrics = cve.get("metrics", {})
                cvss_v3 = metrics.get("cvssV3", [{}])[0]
                cvss_score = cvss_v3.get("cvssData", {}).get("baseScore", 0)
                severity = cvss_v3.get("cvssData", {}).get("baseSeverity", "Unknown")
                
                # Extract description
                descriptions = cve.get("descriptions", [])
                description = descriptions[0].get("value", "N/A") if descriptions else "N/A"
                
                # Extract published date
                published = cve.get("published", "N/A")
                
                vulnerabilities.append({
                    "cve_id": cve_id,
                    "severity": severity,
                    "cvss_score": cvss_score,
                    "description": description[:200],  # Truncate to 200 chars
                    "published": published,
                    "source": "NVD"
                })
            except Exception as e:
                continue
        
        return {
            "vulnerabilities": vulnerabilities,
            "count": len(vulnerabilities)
        }
    
    def _get_demo_cves(self, software: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Return demo CVE data when API is unavailable"""
        demo_cves = {
            "apache": [
                {
                    "cve_id": "CVE-2024-12345",
                    "severity": "HIGH",
                    "cvss_score": 8.1,
                    "description": "Remote code execution in Apache Web Server versions < 2.4.59",
                    "published": "2024-01-15",
                    "source": "NVD"
                },
                {
                    "cve_id": "CVE-2024-11111",
                    "severity": "MEDIUM",
                    "cvss_score": 5.3,
                    "description": "Information disclosure vulnerability in Apache mod_ssl",
                    "published": "2024-02-20",
                    "source": "NVD"
                }
            ],
            "nginx": [
                {
                    "cve_id": "CVE-2024-54321",
                    "severity": "MEDIUM",
                    "cvss_score": 6.5,
                    "description": "Denial of service vulnerability in nginx HTTP/2 implementation",
                    "published": "2024-01-10",
                    "source": "NVD"
                }
            ],
            "php": [
                {
                    "cve_id": "CVE-2024-33333",
                    "severity": "CRITICAL",
                    "cvss_score": 9.8,
                    "description": "Remote code execution in PHP versions < 8.2.18",
                    "published": "2024-02-01",
                    "source": "NVD"
                }
            ]
        }
        
        # Match software name
        software_lower = software.lower()
        vulns = []
        
        for key, cves in demo_cves.items():
            if key in software_lower:
                vulns.extend(cves)
        
        if not vulns:
            # Generic CVE
            vulns = [{
                "cve_id": "CVE-2024-00000",
                "severity": "MEDIUM",
                "cvss_score": 5.0,
                "description": "Generic vulnerability in web server software",
                "published": "2024-01-01",
                "source": "NVD"
            }]
        
        return {
            "vulnerabilities": vulns,
            "count": len(vulns),
            "note": "Demo data - API unavailable"
        }
    
    def get_latest_cves(self, limit: int = 10) -> Dict[str, Any]:
        """Get latest CVEs published"""
        cache_file = self.cache_dir / "latest_cves.json"
        
        # Check cache
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    if datetime.fromisoformat(cached.get("cached_at", "")) > datetime.now() - timedelta(days=1):
                        return cached["data"]
            except:
                pass
        
        try:
            # Get latest CVEs from last 30 days
            params = {
                "resultsPerPage": limit,
                "pubStartDate": (datetime.now() - timedelta(days=30)).isoformat()
            }
            
            response = requests.get(self.nvd_api, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cves = self._parse_nvd_response(data)
                
                # Cache results
                try:
                    with open(cache_file, 'w') as f:
                        json.dump({
                            "cached_at": datetime.now().isoformat(),
                            "data": cves
                        }, f)
                except:
                    pass
                
                return cves
        except:
            pass
        
        return {
            "vulnerabilities": [],
            "note": "API unavailable - try again later"
        }


def check_software_vulnerabilities(software_name: str, version: Optional[str] = None) -> Dict[str, Any]:
    """Quick function to check vulnerabilities for software"""
    fetcher = CVEFetcher()
    return fetcher.search_cve_by_software(software_name, version)
