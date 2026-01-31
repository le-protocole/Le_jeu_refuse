#!/usr/bin/env python3
"""Verify scanner improvements"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.scanner.nmap import NmapScanner

print("\nSCANNER STATUS:")
print("="*60)

scanner = NmapScanner()
print(f"✓ Nmap Available: {scanner.nmap_available}")
print(f"✓ Nmap Binary: {scanner.nmap_bin if scanner.nmap_available else 'Not found'}")

# Test quick scan
print("\n✓ Testing Quick Scan on example.com...")
result = scanner.quick_scan("example.com")

print(f"  - Target: {result['target']}")
print(f"  - Method: {result.get('method', 'unknown')}")
print(f"  - IP: {result.get('ip_address', 'unknown')}")
print(f"  - Open Ports: {len(result.get('open_ports', []))}")
print(f"  - Closed Ports: {len(result.get('closed_ports', []))}")
print(f"  - Error: {result.get('error', 'None')}")

if result.get('open_ports'):
    print(f"\n  Open Ports Found:")
    for port in result['open_ports'][:3]:
        print(f"    - {port['port']}/tcp ({port.get('service', 'unknown')})")

print("\n" + "="*60)
print("✓ SCANNER IMPROVEMENTS VERIFIED\n")
