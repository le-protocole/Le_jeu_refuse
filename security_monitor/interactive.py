#!/usr/bin/env python3
"""
Interactive CLI Menu System
User-friendly terminal interface with numbered options
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import all core modules
from core.resolver.dns import DNSResolver
from core.scanner.nmap import NmapScanner
from core.analysis.rules import VulnerabilityRules
from core.risk.scorer import RiskScorer
from core.fixes.recommendations import RecommendationEngine
from core.reports.report import ReportGenerator
from db.database import DatabaseManager
from core.audit.audit import AuditLogger

class InteractiveCLI:
    """Interactive command-line interface"""
    
    def __init__(self):
        self.resolver = DNSResolver()
        self.scanner = NmapScanner()
        self.rules = VulnerabilityRules()
        self.scorer = RiskScorer()
        self.recommendations = RecommendationEngine()
        self.report_gen = ReportGenerator()
        self.db = DatabaseManager()
        self.audit = AuditLogger()
        
        # Create necessary directories
        Path("reports").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
    
    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if sys.platform == 'win32' else 'clear')
    
    def print_banner(self):
        """Print application banner"""
        print("\n" + "=" * 80)
        print("  SECURITY MONITORING SYSTEM - INTERACTIVE MODE")
        print("  Version 1.0 | Blue-Team Security Posture Scanner")
        print("=" * 80)
    
    def print_menu(self):
        """Print main menu"""
        print("\n" + "-" * 80)
        print("  MAIN MENU - Choose an option:")
        print("-" * 80)
        print("  1. Scan a website or IP address")
        print("  2. View previous scan results")
        print("  3. Generate security report")
        print("  4. View vulnerability database")
        print("  5. System settings & configuration")
        print("  6. Exit")
        print("-" * 80)
    
    def get_choice(self, prompt="Choose option: ", valid_options=None):
        """Get user input with validation"""
        while True:
            try:
                choice = input(f"\n{prompt}").strip()
                
                if valid_options and choice not in valid_options:
                    print(f"  [ERROR] Invalid choice. Please enter one of: {', '.join(valid_options)}")
                    continue
                
                return choice
            except KeyboardInterrupt:
                print("\n\n[!] Cancelled by user")
                return None
            except Exception as e:
                print(f"  [ERROR] {str(e)}")
    
    def scan_target(self):
        """Interactive scan workflow"""
        print("\n" + "=" * 80)
        print("  SCAN TARGET - Website or IP Address")
        print("=" * 80)
        
        # Get target input
        target = input("\nEnter target URL or IP address: ").strip()
        if not target:
            print("  [ERROR] Target cannot be empty")
            return
        
        print(f"\n  Resolving: {target}...")
        
        # Step 1: DNS Resolution
        dns_result = self.resolver.resolve_domain(target)
        
        if not dns_result['ips'] and not dns_result['cname_records']:
            print(f"  [ERROR] Could not resolve {target}")
            return
        
        target_ip = dns_result['ips'][0] if dns_result['ips'] else None
        
        if not target_ip:
            print(f"  [ERROR] No IP address found")
            return
        
        print(f"  ✓ Resolved: {dns_result['target']}")
        print(f"    IP Address: {target_ip}")
        
        if dns_result['cdn']:
            print(f"    [!] Behind CDN: {dns_result['cdn_provider']}")
        
        # Choose scan type
        print("\n" + "-" * 80)
        print("  SELECT SCAN TYPE:")
        print("-" * 80)
        print("  1. Quick scan (fast, common ports only) - ~2 minutes")
        print("  2. Standard scan (thorough, top 10k ports) - ~10 minutes")
        print("  3. Deep scan (comprehensive, all ports) - ~30 minutes")
        print("-" * 80)
        
        scan_type = self.get_choice("Choose scan type (1-3): ", ["1", "2", "3"])
        if not scan_type:
            return
        
        scan_map = {
            "1": ("quick", "Quick Scan"),
            "2": ("standard", "Standard Scan"),
            "3": ("thorough", "Deep Scan")
        }
        
        scan_mode, scan_label = scan_map[scan_type]
        
        # Confirmation
        print("\n" + "-" * 80)
        print(f"  SCAN SUMMARY:")
        print("-" * 80)
        print(f"  Target: {dns_result['target']} ({target_ip})")
        print(f"  Scan Type: {scan_label}")
        print(f"  CDN: {'Yes' if dns_result['cdn'] else 'No'}")
        print("-" * 80)
        
        confirm = self.get_choice("Start scan? (yes/no): ", ["yes", "no", "y", "n"])
        if confirm not in ["yes", "y"]:
            print("  [CANCELLED] Scan aborted")
            return
        
        # Perform scan
        print(f"\n  Running {scan_label.lower()}...")
        
        if scan_mode == "quick":
            scan_result = self.scanner.quick_scan(target_ip)
        elif scan_mode == "standard":
            scan_result = self.scanner.standard_scan(target_ip)
        else:
            scan_result = self.scanner.thorough_scan(target_ip)
        
        if not scan_result or 'error' in scan_result:
            print(f"  [ERROR] Scan failed - Nmap not available or unreachable target")
            print(f"  [INFO] Skipping target (real scan required)\n")
            return None
        
        open_ports = scan_result.get('ports', [])
        print(f"  ✓ Scan complete! Found {len(open_ports)} open port(s)")
        
        for port_info in open_ports[:5]:
            print(f"    → Port {port_info['port']}: {port_info['state']} ({port_info.get('service', 'unknown')})")
        
        if len(open_ports) > 5:
            print(f"    ... and {len(open_ports) - 5} more")
        
        # Analyze findings
        print(f"\n  Analyzing vulnerabilities...")
        findings = self.rules.analyze(scan_result)
        print(f"  ✓ Found {len(findings)} issue(s)")
        
        for finding in findings[:3]:
            print(f"    → [{finding.severity.value}] {finding.title}")
        
        # Calculate risk
        print(f"\n  Calculating risk score...")
        risk_score = self.scorer.calculate_score(
            findings=[{
                'severity': f.severity.value,
                'title': f.title,
                'description': f.description
            } for f in findings],
            open_ports=open_ports
        )
        print(f"  ✓ Risk Score: {risk_score['score']}/100 ({risk_score['level'].value})")
        
        # Generate recommendations
        print(f"\n  Generating recommendations...")
        fixes = []
        for finding in findings[:3]:
            finding_dict = {
                'title': finding.title,
                'severity': finding.severity.value,
                'description': finding.description
            }
            recs = self.recommendations.get_recommendations_for_finding(finding_dict)
            fixes.extend(recs)
        
        print(f"  ✓ Generated {len(fixes)} recommendation(s)")
        
        for fix in fixes[:3]:
            print(f"    → [{fix.difficulty}] {fix.title}")
        
        # Generate report
        print(f"\n  Generating report...")
        report_data = {
            "scan_date": datetime.now().isoformat(),
            "target": dns_result['target'],
            "ip_address": target_ip,
            "behind_cdn": dns_result['cdn'],
            "cdn_provider": dns_result['cdn_provider'],
            "open_ports": open_ports,
            "findings_count": len(findings),
            "risk_score": risk_score['score'],
            "risk_level": risk_score['level'].value,
            "findings": [
                {
                    "severity": f.severity.value,
                    "title": f.title,
                    "description": f.description
                }
                for f in findings[:5]
            ],
            "recommendations": [
                {
                    "title": f.title,
                    "difficulty": f.difficulty,
                    "description": f.description
                }
                for f in fixes[:5]
            ]
        }
        
        report_file = f"reports/{dns_result['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"  ✓ Report saved: {report_file}")
        
        # Summary
        print("\n" + "=" * 80)
        print("  SCAN COMPLETE")
        print("=" * 80)
        print(f"  Target: {dns_result['target']} ({target_ip})")
        print(f"  Open Ports: {len(open_ports)}")
        print(f"  Vulnerabilities: {len(findings)}")
        print(f"  Risk Level: {risk_score['level'].value}")
        print(f"  Report: {report_file}")
        print("=" * 80)
    
    def view_reports(self):
        """View previous scan reports"""
        print("\n" + "=" * 80)
        print("  PREVIOUS SCAN REPORTS")
        print("=" * 80)
        
        report_files = list(Path("reports").glob("*.json"))
        
        if not report_files:
            print("  [INFO] No reports found yet")
            return
        
        print(f"\n  Found {len(report_files)} report(s):\n")
        
        for i, report_file in enumerate(sorted(report_files, reverse=True)[:10], 1):
            print(f"  {i}. {report_file.name}")
        
        print("\n")
    
    def show_database(self):
        """Show vulnerability database"""
        print("\n" + "=" * 80)
        print("  VULNERABILITY DATABASE")
        print("=" * 80)
        
        print("\n  Vulnerability Rules Available:")
        print("  " + "-" * 76)
        
        rules_list = [
            ("SSH", "Port 22 - Password authentication enabled"),
            ("FTP", "Port 21 - Plaintext file transfer protocol"),
            ("MySQL", "Port 3306 - Database exposed to public"),
            ("PostgreSQL", "Port 5432 - Database exposed to public"),
            ("MongoDB", "Port 27017 - NoSQL database exposed"),
            ("Redis", "Port 6379 - Cache server exposed"),
            ("RDP", "Port 3389 - Remote Desktop Protocol (ransomware vector)"),
            ("VNC", "Port 5900 - Virtual Network Computing"),
            ("SMB", "Port 445 - Server Message Block (LAN)"),
            ("Telnet", "Port 23 - Legacy insecure protocol"),
            ("SNMP", "Port 161 - Simple Network Management Protocol"),
            ("Memcached", "Port 11211 - DDoS amplification vector"),
            ("UPnP", "Port 1900 - Universal Plug and Play"),
            ("HTTP", "Port 80 - Unencrypted web traffic"),
            ("Outdated Software", "Service version detection"),
        ]
        
        for service, description in rules_list:
            print(f"  • {service:15s} - {description}")
        
        print("  " + "-" * 76)
        print(f"\n  Total Rules: {len(rules_list)}")
        print("=" * 80)
    
    def show_settings(self):
        """Show system settings"""
        print("\n" + "=" * 80)
        print("  SYSTEM SETTINGS")
        print("=" * 80)
        
        from core.config.settings import (
            DATABASE_PATH, NMAP_TIMEOUT, COMMON_PORTS,
            RISK_THRESHOLDS, REPORT_FORMATS
        )
        
        print(f"\n  Database Path: {DATABASE_PATH}")
        print(f"  Nmap Timeout: {NMAP_TIMEOUT} seconds")
        print(f"  Common Ports: {len(COMMON_PORTS)} ports")
        print(f"    {', '.join(map(str, COMMON_PORTS[:5]))} ...")
        print(f"\n  Risk Thresholds:")
        print(f"    LOW: 0-30")
        print(f"    MEDIUM: 31-60")
        print(f"    HIGH: 61-80")
        print(f"    CRITICAL: 81-100")
        print(f"\n  Report Formats: {', '.join(REPORT_FORMATS)}")
        print("\n" + "=" * 80)
    
    def main_loop(self):
        """Main interactive loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = self.get_choice("Enter your choice (1-6): ", ["1", "2", "3", "4", "5", "6"])
            
            if not choice:
                break
            
            if choice == "1":
                self.scan_target()
            elif choice == "2":
                self.view_reports()
            elif choice == "3":
                print("\n[INFO] Report generation - coming soon")
            elif choice == "4":
                self.show_database()
            elif choice == "5":
                self.show_settings()
            elif choice == "6":
                print("\n  Thank you for using Security Monitoring System!")
                print("  Exiting...\n")
                break
            
            input("\nPress Enter to continue...")

def main():
    """Entry point"""
    try:
        cli = InteractiveCLI()
        cli.main_loop()
    except KeyboardInterrupt:
        print("\n\n[!] Application interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
