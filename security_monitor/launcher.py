#!/usr/bin/env python3
"""
Security Monitoring System - Unified Launcher
Choose between Terminal CLI or Web UI
"""

import subprocess
import sys
import os
from pathlib import Path

def clear_screen():
    """Clear terminal"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def print_banner():
    """Print banner"""
    print("\n" + "=" * 80)
    print("  SECURITY MONITORING SYSTEM - LAUNCHER")
    print("  Choose your interface")
    print("=" * 80 + "\n")

def print_menu():
    """Print main menu"""
    print("Select interface mode:")
    print("-" * 80)
    print("  1. Terminal CLI (Interactive Menu - REAL DATA)")
    print("  2. Web UI (Browser - REAL DATA)")
    print("  3. Batch Scan Mode (10+ websites - REAL DATA)")
    print("  4. Website Analyzer (Random URL - Real-time Deep Scan)")
    print("  5. Advanced Analyzer (Professional - 10 Modules)")
    print("  6. Enhanced Tools (Export, Compliance, CVE, Profiles, Charts)")
    print("  7. Integration Test (Full workflow - REAL DATA)")
    print("  8. Exit")
    print("-" * 80)

def get_choice(prompt="Enter your choice (1-8): "):
    """Get user choice"""
    while True:
        try:
            choice = input(f"\n{prompt}").strip()
            if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                return choice
            print("  [ERROR] Invalid choice. Please enter 1-8")
        except KeyboardInterrupt:
            print("\n\n[!] Cancelled")
            sys.exit(0)
        except Exception as e:
            print(f"  [ERROR] {str(e)}")

def run_interactive_cli():
    """Run terminal CLI"""
    print("\n" + "=" * 80)
    print("  Starting Terminal CLI...")
    print("=" * 80 + "\n")
    
    try:
        subprocess.run([sys.executable, "interactive.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run interactive CLI: {str(e)}")
        input("\nPress Enter to return to menu...")

def run_web_server():
    """Run web server"""
    print("\n" + "=" * 80)
    print("  Starting Web Server...")
    print("=" * 80)
    print("\n[*] Server starting...\n")
    
    try:
        # Show instructions
        print("  Web Interface: http://localhost:8000")
        print("  API Docs: http://localhost:8000/docs")
        print("  Status: http://localhost:8000/api/health")
        print("\n  Press CTRL+C to stop\n")
        print("=" * 80 + "\n")
        
        # Run server
        subprocess.run([sys.executable, "web_server.py"], check=False)
        
    except KeyboardInterrupt:
        print("\n\n[!] Web server stopped")
    except Exception as e:
        print(f"[ERROR] Failed to run web server: {str(e)}")
    finally:
        input("\nPress Enter to return to menu...")

def run_integration_test():
    """Run integration test"""
    print("\n" + "=" * 80)
    print("  Running Integration Test...")
    print("=" * 80 + "\n")
    
    try:
        subprocess.run([sys.executable, "integration_test.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run integration test: {str(e)}")
    finally:
        input("\nPress Enter to return to menu...")

def run_batch_scan():
    """Run batch scan for multiple websites"""
    print("\n" + "=" * 80)
    print("  Batch Scan Mode - Real Data")
    print("=" * 80 + "\n")
    
    try:
        subprocess.run([sys.executable, "batch_scan.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run batch scan: {str(e)}")
    finally:
        input("\nPress Enter to return to menu...")

def run_website_analyzer():
    """Run advanced website analyzer"""
    print("\n" + "=" * 80)
    print("  Advanced Website Analyzer - Professional Edition")
    print("=" * 80 + "\n")
    
    try:
        subprocess.run([sys.executable, "advanced_analyzer.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run advanced analyzer: {str(e)}")
    finally:
        input("\nPress Enter to return to menu...")
def run_advanced_analyzer():
    """Run professional advanced analyzer"""
    print("\n" + "=" * 80)
    print("  Professional Advanced Analyzer - 10 Module Deep Scan")
    print("=" * 80 + "\n")
    
    try:
        subprocess.run([sys.executable, "advanced_analyzer.py"], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run advanced analyzer: {str(e)}")
    finally:
        input("\nPress Enter to return to menu...")

def run_enhanced_tools():
    """Run enhanced tools suite"""
    print("\n" + "=" * 80)
    print("  Enhanced Tools Suite")
    print("=" * 80)
    print("\nNew Features:")
    print("  [1] PDF/CSV Report Export")
    print("  [2] Compliance Checker (CIS/OWASP/PCI-DSS)")
    print("  [3] CVE Database Lookup")
    print("  [4] Scan Profile Manager")
    print("  [5] Performance Charts & Analytics")
    print("  [6] Remediation Guide Generator")
    print("  [7] Back to Main Menu")
    print("\n" + "=" * 80)
    
    sub_choice = input("\nSelect tool (1-7): ").strip()
    
    try:
        if sub_choice == "1":
            print("\n[*] PDF/CSV Export Feature")
            print("    Usage: Use after running a scan to export results")
            demo_code = """
