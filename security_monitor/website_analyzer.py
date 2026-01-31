#!/usr/bin/env python3
"""
ADVANCED WEBSITE ANALYZER - Real-Time Website Reconnaissance
Бодит website-ийн IP, service, CDN detection - Real-time data only!
Demo data үгүй - зөвхөн REAL scanning
"""

import socket
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess
import platform

# Import modules
from core.resolver.dns import DNSResolver
from core.scanner.nmap import NmapScanner
from core.analysis.rules import VulnerabilityRules

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def sanitize_url(url):
    """Sanitize URL to get domain only"""
    url = url.lower().strip()
    # Remove protocol
    if '://' in url:
        url = url.split('://', 1)[1]
    # Remove www
    if url.startswith('www.'):
        url = url[4:]
    # Remove path
    if '/' in url:
        url = url.split('/', 1)[0]
    # Remove port
    if ':' in url:
        url = url.split(':', 1)[0]
    return url

def get_public_ip(domain):
    """Get public IP via socket"""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def get_reverse_dns(ip):
    """Get reverse DNS (hostname from IP)"""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except:
        return None

def check_service_on_port(host, port):
    """Check if port is open and get service"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_service_name(port):
    """Get common service name for port"""
    services = {
        21: "FTP",
        22: "SSH",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        27017: "MongoDB"
    }
    return services.get(port, "Unknown")

def scan_common_ports(host):
    """Quick scan of common ports"""
    common_ports = [
        21, 22, 25, 53, 80, 110, 143, 443, 445,
        3306, 3389, 5432, 5900, 8080, 8443, 27017
    ]
    
    open_ports = {}
    print("  Сканлаж байна... (checking ports)")
    
    for port in common_ports:
        if check_service_on_port(host, port):
            service = get_service_name(port)
            open_ports[port] = service
            print(f"    ✓ Port {port}: {service}")
    
    return open_ports

def detect_cdn(domain, dns_result):
    """Detect CDN from DNS resolution"""
    cdn_providers = {
        'cloudflare': ['cloudflare', 'cf', 'cname.cloudflare'],
        'akamai': ['akamai'],
        'aws': ['cloudfront', 'aws'],
        'azure': ['azureedge', 'azure'],
        'google': ['goog', 'google'],
        'fastly': ['fastly'],
        'level3': ['level3', 'limelight']
    }
    
    cname_records = dns_result.get('cname_records', [])
    
    for cname in cname_records:
        cname_lower = cname.lower()
        for provider, keywords in cdn_providers.items():
            for keyword in keywords:
                if keyword in cname_lower:
                    return True, provider, cname
    
    return False, None, None

def analyze_website(target):
    """Analyze website with REAL data"""
    
    print_header(f"🔍 ANALYZING: {target}")
    
    # Step 1: Sanitize
    domain = sanitize_url(target)
    print(f"[*] Target domain: {domain}")
    
    # Step 2: DNS Resolution (REAL)
    print("\n[1/6] DNS RESOLUTION (Real-time)")
    print("-" * 80)
    
    resolver = DNSResolver()
    dns_result = resolver.resolve_domain(domain)
    
    if not dns_result['ips'] and not dns_result['cname_records']:
        print(f"✗ Could not resolve {domain}")
        return None
    
    public_ip = dns_result['ips'][0] if dns_result['ips'] else None
    print(f"✓ Domain: {domain}")
    print(f"✓ Public IP(s): {', '.join(dns_result['ips'])}")
    
    if dns_result['cname_records']:
        print(f"✓ CNAME Records: {len(dns_result['cname_records'])}")
        for cname in dns_result['cname_records']:
            print(f"   └─ {cname}")
    
    # Step 3: Reverse DNS
    print("\n[2/6] REVERSE DNS (Hidden hostname)")
    print("-" * 80)
    
    if public_ip:
        reverse_hostname = get_reverse_dns(public_ip)
        if reverse_hostname:
            print(f"✓ Reverse DNS: {reverse_hostname}")
            print(f"   (Hidden hostname from IP)")
        else:
            print(f"✗ No reverse DNS (hidden)")
    
    # Step 4: CDN Detection
    print("\n[3/6] CDN / SERVICE DETECTION")
    print("-" * 80)
    
    is_cdn, cdn_provider, cdn_cname = detect_cdn(domain, dns_result)
    
    if is_cdn:
        print(f"✓ Behind CDN: YES")
        print(f"✓ Provider: {cdn_provider.upper()}")
        print(f"✓ CNAME: {cdn_cname}")
    else:
        print(f"✓ Behind CDN: NO (Direct server)")
    
    # Step 5: Port Scanning (REAL)
    print("\n[4/6] PORT SCANNING (Real-time)")
    print("-" * 80)
    
    if public_ip:
        open_ports = scan_common_ports(public_ip)
        
        if not open_ports:
            print("✗ No common ports open")
        else:
            print(f"\n✓ Total open ports: {len(open_ports)}")
    else:
        print("✗ Cannot scan ports (no IP)")
        open_ports = {}
    
    # Step 6: Service Detection & Vulnerability Check
    print("\n[5/6] SERVICE ANALYSIS")
    print("-" * 80)
    
    # Build scan data for vulnerability analysis
    port_list = []
    for port, service in open_ports.items():
        port_list.append({
            "port": port,
            "service": service,
            "state": "open"
        })
        
        # Print service info
        if service == "HTTP":
            print(f"✓ Port {port}: Web Server (HTTP)")
            print(f"   └─ Check: Missing HTTPS redirect?")
        elif service == "HTTPS":
            print(f"✓ Port {port}: Secure Web (HTTPS)")
            print(f"   └─ Check: Valid certificate?")
        elif service == "SSH":
            print(f"✓ Port {port}: SSH Server")
            print(f"   └─ Check: Password auth enabled?")
        elif service == "MySQL" or service == "PostgreSQL":
            print(f"✓ Port {port}: Database ({service})")
            print(f"   └─ Check: Public access? CRITICAL!")
        else:
            print(f"✓ Port {port}: {service}")
    
    # Step 7: Vulnerability Check
    print("\n[6/6] VULNERABILITY CHECK")
    print("-" * 80)
    
    rules = VulnerabilityRules()
    scan_data = {"open_ports": port_list}
    vulnerabilities = rules.analyze(scan_data)
    
    if vulnerabilities:
        print(f"✓ Found {len(vulnerabilities)} potential issues:")
        for vuln in vulnerabilities:
            severity = vuln.severity if hasattr(vuln, 'severity') else 'UNKNOWN'
            desc = vuln.description if hasattr(vuln, 'description') else 'Unknown'
            print(f"   [{severity}] {desc}")
    else:
        print("✓ No known vulnerabilities detected")
    
    # Compile results
    results = {
        'scan_timestamp': datetime.now().isoformat(),
        'domain': domain,
        'public_ip': public_ip,
        'reverse_dns': get_reverse_dns(public_ip) if public_ip else None,
        'is_cdn': is_cdn,
        'cdn_provider': cdn_provider,
        'cname_records': dns_result['cname_records'],
        'all_ips': dns_result['ips'],
        'open_ports': open_ports,
        'vulnerabilities': vulnerabilities,
        'data_source': 'REAL-TIME SCAN (NOT CACHED)'
    }
    
    return results

def save_analysis(results):
    """Save analysis to JSON"""
    if not results:
        return None
    
    # Convert Finding objects to dictionaries for JSON serialization
    if 'vulnerabilities' in results and results['vulnerabilities']:
        vulnerabilities_list = []
        for vuln in results['vulnerabilities']:
            if hasattr(vuln, '__dict__'):
                # It's a Finding object (dataclass)
                vuln_dict = {
                    'severity': str(vuln.severity),
                    'title': vuln.title,
                    'description': vuln.description,
                    'affected_asset': vuln.affected_asset,
                    'evidence': vuln.evidence,
                    'cve_reference': vuln.cve_reference,
                    'mitigation': vuln.mitigation
                }
                vulnerabilities_list.append(vuln_dict)
            else:
                vulnerabilities_list.append(vuln)
        results['vulnerabilities'] = vulnerabilities_list
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = results['domain'].replace('.', '_')
    filename = f"reports/website_analysis_{domain}_{timestamp}.json"
    
    Path("reports").mkdir(exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return filename

def main():
    """Main function"""
    
    print_header("🔍 ADVANCED WEBSITE ANALYZER - Real-Time Reconnaissance")
    print("Бодит website-ийн IP, ports, services, CDN detection")
    print("Real-time data ONLY (no cache, no demo data)\n")
    
    # Get target
    print("Enter website URL (examples: google.com, github.com, example.com):")
    target = input("Website: ").strip()
    
    if not target:
        print("[ERROR] No target provided")
        return
    
    # Analyze
    results = analyze_website(target)
    
    if not results:
        print("\n[ERROR] Could not analyze website")
        return
    
    # Save
    print("\n" + "=" * 80)
    print("  SAVING RESULTS")
    print("=" * 80 + "\n")
    
    filename = save_analysis(results)
    if filename:
        print(f"✓ Report saved: {filename}")
    
    # Display summary
    print_header("📋 ANALYSIS SUMMARY")
    
    print(f"Domain: {results['domain']}")
    print(f"Public IP: {results['public_ip']}")
    print(f"Reverse DNS: {results['reverse_dns'] or 'N/A'}")
    print(f"Behind CDN: {'YES - ' + results['cdn_provider'].upper() if results['is_cdn'] else 'NO'}")
    print(f"Open Ports: {len(results['open_ports'])}")
    print(f"Vulnerabilities: {len(results['vulnerabilities'])}")
    print(f"Scan Time: {results['scan_timestamp']}")
    print(f"Data Source: {results['data_source']}")
    
    # Show ports
    print("\nOpen Ports & Services:")
    for port, service in results['open_ports'].items():
        print(f"  {port:5} → {service}")
    
    print("\n" + "=" * 80)
    print("✓ Real-time analysis complete!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
