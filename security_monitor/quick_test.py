#!/usr/bin/env python3
"""Quick DNS resolver test"""

from core.resolver.dns import DNSResolver

resolver = DNSResolver()

# Test cases
test_urls = [
    "https://www.google.com/",
    "geekprank.com",
    "cloudflare.com",
    "example.com"
]

print("=" * 80)
print("DNS RESOLVER - QUICK TEST")
print("=" * 80)

for url in test_urls:
    print(f"\nTesting: {url}")
    result = resolver.resolve_domain(url)
    
    print(f"  Sanitized: {result['target']}")
    print(f"  IPs: {result['ips'] if result['ips'] else 'None'}")
    print(f"  CNAME: {result['cname_records'] if result['cname_records'] else 'None'}")
    print(f"  CDN: {result['cdn']} ({result['cdn_provider']})")
    
    if result.get('errors'):
        print(f"  Errors: {result['errors']}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
