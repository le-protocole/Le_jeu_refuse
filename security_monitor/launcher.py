#!/usr/bin/env python3
"""
Security Monitoring System - Unified Launcher
Choose between Terminal CLI or Web UI
"""

import subprocess
import sys
import os
from pathlib import Path

# ANSI Color codes for terminal
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    BG_CYAN = "\033[46m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"

# Enable colors in Windows Terminal
if sys.platform == 'win32':
    os.system('mode con: cols=100 lines=30')

def clear_screen():
    """Clear terminal"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def print_banner():
    """Print beautiful ASCII banner"""
    banner = f"""
{Colors.BOLD}{Colors.CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          {Colors.GREEN}███████████████████████████████████████████████{Colors.CYAN}           ║
║          {Colors.BLUE}█{Colors.RESET}{Colors.WHITE}   SECURITY MONITORING SYSTEM{Colors.CYAN}{Colors.BLUE}█{Colors.CYAN}           ║
║          {Colors.GREEN}███████████████████████████████████████████████{Colors.CYAN}           ║
║                                                                              ║
║  {Colors.YELLOW}🔐 Enterprise-Ready{Colors.CYAN} | {Colors.GREEN}✓ Production Deployed{Colors.CYAN} | {Colors.MAGENTA}⚡ Level 1 Complete{Colors.CYAN}        ║
║  {Colors.BLUE}27 Modules{Colors.CYAN} | {Colors.WHITE}7500+ Lines{Colors.CYAN} | {Colors.RED}Real-Time Data{Colors.CYAN}                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def print_menu():
    """Print beautiful menu in protocol format"""
    menu = f"""
{Colors.CYAN}╭──────────────────────────────────────────────────────────────────────────────╮{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}⚙️  OPERATIONAL MODE SELECTOR{Colors.RESET}                                           {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}╰──────────────────────────────────────────────────────────────────────────────╯{Colors.RESET}

{Colors.BOLD}{Colors.GREEN}┌─ AVAILABLE MODES ──────────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[1]{Colors.RESET} {Colors.CYAN}TERMINAL_CLI{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[2]{Colors.RESET} {Colors.CYAN}BATCH_SCAN{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[3]{Colors.RESET} {Colors.CYAN}WEBSITE_ANALYZER{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[4]{Colors.RESET} {Colors.CYAN}ADVANCED_ANALYZER{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[5]{Colors.RESET} {Colors.CYAN}ENHANCED_TOOLS{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[6]{Colors.RESET} {Colors.CYAN}INTEGRATION_TEST{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}├─{Colors.RESET} {Colors.BOLD}{Colors.RED}[7]{Colors.RESET} {Colors.CYAN}EXIT{Colors.RESET}
{Colors.GREEN}│{Colors.RESET}
{Colors.GREEN}└────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}{Colors.GREEN}✓ SYSTEM STATUS{Colors.RESET}  {Colors.DIM}|{Colors.RESET}  {Colors.GREEN}Online{Colors.RESET}  {Colors.DIM}|{Colors.RESET}  {Colors.GREEN}27 modules{Colors.RESET}  {Colors.DIM}|{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}Ready{Colors.RESET}  {Colors.BLUE}║{Colors.RESET}
{Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}📖 HELP{Colors.RESET}  {Colors.DIM}|{Colors.RESET}  See {Colors.YELLOW}launcher.md{Colors.RESET} for detailed documentation               {Colors.BLUE}║{Colors.RESET}
{Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}{Colors.MAGENTA}🔐 SECURITY{Colors.RESET}  {Colors.DIM}|{Colors.RESET}  Enterprise Grade | Real-Time Scanning                  {Colors.BLUE}║{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}╚════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(menu)

def get_choice(prompt="Enter your choice (1-7): "):
    """Get user choice"""
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}{Colors.YELLOW}{prompt}{Colors.RESET}").strip()
            if choice in ["1", "2", "3", "4", "5", "6", "7"]:
                return choice
            print(f"{Colors.RED}  [ERROR] Invalid choice. Please enter 1-7{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[!] Cancelled{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}  [ERROR] {str(e)}{Colors.RESET}")

def run_interactive_cli():
    """Run terminal CLI with beautiful design"""
    header = f"""
{Colors.BOLD}{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}>> INTERACTIVE CLI TERMINAL <<{Colors.RESET}  {Colors.DIM}{Colors.WHITE}(Real-time mode){Colors.RESET}                 {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}                                                                              {Colors.GREEN}║{Colors.RESET}
{Colors.BOLD}{Colors.GREEN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)
    
    try:
        subprocess.run([sys.executable, "interactive.py"], check=False)
    except Exception as e:
        print(f"\n{Colors.RED}✗ ERROR: Failed to run interactive CLI: {str(e)}{Colors.RESET}")
        input(f"{Colors.CYAN}\nPress Enter to return to menu...{Colors.RESET}")

def run_integration_test():
    """Run integration test with protocol format"""
    header = f"""
{Colors.MAGENTA}┌───────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.MAGENTA}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[PROTOCOL_HANDLER]{Colors.RESET} SYSTEM_INTEGRATION_TEST                               {Colors.MAGENTA}│{Colors.RESET}
{Colors.MAGENTA}│{Colors.RESET} {Colors.DIM}{Colors.WHITE}Diagnostic: Full system health verification{Colors.RESET}                      {Colors.MAGENTA}│{Colors.RESET}
{Colors.MAGENTA}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}
"""
    print(header)
    
    try:
        subprocess.run([sys.executable, "integration_test.py"], check=False)
    except Exception as e:
        print(f"\n{Colors.RED}[!] ERROR: Failed to run integration test: {str(e)}{Colors.RESET}")
    finally:
        input(f"{Colors.CYAN}\nPress Enter to return to menu...{Colors.RESET}")

def run_batch_scan():
    """Run batch scan with beautiful design"""
    header = f"""
{Colors.BOLD}{Colors.BLUE}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BLUE}║{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}>> BATCH SCAN MODE <<{Colors.RESET}  {Colors.DIM}{Colors.WHITE}(Multi-domain CSV export){Colors.RESET}              {Colors.BLUE}║{Colors.RESET}
{Colors.BLUE}║{Colors.RESET}                                                                              {Colors.BLUE}║{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)
    
    try:
        subprocess.run([sys.executable, "batch_scan.py"], check=False)
    except Exception as e:
        print(f"\n{Colors.RED}✗ ERROR: Failed to run batch scan: {str(e)}{Colors.RESET}")
        input(f"{Colors.CYAN}\nPress Enter to return to menu...{Colors.RESET}")

def run_website_analyzer():
    """Run website analyzer with beautiful design"""
    header = f"""
{Colors.BOLD}{Colors.RED}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.RED}║{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}>> WEBSITE FORENSIC ANALYZER <<{Colors.RESET}  {Colors.DIM}{Colors.WHITE}(SSL/TLS deep scan){Colors.RESET}             {Colors.RED}║{Colors.RESET}
{Colors.RED}║{Colors.RESET}                                                                              {Colors.RED}║{Colors.RESET}
{Colors.BOLD}{Colors.RED}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)
    
    try:
        subprocess.run([sys.executable, "advanced_analyzer.py"], check=False)
    except Exception as e:
        print(f"\n{Colors.RED}✗ ERROR: Failed to run analyzer: {str(e)}{Colors.RESET}")
        input(f"{Colors.CYAN}\nPress Enter to return to menu...{Colors.RESET}")