from core.reports.export_manager import ExportManager

manager = ExportManager()
# Export to CSV
manager.export_to_csv(scan_data)
# Export to PDF (requires reportlab)
manager.export_to_pdf(scan_data)
# Export to JSON
manager.export_json(scan_data)
            """
            print(demo_code)
        
        elif sub_choice == "2":
            print("\n[*] Compliance Checker")
            print("    Supports: CIS Controls, OWASP Top 10, PCI-DSS")
            demo_code = """
from core.security.compliance_checker import ComplianceChecker

checker = ComplianceChecker()
results = checker.evaluate_all(scan_data)
print(f"CIS Score: {results['cis_score']}%")
print(f"OWASP Score: {results['owasp_score']}%")
print(f"PCI-DSS Score: {results['pci_score']}%")
            """
            print(demo_code)
        
        elif sub_choice == "3":
            print("\n[*] CVE Database Lookup")
            print("    Fetches vulnerability data from NVD")
            demo_code = """
from core.database.cve_fetcher import CVEFetcher

fetcher = CVEFetcher()
vulns = fetcher.search_cve_by_software('apache')
for vuln in vulns['vulnerabilities']:
    print(f"{vuln['cve_id']}: {vuln['severity']}")
            """
            print(demo_code)
        
        elif sub_choice == "4":
            print("\n[*] Scan Profile Manager")
            print("    Predefined profiles: quick, standard, pci_dss, owasp, infrastructure")
            demo_code = """
from core.config.profile_manager import ProfileManager

manager = ProfileManager()
# Get predefined profiles
profiles = manager.get_predefined_profiles()
# Create custom profile
manager.create_custom_profile({'name': 'My Profile', ...})
# List all profiles
manager.list_all_profiles()
            """
            print(demo_code)
        
        elif sub_choice == "5":
            print("\n[*] Performance Charts & Analytics")
            print("    Requires: matplotlib")
            demo_code = """
from core.reports.performance_charts import PerformanceChartGenerator

generator = PerformanceChartGenerator()
# Risk trend chart
generator.generate_risk_trend_chart(scan_history)
# Compliance scorecard
generator.generate_compliance_scorecard(compliance_data)
# Module coverage
generator.generate_module_coverage_chart(modules)
            """
            print(demo_code)
        
        elif sub_choice == "6":
            print("\n[*] Remediation Guide Generator")
            print("    Generates fix recommendations based on findings")
            demo_code = """
from core.analysis.remediation_guide import RemediationGuide

guide = RemediationGuide()
plan = guide.generate_remediation_plan(scan_data)
roadmap = guide.generate_roadmap(plan)
for phase in roadmap['phases']:
    print(f"{phase['phase']}: {phase['timeline']}")
            """
            print(demo_code)
        
        elif sub_choice == "7":
            return
        
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        input("\nPress Enter to continue...")

def main():
    """Main launcher loop"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = get_choice()
        
        if choice == "1":
            run_interactive_cli()
        elif choice == "2":
            run_web_server()
        elif choice == "3":
            run_batch_scan()
        elif choice == "4":
            run_website_analyzer()
        elif choice == "5":
            run_advanced_analyzer()
        elif choice == "6":
            run_enhanced_tools()
        elif choice == "7":
            run_integration_test()
        elif choice == "8":
            print("\n  Thank you for using Security Monitoring System!")
            print("  Exiting...\n")
            sys.exit(0)

if __name__ == "__main__":
    try:
        # Check if we're in the right directory
        if not Path("core").exists() or not Path("db").exists():
            print("[ERROR] Please run this script from the security_monitor directory")
            sys.exit(1)
        
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Application interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
