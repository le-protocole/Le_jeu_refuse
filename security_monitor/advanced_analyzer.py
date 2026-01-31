#!/usr/bin/env python3
"""
ADVANCED WEBSITE ANALYZER - PROFESSIONAL EDITION
Complete security assessment with 15+ analysis modules
Real-time deep reconnaissance + SSL + Headers + Cloud + Tech Stack + GeoIP
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import all core modules
try:
    from core.resolver.dns import DNSResolver
    from core.scanner.nmap import NmapScanner
    from core.analysis.rules import VulnerabilityRules
    from core.security.ssl_checker import SSLChecker
    from core.security.headers_analyzer import HeadersAnalyzer
    from core.cloud.cloud_detector import CloudDetector
    from core.cloud.tech_stack import TechStackDetector
    from core.network.geolocation import GeoIPLookup, ASNLookup, NetworkRecon
except ImportError as e:
    print(f"[ERROR] Missing module: {e}")
    sys.exit(1)

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 90)
    print(f"  {title}")
    print("=" * 90)

def sanitize_url(url: str) -> str:
    """Extract domain from URL"""
    import re
    url = url.strip()
    
    # Remove protocol
    url = re.sub(r'https?://', '', url, flags=re.I)
    url = re.sub(r'www\.', '', url)
    
    # Extract domain
    domain = url.split('/')[0].split(':')[0]
    return domain

def analyze_advanced(target: str) -> Optional[Dict[str, Any]]:
    """Complete advanced analysis with all modules"""
    
    domain = sanitize_url(target)
    print(f"\n[*] Target domain: {domain}")
    
    results = {
        'scan_timestamp': datetime.now().isoformat(),
        'domain': domain,
        'data_source': 'ADVANCED SCAN (REAL-TIME, NOT CACHED)',
        'modules': {}
    }
    
    # MODULE 1: DNS Resolution
    print("\n[1/10] DNS RESOLUTION")
    print("-" * 90)
    try:
        resolver = DNSResolver()
        dns_result = resolver.resolve_domain(domain)
        
        if not dns_result['ips'] and not dns_result['cname_records']:
            print(f"✗ Could not resolve {domain}")
            return None
        
        print(f"✓ IPs: {', '.join(dns_result['ips'][:3])}")
        print(f"✓ CDN: {'Yes (' + dns_result['cdn_provider'] + ')' if dns_result['cdn'] else 'No'}")
        
        results['modules']['dns'] = dns_result
        public_ip = dns_result['ips'][0] if dns_result['ips'] else None
    except Exception as e:
        print(f"✗ DNS failed: {e}")
        public_ip = None
    
    # MODULE 2: SSL/TLS Certificate Analysis
    print("\n[2/10] SSL/TLS CERTIFICATE ANALYSIS")
    print("-" * 90)
    try:
        ssl_checker = SSLChecker()
        ssl_result = ssl_checker.analyze_certificate(domain)
        
        if ssl_result.get('ssl_enabled'):
            print(f"✓ SSL Enabled")
            expiry = ssl_result.get('status', {}).get('expiration_date', 'N/A')
            print(f"✓ Expires: {expiry}")
            
            if ssl_result.get('vulnerabilities'):
                print(f"[!] Found {len(ssl_result['vulnerabilities'])} SSL issues")
        else:
            print(f"✗ SSL Not Enabled or failed to connect")
        
        results['modules']['ssl'] = ssl_result
    except Exception as e:
        print(f"[!] SSL check failed: {e}")
    
    # MODULE 3: HTTP Security Headers
    print("\n[3/10] HTTP SECURITY HEADERS")
    print("-" * 90)
    try:
        headers_analyzer = HeadersAnalyzer()
        headers_result = headers_analyzer.check_headers(domain)
        
        if 'error' not in headers_result:
            score = headers_result.get('security_score', 0)
            print(f"✓ Security Score: {score}/100")
            print(f"✓ Headers Found: {len(headers_result.get('headers_found', {}))}")
            print(f"[!] Headers Missing: {len(headers_result.get('headers_missing', []))}")
            
            if score < 70:
                print(f"   Recommendation: Improve header configuration")
        else:
            print(f"[!] Header check failed: {headers_result.get('error')}")
        
        results['modules']['headers'] = headers_result
    except Exception as e:
        print(f"[!] Header analysis failed: {e}")
    
    # MODULE 4: Port Scanning
    print("\n[4/10] PORT SCANNING (Real-time)")
    print("-" * 90)
    try:
        if public_ip:
            scanner = NmapScanner()
            scan_result = scanner.quick_scan(public_ip)
            
            if scan_result and 'ports' in scan_result:
                open_ports = scan_result.get('ports', [])
                print(f"✓ Open Ports: {len(open_ports)}")
                
                for port_info in open_ports[:5]:
                    service = port_info.get('service', 'unknown')
                    print(f"   → Port {port_info['port']}: {service}")
                
                if len(open_ports) > 5:
                    print(f"   ... and {len(open_ports) - 5} more")
            else:
                print(f"✗ Scan failed or no open ports")
                scan_result = {}
            
            results['modules']['ports'] = scan_result
        else:
            print(f"✗ No IP to scan")
    except Exception as e:
        print(f"[!] Port scan failed: {e}")
    
    # MODULE 5: Cloud Provider Detection
    print("\n[5/10] CLOUD PROVIDER DETECTION")
    print("-" * 90)
    try:
        cloud_detector = CloudDetector()
        cloud_result = cloud_detector.detect_cloud(domain, dns_result if 'dns' in results['modules'] else None)
        
        providers = cloud_result.get('providers', [])
        if providers:
            print(f"✓ Providers: {', '.join(providers)}")
        else:
            print(f"✓ No major cloud/CDN providers detected")
        
        results['modules']['cloud'] = cloud_result
    except Exception as e:
        print(f"[!] Cloud detection failed: {e}")
    
    # MODULE 6: Technology Stack Detection
    print("\n[6/10] TECHNOLOGY STACK DETECTION")
    print("-" * 90)
    try:
        tech_detector = TechStackDetector()
        tech_result = tech_detector.detect_stack(domain)
        
        if 'error' not in tech_result:
            server = tech_result.get('server', 'Unknown')
            cms = tech_result.get('cms')
            frameworks = tech_result.get('frameworks', [])
            
            print(f"✓ Server: {server}")
            if cms:
                print(f"✓ CMS: {cms}")
            if frameworks:
                print(f"✓ Frameworks: {', '.join(frameworks)}")
        else:
            print(f"[!] Tech detection failed: {tech_result.get('error')}")
        
        results['modules']['tech_stack'] = tech_result
    except Exception as e:
        print(f"[!] Tech stack detection failed: {e}")
    
    # MODULE 7: Vulnerability Analysis
    print("\n[7/10] VULNERABILITY ANALYSIS")
    print("-" * 90)
    try:
        rules = VulnerabilityRules()
        port_list = []
        
        if 'ports' in results['modules'] and 'ports' in results['modules']['ports']:
            for port_info in results['modules']['ports']['ports']:
                port_list.append({
                    'port': port_info['port'],
                    'service': port_info.get('service', 'unknown'),
                    'state': 'open'
                })
        
        scan_data = {'open_ports': port_list}
        vulnerabilities = rules.analyze(scan_data)
        
        print(f"✓ Vulnerabilities Found: {len(vulnerabilities)}")
        
        for vuln in vulnerabilities[:5]:
            severity = vuln.severity if hasattr(vuln, 'severity') else 'UNKNOWN'
            title = vuln.title if hasattr(vuln, 'title') else 'Unknown'
            print(f"   [{severity}] {title}")
        
        results['modules']['vulnerabilities'] = [{
            'severity': str(v.severity),
            'title': v.title,
            'description': v.description
        } for v in vulnerabilities]
    except Exception as e:
        print(f"[!] Vulnerability analysis failed: {e}")
    
    # MODULE 8: GeoIP Lookup
    print("\n[8/10] GEOLOCATION & NETWORK")
    print("-" * 90)
    try:
        if public_ip:
            geo_lookup = GeoIPLookup()
            asn_lookup = ASNLookup()
            
            geo_result = geo_lookup.lookup(public_ip)
            asn_result = asn_lookup.lookup(public_ip)
            
            if 'country' in geo_result:
                print(f"✓ Country: {geo_result.get('country')}")
                print(f"✓ City: {geo_result.get('city')}")
                print(f"✓ ISP: {geo_result.get('isp')}")
            
            if 'asn' in asn_result:
                print(f"✓ ASN: {asn_result.get('asn')}")
                print(f"✓ Organization: {asn_result.get('organization')}")
            
            results['modules']['geoip'] = geo_result
            results['modules']['asn'] = asn_result
        else:
            print(f"✗ No IP to geolocate")
    except Exception as e:
        print(f"[!] Geolocation failed: {e}")
    
    # MODULE 9: Overall Risk Assessment
    print("\n[9/10] RISK ASSESSMENT")
    print("-" * 90)
    try:
        risk_score = 0
        risk_factors = []
        
        # SSL score
        if 'ssl' in results['modules']:
            ssl_data = results['modules']['ssl']
            if not ssl_data.get('ssl_enabled'):
                risk_score += 20
                risk_factors.append("No SSL certificate")
            elif ssl_data.get('vulnerabilities'):
                risk_score += 10
                risk_factors.append(f"{len(ssl_data['vulnerabilities'])} SSL issues")
        
        # Headers score
        if 'headers' in results['modules']:
            h_score = results['modules']['headers'].get('security_score', 100)
            if h_score < 50:
                risk_score += 15
                risk_factors.append("Poor security headers")
            elif h_score < 70:
                risk_score += 5
                risk_factors.append("Missing some security headers")
        
        # Vulnerabilities
        if 'vulnerabilities' in results['modules']:
            vuln_count = len(results['modules']['vulnerabilities'])
            risk_score += min(30, vuln_count * 5)
            if vuln_count > 0:
                risk_factors.append(f"{vuln_count} vulnerabilities found")
        
        risk_score = min(100, risk_score)
        risk_level = 'CRITICAL' if risk_score >= 80 else 'HIGH' if risk_score >= 60 else 'MEDIUM' if risk_score >= 40 else 'LOW'
        
        print(f"✓ Risk Score: {risk_score}/100 ({risk_level})")
        if risk_factors:
            print(f"[!] Risk Factors:")
            for factor in risk_factors:
                print(f"   - {factor}")
        
        results['risk_assessment'] = {
            'score': risk_score,
            'level': risk_level,
            'factors': risk_factors
        }
    except Exception as e:
        print(f"[!] Risk assessment failed: {e}")
    
    # MODULE 10: Summary
    print("\n[10/10] SUMMARY")
    print("-" * 90)
    print(f"✓ Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✓ Modules analyzed: {len([m for m in results['modules'] if m not in ['dns']])}")
    print(f"✓ Data: REAL-TIME (NOT CACHED)")
    
    return results

def save_analysis(results):
    """Save analysis to JSON"""
    if not results:
        return None
    
    # Convert all non-serializable objects
    clean_results = _clean_for_json(results)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = results['domain'].replace('.', '_')
    filename = f"reports/advanced_analysis_{domain}_{timestamp}.json"
    
    Path("reports").mkdir(exist_ok=True)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {e}")
        return None

def _clean_for_json(obj):
    """Convert non-JSON-serializable objects to strings"""
    if isinstance(obj, dict):
        return {k: _clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_clean_for_json(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        # Handle dataclass/object instances
        return str(obj)
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)

def main():
    """Main function"""
    print_header("[*] ADVANCED WEBSITE ANALYZER - PROFESSIONAL EDITION")
    print("Complete security assessment with 10 analysis modules")
    print("Real-time deep reconnaissance (no cache, no demo data)\n")
    
    # Get target
    print("Enter website URL (examples: google.com, github.com, example.com):")
    target = input("Website: ").strip()
    
    if not target:
        print("[!] No target specified")
        return
    
    print_header(f"[*] ANALYZING: {target}")
    
    # Analyze
    results = analyze_advanced(target)
    
    if not results:
        print("\n[ERROR] Analysis failed")
        return
    
    # Save
    print_header("SAVING RESULTS")
    filename = save_analysis(results)
    
    if filename:
        print(f"✓ Report saved: {filename}")
    
    # Summary
    print_header("ANALYSIS COMPLETE")
    print(f"Domain: {results['domain']}")
    print(f"Risk Level: {results.get('risk_assessment', {}).get('level', 'Unknown')}")
    print(f"Modules: {len(results['modules'])}")
    print(f"Time: {results['scan_timestamp']}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