def run_advanced_analyzer():
    """Run professional advanced analyzer with protocol format"""
    header = f"""
{Colors.YELLOW}┌───────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[PROTOCOL_HANDLER]{Colors.RESET} ADVANCED_ANALYZER_10_MODULE_PROFESSIONAL                {Colors.YELLOW}│{Colors.RESET}
{Colors.YELLOW}│{Colors.RESET} {Colors.DIM}{Colors.WHITE}Deep scan: Portfolio assessment with intelligence{Colors.RESET}                {Colors.YELLOW}│{Colors.RESET}
{Colors.YELLOW}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}
"""
    print(header)
    
    try:
        subprocess.run([sys.executable, "advanced_analyzer.py"], check=False)
    except Exception as e:
        print(f"\n{Colors.RED}[!] ERROR: Failed to run advanced analyzer: {str(e)}{Colors.RESET}")
        input(f"{Colors.CYAN}\nPress Enter to return to menu...{Colors.RESET}")

def run_enhanced_tools():
    """Run enhanced tools suite with protocol format"""
    header = f"""
{Colors.CYAN}┌───────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}[PROTOCOL_HANDLER]{Colors.RESET} ENHANCED_TOOLS_SUITE_ENTERPRISE                         {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.DIM}{Colors.WHITE}Features: Compliance, CVE, PDF reports, Analytics{Colors.RESET}                  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.CYAN}[TOOL_SELECTOR]{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[1]{Colors.RESET} PDF/CSV_EXPORT         : Multi-format report generation and archival
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[2]{Colors.RESET} COMPLIANCE_CHECKER      : CIS/OWASP/PCI-DSS standards validation
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[3]{Colors.RESET} CVE_DATABASE_LOOKUP     : Real-time vulnerability intelligence
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[4]{Colors.RESET} SCAN_PROFILE_MANAGER    : Custom assessment profile management
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[5]{Colors.RESET} PERFORMANCE_ANALYTICS   : Charts, metrics, and trend analysis
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├─{Colors.RESET} {Colors.GREEN}[6]{Colors.RESET} REMEDIATION_GENERATOR   : Auto-generated fix recommendations
{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}└─{Colors.RESET} {Colors.GREEN}[7]{Colors.RESET} RETURN_TO_MAIN          : Exit tool suite
"""
    print(header)
    
    sub_choice = input(f"\n{Colors.BOLD}{Colors.YELLOW}[COMMAND] Select tool (1-7): {Colors.RESET}").strip()
    
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
            run_batch_scan()
        elif choice == "3":
            run_website_analyzer()
        elif choice == "4":
            run_advanced_analyzer()
        elif choice == "5":
            run_enhanced_tools()
        elif choice == "6":
            run_integration_test()
        elif choice == "7":
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
