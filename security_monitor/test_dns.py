#!/usr/bin/env python3
"""Simple DNS resolver test"""

from core.resolver.dns import DNSResolver
import json

def main():
    print("=" * 80)
    print("DNS RESOLVER - INTERACTIVE TEST")
    print("=" * 80)
    
    resolver = DNSResolver()
    print("\n[OK] DNS Resolver initialized with Google + Cloudflare DNS\n")
    
    while True:
        url = input("\nEnter URL (or 'quit' to exit): ").strip()
        
        if url.lower() == 'quit':
            print("\nExiting...")
            break
        
        if not url:
            print("Please enter a valid URL")
            continue
        
        print(f"\nResolving: {url}")
        print("-" * 60)
        
        result = resolver.resolve_domain(url)
        
        # Check if domain is valid (has IPs or CNAME)
        if not result['ips'] and not result['cname_records']:
            print(f"[ERROR] Could not resolve domain: {result['target']}")
            if result.get('errors'):
                for error in result['errors']:
                    print(f"  - {error}")
            continue
        
        # Display results
        print(f"Target: {result['target']}")
        
        if result['ips']:
            print(f"IP Addresses ({len(result['ips'])}): {', '.join(result['ips'])}")
        else:
            print(f"IP Addresses: None (CNAME record found)")
        
        if result['cname_records']:
            print(f"CNAME Records: {', '.join(result['cname_records'])}")
        
        print(f"Behind CDN: {'YES' if result['cdn'] else 'NO'}")
        if result['cdn']:
            print(f"CDN Provider: {result['cdn_provider']}")
            print(f"[NOTE] Scanning edge IP only (CDN detected)")
        
        if result.get('mx_records'):
            print(f"MX Records: {len(result['mx_records'])} record(s)")
        
        if result.get('errors'):
            print(f"\nWarnings:")
            for error in result['errors']:
                print(f"  - {error}")
        
        # Display JSON for debugging
        print(f"\nFull Result (JSON):")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

