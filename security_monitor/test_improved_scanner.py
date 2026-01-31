#!/usr/bin/env python3
"""Test improved scanner with fallback"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.scanner.nmap import NmapScanner

print("\n" + "="*80)
print("IMPROVED NMAP SCANNER TEST - WITH PYTHON FALLBACK")
print("="*80 + "\n")

scanner = NmapScanner()

print(f"Nmap Available: {scanner.nmap_available}")
print(f"Method: {'Nmap' if scanner.nmap_available else 'Python Socket (Fallback)'}\n")

# Test quick scan
print("[*] Testing Quick Scan: google.com")
print("-" * 80)
result = scanner.quick_scan("google.com")

print(f"Target: {result['target']}")
print(f"Method: {result.get('method', 'unknown')}")
print(f"Scan Type: {result['scan_type']}")
if result.get('ip_address'):
    print(f"IP Address: {result['ip_address']}")

if result.get('error'):
    print(f"Error: {result['error']}")
else:
    open_ports = result.get('open_ports', [])
    if open_ports:
        print(f"\nOpen Ports ({len(open_ports)}):")
        for p in open_ports[:10]:
            port_num = p['port'] if isinstance(p, dict) else p
            service = p.get('service', 'unknown') if isinstance(p, dict) else 'unknown'
            print(f"  {port_num}/tcp  ({service})")
    else:
        print("No open ports detected")
    
    closed = len(result.get('closed_ports', []))
    filtered = len(result.get('filtered_ports', []))
    print(f"\nSummary: Open: {len(open_ports)} | Closed: {closed} | Filtered: {filtered}")

# Test standard scan
print("\n" + "="*80)
print("[*] Testing Standard Scan: localhost")
print("-" * 80)
result = scanner.standard_scan("localhost")

print(f"Target: {result['target']}")
print(f"Method: {result.get('method', 'unknown')}")
if result.get('ip_address'):
    print(f"IP Address: {result['ip_address']}")

if result.get('error'):
    print(f"Error: {result['error']}")
else:
    open_ports = result.get('open_ports', [])
    if open_ports:
        print(f"\nOpen Ports ({len(open_ports)}):")
        for p in open_ports[:5]:
            port_num = p['port'] if isinstance(p, dict) else p
            service = p.get('service', 'unknown') if isinstance(p, dict) else 'unknown'
            print(f"  {port_num}/tcp  ({service})")
    else:
        print("No open ports detected")
    
    closed = len(result.get('closed_ports', []))
    filtered = len(result.get('filtered_ports', []))
    print(f"\nSummary: Open: {len(open_ports)} | Closed: {closed} | Filtered: {filtered}")

print("\n" + "="*80)
print("✓ SCANNER TEST COMPLETE")
print("="*80 + "\n")
