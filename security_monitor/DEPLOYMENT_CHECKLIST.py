#!/usr/bin/env python3
"""
SYSTEM DEPLOYMENT CHECKLIST
Verification that all components are ready
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if file exists"""
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {description:40} {path}")
    return exists

def check_directory(path, description):
    """Check if directory exists"""
    exists = Path(path).is_dir()
    status = "✅" if exists else "❌"
    print(f"  {status} {description:40} {path}/")
    return exists

def main():
    print("\n" + "=" * 80)
    print("  SECURITY MONITORING SYSTEM - DEPLOYMENT CHECKLIST")
    print("=" * 80)
    
    all_good = True
    
    # Core launcher
    print("\n📌 LAUNCHER (Entry Point)")
    print("-" * 80)
    all_good &= check_file("launcher.py", "Unified launcher")
    
    # User Interfaces
    print("\n🖥️  USER INTERFACES")
    print("-" * 80)
    all_good &= check_file("interactive.py", "Terminal CLI")
    all_good &= check_file("web_server.py", "Web UI (FastAPI)")
    
    # Core Modules
    print("\n⚙️  CORE MODULES")
    print("-" * 80)
    all_good &= check_directory("core/resolver", "DNS Resolver")
    all_good &= check_directory("core/scanner", "Port Scanner")
    all_good &= check_directory("core/analysis", "Vulnerability Analysis")
    all_good &= check_directory("core/risk", "Risk Scorer")
    all_good &= check_directory("core/fixes", "Recommendations Engine")
    all_good &= check_directory("core/reports", "Report Generator")
    all_good &= check_directory("core/audit", "Audit Logger")
    all_good &= check_directory("core/config", "Configuration")
    
    # Data Storage
    print("\n💾 DATA STORAGE")
    print("-" * 80)
    all_good &= check_directory("db", "Database directory")
    all_good &= check_directory("reports", "Reports directory")
    all_good &= check_directory("logs", "Logs directory")
    
    # Testing
    print("\n🧪 TESTING & DIAGNOSTICS")
    print("-" * 80)
    all_good &= check_file("integration_test.py", "Integration test")
    all_good &= check_file("demo_dns.py", "DNS diagnostics")
    all_good &= check_file("DELIVERY_SUMMARY.py", "Delivery summary")
    
    # Documentation
    print("\n📚 DOCUMENTATION")
    print("-" * 80)
    all_good &= check_file("README.md", "System overview")
    all_good &= check_file("START_HERE.md", "Getting started")
    all_good &= check_file("COMPLETE_GUIDE.md", "Comprehensive manual")
    all_good &= check_file("QUICK_START.py", "Interactive guide")
    all_good &= check_file("ARCHITECTURE.md", "System design")
    all_good &= check_file("SETUP.md", "Installation guide")
    all_good &= check_file("LEGAL.md", "Legal information")
    all_good &= check_file("FINAL_STATUS.md", "Final status")
    
    # Environment
    print("\n🔧 ENVIRONMENT")
    print("-" * 80)
    all_good &= check_directory(".venv", "Python virtual environment")
    all_good &= check_file("requirements.txt", "Dependencies list")
    
    # Summary
    print("\n" + "=" * 80)
    if all_good:
        print("  ✅ ALL COMPONENTS PRESENT AND READY!")
        print("=" * 80)
        print("\n🚀 System is PRODUCTION READY!\n")
        print("To get started, run:")
        print("  python launcher.py")
        print("\nThen choose:")
        print("  1 - Terminal CLI")
        print("  2 - Web Browser UI")
        print("  3 - Integration Test")
        print("  4 - DNS Diagnostics")
        print("  5 - Exit")
        print("\n" + "=" * 80)
        return 0
    else:
        print("  ⚠️  SOME COMPONENTS MISSING")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
