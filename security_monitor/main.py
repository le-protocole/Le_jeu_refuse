"""
Main Security Monitor Orchestrator
Purpose: Coordinate all modules for end-to-end security assessment
"""

import sys
from typing import Dict, List, Optional
from pathlib import Path

from core.config.settings import DATABASE_PATH
from core.resolver.dns import DNSResolver
from core.scanner.nmap import NmapScanner
from core.analysis.rules import VulnerabilityRules, Finding
from core.risk.scorer import RiskScorer
from core.fixes.recommendations import RecommendationEngine
from core.reports.report import ReportGenerator
from core.audit.audit import AuditLogger
from db.database import DatabaseManager

class SecurityMonitor:
    """Main orchestrator for security assessments"""
    
    def __init__(self):
        self.resolver = DNSResolver()
        self.scanner = NmapScanner()
        self.analyzer = VulnerabilityRules()
        self.risk_scorer = RiskScorer()
        self.recommendations = RecommendationEngine()
        self.report_gen = ReportGenerator()
        self.audit = AuditLogger()
        self.db = DatabaseManager(str(DATABASE_PATH))
        
        self.audit.log("SYSTEM_INITIALIZED", admin="admin")
    
    def assess_target(self, target: str, scan_type: str = "quick", 
                     admin: str = "admin") -> Dict:
        """
        Complete security assessment workflow
        
        Args:
            target: URL or IP to assess
            scan_type: quick / standard / thorough
            admin: Admin user performing assessment
        
        Returns:
            Comprehensive assessment result
        """
        
        print("\n" + "="*80)
        print("🔐 SECURITY MONITOR - ASSESSMENT INITIATED")
        print("="*80)
        
        # Step 1: Resolve target
        print(f"\n[1/7] Resolving target: {target}")
        resolver_result = self.resolver.resolve_domain(target)
        
        if not resolver_result.get("ips"):
            print("  ❌ Could not resolve target")
            self.audit.log("ASSESSMENT_FAILED", admin, target, 
                          details={"reason": "Resolution failed"})
            return {"error": "Resolution failed"}
        
        ips = resolver_result.get("ips")
        print(f"  ✓ Resolved to: {ips}")
        if resolver_result.get("cdn"):
            print(f"  ⚠️  Behind CDN/Proxy: {resolver_result.get('cdn_provider')}")
        
        # Step 2: Port scanning
        print(f"\n[2/7] Scanning ports ({scan_type} scan)...")
        self.audit.log("SCAN_INITIATED", admin, target, 
                      details={"scan_type": scan_type})
        
        scan_results = None
        for ip in ips:
            if self.scanner.validate_ip(ip) and not self.scanner.is_private_ip(ip):
                if scan_type == "quick":
                    scan_results = self.scanner.quick_scan(ip)
                elif scan_type == "standard":
                    scan_results = self.scanner.standard_scan(ip)
                elif scan_type == "thorough":
                    scan_results = self.scanner.thorough_scan(ip)
                break
        
        if not scan_results:
            print("  ⚠️  Could not scan target (may be private IP or unreachable)")
            scan_results = {
                "target": target,
                "scan_type": scan_type,
                "open_ports": [],
                "filtered_ports": [],
                "closed_ports": [],
                "error": "Could not perform scan"
            }
        else:
            print(f"  ✓ Found {len(scan_results.get('open_ports', []))} open ports")
        
        # Step 3: Vulnerability analysis
        print(f"\n[3/7] Analyzing for vulnerabilities...")
        findings_objects = self.analyzer.analyze(scan_results)
        
        # Convert Finding objects to dicts
        findings = []
        for finding in findings_objects:
            findings.append({
                "severity": finding.severity.value,
                "title": finding.title,
                "description": finding.description,
                "affected_asset": finding.affected_asset,
                "evidence": finding.evidence,
                "mitigation": finding.mitigation,
                "cve_reference": finding.cve_reference
            })
        
        print(f"  ✓ Identified {len(findings)} potential issues")
        
        # Step 4: Risk scoring
        print(f"\n[4/7] Calculating risk score...")
        risk_analysis = self.risk_scorer.calculate_score(
            findings,
            scan_results.get("open_ports", [])
        )
        print(f"  ✓ Risk Score: {risk_analysis['score']}/100 ({risk_analysis['level']})")
        
        # Step 5: Generate recommendations
        print(f"\n[5/7] Generating recommendations...")
        prioritized_findings = self.risk_scorer.prioritize_findings(findings)
        recommendations = []
        for finding in prioritized_findings[:5]:  # Top 5
            recs = self.recommendations.get_recommendations_for_finding(finding)
            recommendations.extend(recs)
        print(f"  ✓ Generated {len(recommendations)} recommendations")
        
        # Step 6: Generate reports
        print(f"\n[6/7] Generating reports...")
        report_paths = self.report_gen.generate_full_report(
            scan_results,
            findings,
            risk_analysis,
            target
        )
        print(f"  ✓ Reports generated:")
        for format, path in report_paths.items():
            print(f"    - {format.upper()}: {path}")
        
        # Step 7: Audit logging
        print(f"\n[7/7] Logging assessment...")
        self.audit.log("ASSESSMENT_COMPLETED", admin, target,
                      details={
                          "findings": len(findings),
                          "risk_level": risk_analysis['level'],
                          "risk_score": risk_analysis['score']
                      })
        
        # Compile results
        assessment_result = {
            "status": "success",
            "target": target,
            "resolver_data": resolver_result,
            "scan_data": scan_results,
            "findings": findings,
            "risk_analysis": risk_analysis,
            "recommendations": [
                {
                    "title": r.title,
                    "description": r.description,
                    "difficulty": r.difficulty,
                    "impact": r.impact,
                    "steps": r.steps
                } for r in recommendations[:5]
            ],
            "report_paths": report_paths
        }
        
        print("\n" + "="*80)
        print(f"✓ ASSESSMENT COMPLETE - Risk Level: {risk_analysis['level']}")
        print("="*80 + "\n")
        
        return assessment_result
    
    def print_summary(self, result: Dict):
        """Print human-readable summary"""
        if result.get("error"):
            print(f"❌ Assessment failed: {result['error']}")
            return
        
        print("\n" + "="*80)
        print("ASSESSMENT SUMMARY")
        print("="*80)
        
        print(f"\nTarget: {result['target']}")
        print(f"Risk Score: {result['risk_analysis']['score']}/100")
        print(f"Risk Level: {result['risk_analysis']['level']}")
        print(f"Total Findings: {len(result['findings'])}")
        
        breakdown = result['risk_analysis']['breakdown']
        print(f"\nFinding Breakdown:")
        print(f"  CRITICAL: {breakdown['critical']}")
        print(f"  HIGH: {breakdown['high']}")
        print(f"  MEDIUM: {breakdown['medium']}")
        print(f"  LOW: {breakdown['low']}")
        
        open_ports = result['scan_data'].get('open_ports', [])
        print(f"\nOpen Ports: {len(open_ports)}")
        if open_ports:
            print("  Top ports:")
            for port in open_ports[:5]:
                print(f"    Port {port['port']}: {port.get('service', 'unknown')}")
        
        print(f"\nReports Generated:")
        for format, path in result.get('report_paths', {}).items():
            print(f"  📄 {format.upper()}: {path}")
        
        print("\nTop Recommendations:")
        for i, rec in enumerate(result.get('recommendations', [])[:3], 1):
            print(f"\n  {i}. {rec['title']}")
            print(f"     Difficulty: {rec['difficulty']} | Impact: {rec['impact']}")
        
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    monitor = SecurityMonitor()
    
    # Example assessment
    if len(sys.argv) > 1:
        target = sys.argv[1]
        scan_type = sys.argv[2] if len(sys.argv) > 2 else "quick"
        
        result = monitor.assess_target(target, scan_type)
        monitor.print_summary(result)
    else:
        print("Usage: python main.py <target> [quick|standard|thorough]")
        print("Example: python main.py example.com quick")
