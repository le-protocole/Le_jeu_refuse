#!/usr/bin/env python3
"""
QUICK REFERENCE - What You Need to Know
"""

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         SECURITY MONITOR - QUICK REFERENCE                ║
╚════════════════════════════════════════════════════════════════════════════╝

YOUR QUESTION:
──────────────────────────────────────────────────────────────────────────────
"Code real data ашигладаг уу? Demo data үү?"

ANSWER:
──────────────────────────────────────────────────────────────────────────────
✅ YA, REAL DATA ASIGLADAG!

But you need the RIGHT OPTION:

    ❌ Option 4 (Integration Test) = Demo data fallback (for testing)
    ✅ Option 1 (Terminal CLI) = Real data (single target)
    ✅ Option 2 (Web UI) = Real data (single/multiple targets)
    ✅ Option 3 (Batch Scan) = Real data (10+ websites) ← NEW!


WHICH OPTION TO USE:
──────────────────────────────────────────────────────────────────────────────

Want to see 10 websites with REAL data?
    → Use: python launcher.py → 3 (Batch Scan Mode)

Want to scan 1 website with REAL data (Terminal)?
    → Use: python launcher.py → 1 (Terminal CLI)

Want to scan 1 website with REAL data (Web)?
    → Use: python launcher.py → 2 (Web UI)

Want to verify system works (demo data ok)?
    → Use: python launcher.py → 4 (Integration Test)


LAUNCHER MENU:
──────────────────────────────────────────────────────────────────────────────

python launcher.py

    1. Terminal CLI ..................... Single target, real data ✅
    2. Web UI ........................... Single target, real data ✅
    3. Batch Scan Mode ................. 10+ websites, real data ✅✅✅
    4. Integration Test ................ Demo data (for testing)
    5. Quick DNS Test .................. DNS diagnostics
    6. Exit


BATCH SCAN MODE (THE NEW FEATURE):
──────────────────────────────────────────────────────────────────────────────

What: Scan 10+ websites with REAL data
How: python launcher.py → 3

Features:
    • Real DNS resolution
    • Real port scanning (Nmap)
    • Real vulnerability analysis (20+ rules)
    • Real risk scoring (0-100)
    • Real reports (JSON)
    • Summary table with all 10 websites
    • Database persistence

Example Output:
    ┌────────────────┬──────────────┬───────┬───────┬─────────┬────────┐
    │ Target         │ IP           │ Ports │ Vulns │ Score   │ Status │
    ├────────────────┼──────────────┼───────┼───────┼─────────┼────────┤
    │ google.com     │ 142.250.x.x  │ 2     │ 1     │ 3/100   │ ✓      │
    │ example.com    │ 93.184.x.x   │ 1     │ 0     │ 2/100   │ ✓      │
    │ github.com     │ 140.82.x.x   │ 2     │ 1     │ 15/100  │ ✓      │
    │ ... (10 total) │ ...          │ ...   │ ...   │ ...     │ ...    │
    └────────────────┴──────────────┴───────┴───────┴─────────┴────────┘


REAL DATA VERIFICATION:
──────────────────────────────────────────────────────────────────────────────

How to verify it's REAL data:

1. Run: python launcher.py → 3 (Batch Scan)
2. See IP addresses (e.g., 142.250.197.110)
3. Check reports/ folder → batch_scan_*.json
4. Open JSON file → see REAL data
5. Run independently: nmap google.com → compare results


KEY DIFFERENCES:
──────────────────────────────────────────────────────────────────────────────

Integration Test (Option 4):
    • May use demo data if Nmap unavailable
    • Purpose: Verify all modules work
    • 3 fixed targets
    • Summary: Text output

Batch Scan (Option 3):
    • ALWAYS real data
    • Purpose: Scan multiple sites
    • 10+ targets (your choice)
    • Summary: Table + JSON report


SPEED COMPARISON:
──────────────────────────────────────────────────────────────────────────────

Terminal CLI (1 website):
    • Quick scan: 2 minutes
    • Standard: 10 minutes
    • Deep: 30 minutes

Batch Scan (10 websites):
    • All 10 with Quick: ~20 minutes
    • All 10 with Standard: ~100 minutes
    • All 10 with Deep: ~300 minutes


WHAT GETS SAVED:
──────────────────────────────────────────────────────────────────────────────

From Batch Scan:
    ✓ reports/batch_scan_*.json    (all results)
    ✓ db/security_monitor.db       (database)
    ✓ logs/                        (audit trail)


DOCUMENTATION:
──────────────────────────────────────────────────────────────────────────────

For more details:
    • README.md ..................... System overview
    • BATCH_SCAN_GUIDE.md ........... Batch scan details
    • REAL_DATA_EXPLAINED.md ........ Real vs demo data
    • COMPLETE_GUIDE.md ............. Full manual


ONE-LINER TO GET STARTED:
──────────────────────────────────────────────────────────────────────────────

python launcher.py → 3 → Press Enter twice → See real data! 🎯


REMEMBER:
──────────────────────────────────────────────────────────────────────────────

    ✅ Terminal CLI (Option 1) = Real data
    ✅ Web UI (Option 2) = Real data
    ✅ Batch Scan (Option 3) = Real data (10+ sites)
    ⚠️  Integration Test (Option 4) = Demo data (testing only)

╚════════════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
