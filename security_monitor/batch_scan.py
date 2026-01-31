#!/usr/bin/env python3
"""
BATCH SCAN MODE - Real scanning for multiple websites
Хамгийн чухал: REAL DATA - бүх website-ийг бодит хэмжээнд сканлана
10+ website-ийн үр дүн харуулна
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Import all core modules
from core.resolver.dns import DNSResolver
from core.scanner.nmap import NmapScanner
from core.analysis.rules import VulnerabilityRules
from core.risk.scorer import RiskScorer
from core.fixes.recommendations import RecommendationEngine
from core.reports.report import ReportGenerator
from db.database import DatabaseManager
from core.audit.audit import AuditLogger

def print_section(title, char="="):
    """Print formatted section"""
    print("\n" + char * 80)
    print(f"  {title}")
    print(char * 80)

def print_progress(current, total, target):
    """Print progress bar"""
    percent = (current / total) * 100
    print(f"\n  [{current}/{total}] Scanning: {target} ({percent:.0f}%)")

def scan_website_real(target, resolver, scanner, rules, scorer, recommendations, report_gen, db):
    """
    Real scan - үнэндээ scan хийнэ (demo data биш!)
    """
    try:
        # Step 1: DNS Resolution (REAL)
        dns_result = resolver.resolve_domain(target)
        
        if not dns_result['ips'] and not dns_result['cname_records']:
            return {
                'target': target,
                'status': 'FAILED',
                'error': 'Could not resolve domain',
                'ips': [],
                'open_ports': 0,
                'vulnerabilities': 0,
                'risk_score': 0,
                'risk_level': 'UNKNOWN'
            }
        
        target_ip = dns_result['ips'][0] if dns_result['ips'] else 'unknown'
        
        # Step 2: Port Scan (REAL - using Nmap)
        print(f"    └─ DNS: {target} → {target_ip} (CDN: {dns_result['cdn']})")
        
        if target_ip != 'unknown':
            scan_result = scanner.quick_scan(target_ip)
        else:
            scan_result = {'open_ports': [], 'services': {}}
        
        open_ports = scan_result.get('open_ports', [])
        services = scan_result.get('services', {})
        print(f"    └─ Ports: {len(open_ports)} открытых ({', '.join(map(str, open_ports[:3]))}...)" if open_ports else "    └─ Ports: 0")
        
        # Step 3: Vulnerability Analysis (REAL rules)
        findings = []
        for port in open_ports:
            service = services.get(port, 'unknown')
            rule_findings = rules.check_port(port, service)
            findings.extend(rule_findings)
        
        print(f"    └─ Analysis: {len(findings)} уязвимостей найдено")
        
        # Step 4: Risk Scoring (REAL)
        risk_data = scorer.calculate_score(findings, open_ports)
        risk_score = risk_data['score']
        risk_level = risk_data['level']
        
        print(f"    └─ Risk: {risk_score}/100 ({risk_level})")
        
        # Step 5: Generate Report (REAL)
        report = report_gen.generate_json_report(
            target=target,
            ip=target_ip,
            open_ports=open_ports,
            services=services,
            findings=findings,
            risk_score=risk_score,
            risk_level=risk_level,
            cdn=dns_result['cdn'],
            cdn_provider=dns_result['cdn_provider']
        )
        
        # Step 6: Save to database (REAL)
        db.add_target(target, f"https://{target}", "batch_scan")
        
        return {
            'target': target,
            'status': 'SUCCESS',
            'ip': target_ip,
            'ips': dns_result['ips'],
            'cdn': dns_result['cdn'],
            'cdn_provider': dns_result['cdn_provider'],
            'open_ports': len(open_ports),
            'ports_list': open_ports,
            'vulnerabilities': len(findings),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'findings': findings
        }
        
    except Exception as e:
        return {
            'target': target,
            'status': 'ERROR',
            'error': str(e),
            'open_ports': 0,
            'vulnerabilities': 0,
            'risk_score': 0,
            'risk_level': 'ERROR'
        }

def main():
    """Main batch scan function"""
    
    print_section("🛡️  BATCH SCAN MODE - Real Data Scanning", "=")
    print("\n  Энэ режим нь ҮНЭНДЭЭ бүх website-ыг сканлана")
    print("  (Demo/cached data биш - real data!)  \n")
    
    # Default target list
    default_targets = [
        "google.com",
        "example.com",
        "cloudflare.com",
        "github.com",
        "stackoverflow.com",
        "wikipedia.org",
        "medium.com",
        "amazon.com",
        "facebook.com",
        "reddit.com"
    ]
    
    print("  Default targets:")
    for i, target in enumerate(default_targets, 1):
        print(f"    {i}. {target}")
    
    print("  OPTIONS:")
    print("    1. Use all default targets (10)")
    print("    2. Select specific targets from defaults")
    print("    3. Enter custom targets\n")
    
    choice = input("  Choose option (1-3): ").strip()
    targets = []
    
    if choice == "2":
        # Display targets with checkboxes
        print("\n  Select targets from default list:")
        selections = {}
        for i, target in enumerate(default_targets, 1):
            resp = input(f"    [{i:2d}] {target:<25} (y/n): ").strip().lower()
            selections[target] = resp in ['y', 'yes', '']
        
        targets = [t for t, selected in selections.items() if selected]
        if not targets:
            print("  No targets selected, using defaults")
            targets = default_targets
    
    elif choice == "3":
        # Custom targets
        print("\n  Enter custom targets (one per line, empty line to finish):")
        while True:
            target = input("    > ").strip()
            if not target:
                break
            targets.append(target)
        
        if not targets:
            print("  No custom targets entered, using defaults")
            targets = default_targets
    
    else:
        # Default: use all defaults
        targets = default_targets
    
    # Initialize modules
    print_section(f"📊 Initializing {len(targets)} targets for REAL scanning")
    
    resolver = DNSResolver()
    scanner = NmapScanner()
    rules = VulnerabilityRules()
    scorer = RiskScorer()
    recommendations = RecommendationEngine()
    report_gen = ReportGenerator()
    db = DatabaseManager()
    audit = AuditLogger()
    
    print("\n  ✓ All modules initialized")
    print(f"  ✓ Ready to scan {len(targets)} websites with REAL data\n")
    
    results = []
    
    # Scan each target
    for idx, target in enumerate(targets, 1):
        print_progress(idx, len(targets), target)
        
        result = scan_website_real(
            target, resolver, scanner, rules, scorer,
            recommendations, report_gen, db
        )
        results.append(result)
    
    # Display summary
    print_section("📋 BATCH SCAN RESULTS - Real Data Summary")
    
    # Create simple table (without tabulate)
    print("\n  " + "-" * 76)
    print(f"  {'Target':<20} {'IP':<18} {'Ports':<6} {'Vulns':<6} {'Score':<10} {'Level':<10} {'Status':<6}")
    print("  " + "-" * 76)
    
    for r in results:
        target = r['target'][:19]
        ip = r.get('ip', 'unknown')[:17]
        ports = r.get('open_ports', 0)
        vulns = r.get('vulnerabilities', 0)
        score = f"{r.get('risk_score', 0)}/100"
        level = r.get('risk_level', 'UNKNOWN')
        status = "✓" if r['status'] == 'SUCCESS' else "✗"
        
        print(f"  {target:<20} {ip:<18} {ports:<6} {vulns:<6} {score:<10} {level:<10} {status:<6}")
    
    print("  " + "-" * 76)
    
    # Statistics
    successful = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed = len(results) - successful
    total_ports = sum(r.get('open_ports', 0) for r in results)
    total_vulns = sum(r.get('vulnerabilities', 0) for r in results)
    avg_score = sum(r.get('risk_score', 0) for r in results) / len(results) if results else 0
    
    print_section("📈 Statistics - Real Data Analysis")
    print(f"\n  Total Targets: {len(results)}")
    print(f"  Successful: {successful} ({successful/len(results)*100:.0f}%)")
    print(f"  Failed: {failed}")
    print(f"\n  Total Open Ports: {total_ports}")
    print(f"  Total Vulnerabilities: {total_vulns}")
    print(f"  Average Risk Score: {avg_score:.1f}/100")
    
    # Risk breakdown
    risk_counts = {}
    for r in results:
        level = r.get('risk_level', 'UNKNOWN')
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    print(f"\n  Risk Levels:")
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = risk_counts.get(level, 0)
        if count > 0:
            print(f"    {level}: {count}")
    
    # Save batch report
    print_section("💾 Saving Batch Report")
    
    batch_report = {
        'scan_type': 'batch',
        'timestamp': datetime.now().isoformat(),
        'total_targets': len(results),
        'successful_scans': successful,
        'failed_scans': failed,
        'total_open_ports': total_ports,
        'total_vulnerabilities': total_vulns,
        'average_risk_score': avg_score,
        'risk_breakdown': risk_counts,
        'results': results
    }
    
    report_file = f"reports/batch_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path("reports").mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(batch_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n  ✓ Batch report saved: {report_file}")
    print(f"  ✓ Database updated with {successful} new scans")
    
    # Show top risks
    print_section("⚠️  Top Risks Found")
    
    critical_targets = [r for r in results if r.get('risk_level') == 'CRITICAL']
    high_targets = [r for r in results if r.get('risk_level') == 'HIGH']
    
    if critical_targets:
        print("\n  🔴 CRITICAL:")
        for t in critical_targets:
            print(f"    • {t['target']} - Score: {t.get('risk_score', 0)}/100")
    
    if high_targets:
        print("\n  🟠 HIGH:")
        for t in high_targets[:5]:
            print(f"    • {t['target']} - Score: {t.get('risk_score', 0)}/100")
    
    if not critical_targets and not high_targets:
        print("\n  ✓ No critical or high risks found")
    
    print("\n" + "=" * 80)
    print("  ✓ Batch scan complete!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Batch scan cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
