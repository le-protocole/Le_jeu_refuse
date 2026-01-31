"""
Security Monitor - Legal Disclaimer & Terms
"""

LEGAL_DISCLAIMER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ⚠️  IMPORTANT LEGAL NOTICE ⚠️                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

This Security Monitor tool is PROVIDED EXCLUSIVELY for authorized system 
administrators and security professionals to assess the security posture of 
their OWN infrastructure or systems they have EXPLICIT WRITTEN PERMISSION to test.

═══════════════════════════════════════════════════════════════════════════════

🛑 UNAUTHORIZED USE IS ILLEGAL

Unauthorized access to computer systems is a FEDERAL CRIME under:
  • Computer Fraud and Abuse Act (CFAA) - USA
  • Computer Misuse Act 1990 - UK
  • Similar laws in most countries

Unauthorized security testing can result in:
  ✗ Criminal prosecution
  ✗ Civil liability
  ✗ Imprisonment (up to 10+ years)
  ✗ Substantial fines (up to $250,000+)
  ✗ Restitution for damages

═══════════════════════════════════════════════════════════════════════════════

✅ LEGITIMATE USES

This tool is designed for:
  ✓ Internal security audits (your own systems)
  ✓ Pre-deployment hardening validation
  ✓ Authorized penetration testing (with written scope)
  ✓ Blue team security operations
  ✓ DevOps security hardening
  ✓ Bug bounty programs (within disclosed scope)
  ✓ Compliance assessments (documented permissions)

═══════════════════════════════════════════════════════════════════════════════

📋 REQUIRED BEFORE USE

You MUST have:
  1. ✓ Written authorization to test the target system
  2. ✓ Clear scope of what may be tested
  3. ✓ Time window for testing
  4. ✓ Emergency contact information
  5. ✓ Organization approval

ALWAYS CONFIRM YOU OWN OR HAVE PERMISSION BEFORE PROCEEDING

═══════════════════════════════════════════════════════════════════════════════

⚠️  WHAT THIS TOOL DOES

  • Performs passive scanning (no exploitation)
  • Analyzes open ports and services
  • Evaluates configuration against security rules
  • Identifies potential vulnerabilities
  • Provides hardening recommendations
  • Logs all activities for audit trail

═══════════════════════════════════════════════════════════════════════════════

🚫 WHAT THIS TOOL DOES NOT DO

  ✗ Does NOT exploit vulnerabilities
  ✗ Does NOT modify system data
  ✗ Does NOT attempt authentication bypass
  ✗ Does NOT deliver malware/payloads
  ✗ Does NOT perform illegal network activities

═══════════════════════════════════════════════════════════════════════════════

📊 AUDIT TRAIL

All activities are logged including:
  • When scans were performed
  • Who initiated them
  • What targets were scanned
  • What findings were identified
  • Reports generated

These logs can be used as evidence of authorized testing.

═══════════════════════════════════════════════════════════════════════════════

❓ LIABILITY

The creators of this tool:
  ✗ Assume NO liability for unauthorized use
  ✗ Assume NO liability for damages caused by misuse
  ✗ Assume NO liability for illegal activity
  ✓ Provide this tool "AS-IS" for legitimate purposes only

═══════════════════════════════════════════════════════════════════════════════

By using this tool, you:
  1. Confirm you have authorization to test the target
  2. Acknowledge you understand the legal risks
  3. Accept full responsibility for your actions
  4. Agree to use this tool only for legitimate purposes
  5. Release the creators from any liability

═══════════════════════════════════════════════════════════════════════════════

🤔 QUESTIONS?

  • Do you own this system? → YES, use the tool
  • Do you have written permission? → YES, use the tool  
  • Is this a production system? → Get approval first
  • Did someone ask you to test it? → Get approval in writing
  • Are you unsure? → DO NOT USE - SEEK LEGAL ADVICE

═══════════════════════════════════════════════════════════════════════════════

If you proceed, you are accepting ALL legal responsibility for your actions.

"""

# Severity-level messaging
SEVERITY_MESSAGES = {
    "CRITICAL": {
        "color": "🔴 CRITICAL",
        "message": "System requires IMMEDIATE remediation - DO NOT use in production",
        "action": "Fix within 24 hours"
    },
    "HIGH": {
        "color": "🟠 HIGH",
        "message": "Serious security issues found - address urgently",
        "action": "Fix within 1 week"
    },
    "MEDIUM": {
        "color": "🟡 MEDIUM",
        "message": "Notable security concerns detected",
        "action": "Plan fixes for next maintenance window"
    },
    "LOW": {
        "color": "🟢 LOW",
        "message": "Minor security recommendations",
        "action": "Address during routine updates"
    }
}

# Best practices
SECURITY_BEST_PRACTICES = [
    "Always use HTTPS for web services",
    "Keep all software updated to latest versions",
    "Use strong, unique passwords (or SSH keys)",
    "Restrict ports and services to minimum necessary",
    "Enable authentication for all services",
    "Use firewalls to control network access",
    "Monitor logs for suspicious activity",
    "Regular backups with offline copies",
    "Implement principle of least privilege",
    "Document all infrastructure changes"
]
