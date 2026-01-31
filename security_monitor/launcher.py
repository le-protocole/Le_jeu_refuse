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
    print("  6. Integration Test (Full workflow - REAL DATA)")
    print("  7. Exit")
    print("-" * 80)

def get_choice(prompt="Enter your choice (1-7): "):
    """Get user choice"""
    while True:
        try:
            choice = input(f"\n{prompt}").strip()
            if choice in ["1", "2", "3", "4", "5", "6", "7"]:
                return choice
            print("  [ERROR] Invalid choice. Please enter 1-7")
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
