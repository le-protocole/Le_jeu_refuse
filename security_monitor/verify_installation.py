"""
Installation and Dependency Management
"""

import subprocess
import sys
from pathlib import Path

def check_nmap():
    """Verify Nmap is installed"""
    try:
        result = subprocess.run(
            ["nmap", "-V"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True
    except:
        return False

def check_python():
    """Verify Python version"""
    version = sys.version_info
    return version.major >= 3 and version.minor >= 9

def install_requirements():
    """Install Python dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        return True
    except:
        return False

def verify_installation():
    """Verify all dependencies are installed"""
    missing = []
    
    # Check Nmap
    if not check_nmap():
        missing.append("Nmap - Download from https://nmap.org/download.html")
    
    # Check Python version
    if not check_python():
        missing.append("Python 3.9+ required")
    
    # Check Python packages
    try:
        import dnspython
        import requests
        import typer
        import rich
    except ImportError as e:
        missing.append(f"Python package missing: {str(e)}")
    
    return missing

if __name__ == "__main__":
    print("Checking installation...")
    
    missing = verify_installation()
    
    if missing:
        print("\n❌ Missing dependencies:")
        for item in missing:
            print(f"  - {item}")
        
        print("\nTo fix:")
        print("  1. Install Nmap: https://nmap.org/download.html")
        print("  2. pip install -r requirements.txt")
    else:
        print("✓ All dependencies installed correctly!")
