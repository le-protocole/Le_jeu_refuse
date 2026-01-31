#!/usr/bin/env python3
"""
Security Monitor - Quick Start Script
Runs initial setup and first scan
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("🔐 SECURITY MONITOR - QUICK START")
    print("="*80)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    
    # Try to import main
    try:
        from main import SecurityMonitor
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Try: pip install -r requirements.txt")
        sys.exit(1)
    
    # Initialize
    monitor = SecurityMonitor()
    
    print("\n📋 LEGAL DISCLAIMER:")
    print("   This tool is for AUTHORIZED ADMINISTRATORS ONLY")
    print("   Unauthorized security testing is ILLEGAL\n")
    
    # Get target
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Enter target (URL or IP): ").strip()
    
    if not target:
        print("❌ No target provided")
        sys.exit(1)
    
    # Get scan type
    scan_type = "quick"
    if len(sys.argv) > 2:
        scan_type = sys.argv[2]
    else:
        print("\nSelect scan type:")
        print("  1. quick    (2-5 min, common ports)")
        print("  2. standard (5-15 min, recommended)")
        print("  3. thorough (30+ min, all ports)")
        choice = input("Choose [1-3] (default: 2): ").strip()
        if choice == "1":
            scan_type = "quick"
        elif choice == "3":
            scan_type = "thorough"
        else:
            scan_type = "standard"
    
    # Confirm
    print(f"\n✓ Target: {target}")
    print(f"✓ Scan Type: {scan_type}")
    
    confirm = input("\nProceed with scan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        sys.exit(0)
    
    # Run assessment
    result = monitor.assess_target(target, scan_type)
    monitor.print_summary(result)
    
    print("\n📄 Reports saved to: reports/")
    print("📋 Audit log saved to: logs/")
    print("💾 Data saved to: db/security_monitor.db")
    print("\n✓ Assessment complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
