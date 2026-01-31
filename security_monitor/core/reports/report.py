"""
Report Generation Module
Purpose: Create comprehensive reports in multiple formats (JSON, PDF, HTML, TXT)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class ReportGenerator:
    """Generate security assessment reports"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_full_report(self, 
                            scan_data: Dict,
                            findings: List[Dict],
                            risk_analysis: Dict,
                            target: str) -> Dict[str, str]:
        """
        Generate report in all formats
        Returns dict with file paths
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"{target.replace('.', '_')}_{timestamp}"
        
        report_paths = {}
        
        # JSON Report (most comprehensive)
        report_paths["json"] = self._generate_json_report(
            scan_data, findings, risk_analysis, target, report_name
        )
        
        # Text Report (human-readable)
        report_paths["txt"] = self._generate_text_report(
            scan_data, findings, risk_analysis, target, report_name
        )
        
        # HTML Report (visual)
        report_paths["html"] = self._generate_html_report(
            scan_data, findings, risk_analysis, target, report_name
        )
        
        return report_paths
    
    def _generate_json_report(self, scan_data: Dict, findings: List[Dict], 
                             risk_analysis: Dict, target: str, 
                             report_name: str) -> str:
        """Generate JSON format report"""
        
        report = {
            "metadata": {
                "target": target,
                "timestamp": datetime.now().isoformat(),
                "report_version": "1.0",
                "disclaimer": "LEGITIMATE SECURITY ASSESSMENT ONLY - Admin use only"
            },
            "executive_summary": {
                "risk_score": risk_analysis.get("score"),
                "risk_level": risk_analysis.get("level"),
                "total_findings": len(findings),
                "critical_findings": risk_analysis.get("breakdown", {}).get("critical", 0),
                "high_findings": risk_analysis.get("breakdown", {}).get("high", 0),
                "medium_findings": risk_analysis.get("breakdown", {}).get("medium", 0),
                "low_findings": risk_analysis.get("breakdown", {}).get("low", 0),
                "open_ports": len(scan_data.get("open_ports", [])),
                "recommendation": self._get_risk_recommendation(risk_analysis.get("level"))
            },
            "scan_details": {
                "target": scan_data.get("target"),
                "scan_type": scan_data.get("scan_type"),
                "open_ports": scan_data.get("open_ports", []),
                "filtered_ports": len(scan_data.get("filtered_ports", [])),
                "closed_ports": len(scan_data.get("closed_ports", [])),
            },
            "findings": findings,
            "risk_analysis": risk_analysis,
            "timeline": {
                "scan_start": scan_data.get("timestamp"),
                "report_generated": datetime.now().isoformat()
            }
        }
        
        filepath = self.output_dir / f"{report_name}.json"
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(filepath)
    
    def _generate_text_report(self, scan_data: Dict, findings: List[Dict],
                             risk_analysis: Dict, target: str,
                             report_name: str) -> str:
        """Generate human-readable text report"""
        
        lines = []
        lines.append("=" * 80)
        lines.append("SECURITY ASSESSMENT REPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Target: {target}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Scan Type: {scan_data.get('scan_type', 'unknown')}")
        lines.append("")
        
        # Legal disclaimer
        lines.append("IMPORTANT DISCLAIMER:")
        lines.append("-" * 80)
        lines.append("This assessment is for AUTHORIZED ADMINISTRATORS ONLY")
        lines.append("Unauthorized security testing is ILLEGAL")
        lines.append("Use this tool only on systems you own or have explicit permission to test")
        lines.append("")
        
        # Risk Summary
        lines.append("RISK SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Risk Score: {risk_analysis.get('score')}/100")
        lines.append(f"Risk Level: {risk_analysis.get('level')}")
        lines.append(f"Total Findings: {len(findings)}")
        lines.append("")
        
        breakdown = risk_analysis.get("breakdown", {})
        lines.append("Finding Breakdown:")
        lines.append(f"  CRITICAL: {breakdown.get('critical', 0)}")
        lines.append(f"  HIGH:     {breakdown.get('high', 0)}")
        lines.append(f"  MEDIUM:   {breakdown.get('medium', 0)}")
        lines.append(f"  LOW:      {breakdown.get('low', 0)}")
        lines.append("")
        
        # Open Ports
        lines.append("OPEN PORTS")
        lines.append("-" * 80)
        open_ports = scan_data.get("open_ports", [])
        if open_ports:
            for port_info in open_ports:
                port = port_info.get("port")
                service = port_info.get("service", "unknown")
                version = port_info.get("version", "")
                lines.append(f"  Port {port:5d} | {service:15s} | {version}")
        else:
            lines.append("  No open ports detected (positive indicator)")
        lines.append("")
        
        # Detailed Findings
        lines.append("DETAILED FINDINGS")
        lines.append("-" * 80)
        if findings:
            for i, finding in enumerate(findings, 1):
                lines.append(f"\n{i}. [{finding.get('severity')}] {finding.get('title')}")
                lines.append(f"   Description: {finding.get('description')}")
                lines.append(f"   Asset: {finding.get('affected_asset')}")
                lines.append(f"   Evidence: {finding.get('evidence')}")
                if finding.get("mitigation"):
                    lines.append("   Mitigation:")
                    for mit in finding.get("mitigation", []):
                        lines.append(f"     - {mit}")
        else:
            lines.append("  No findings (excellent)")
        lines.append("")
        
        # Recommendations
        lines.append("PRIORITIZED RECOMMENDATIONS")
        lines.append("-" * 80)
        lines.append("1. Address all CRITICAL findings immediately")
        lines.append("2. Schedule fixes for HIGH findings within 1 week")
        lines.append("3. Plan MEDIUM findings for next maintenance window")
        lines.append("4. Address LOW findings during routine updates")
        lines.append("")
        
        # Footer
        lines.append("=" * 80)
        lines.append("End of Report")
        lines.append("=" * 80)
        
        content = "\n".join(lines)
        
        filepath = self.output_dir / f"{report_name}.txt"
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def _generate_html_report(self, scan_data: Dict, findings: List[Dict],
                             risk_analysis: Dict, target: str,
                             report_name: str) -> str:
        """Generate HTML format report"""
        
        risk_level = risk_analysis.get("level", "UNKNOWN")
        risk_color = {
            "CRITICAL": "#d32f2f",
            "HIGH": "#f57c00",
            "MEDIUM": "#fbc02d",
            "LOW": "#388e3c"
        }.get(risk_level, "#757575")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Security Assessment Report - {target}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            border-bottom: 3px solid {risk_color};
            padding-bottom: 10px;
            color: #1a1a1a;
        }}
        h2 {{
            color: #424242;
            margin-top: 30px;
            border-left: 4px solid {risk_color};
            padding-left: 10px;
        }}
        .disclaimer {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .risk-badge {{
            display: inline-block;
            background-color: {risk_color};
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            font-size: 18px;
            font-weight: bold;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .summary-card {{
            background-color: #fafafa;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            text-align: center;
        }}
        .summary-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: {risk_color};
        }}
        .summary-card .label {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
        .finding {{
            border-left: 4px solid {risk_color};
            padding: 15px;
            margin: 15px 0;
            background-color: #fafafa;
            border-radius: 4px;
        }}
        .finding.CRITICAL {{
            border-left-color: #d32f2f;
            background-color: #ffebee;
        }}
        .finding.HIGH {{
            border-left-color: #f57c00;
            background-color: #fff3e0;
        }}
        .finding.MEDIUM {{
            border-left-color: #fbc02d;
            background-color: #fffde7;
        }}
        .finding.LOW {{
            border-left-color: #388e3c;
            background-color: #f1f8e9;
        }}
        .finding-title {{
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        .finding-severity {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-weight: bold;
            font-size: 12px;
            color: white;
            margin-bottom: 10px;
        }}
        .severity-CRITICAL {{ background-color: #d32f2f; }}
        .severity-HIGH {{ background-color: #f57c00; }}
        .severity-MEDIUM {{ background-color: #fbc02d; color: #333; }}
        .severity-LOW {{ background-color: #388e3c; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Security Assessment Report</h1>
        
        <div class="disclaimer">
            <strong>⚠️ IMPORTANT DISCLAIMER:</strong><br>
            This assessment is for AUTHORIZED ADMINISTRATORS ONLY.<br>
            Unauthorized security testing is ILLEGAL in most jurisdictions.<br>
            Use this tool only on systems you own or have explicit written permission to test.
        </div>
        
        <h2>Executive Summary</h2>
        <p><strong>Target:</strong> {target}</p>
        <p><strong>Assessment Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Scan Type:</strong> {scan_data.get('scan_type', 'unknown')}</p>
        
        <div style="margin: 20px 0;">
            <span class="risk-badge">{risk_level}</span>
            <span style="margin-left: 20px; font-size: 24px;">
                Risk Score: <strong>{risk_analysis.get('score')}/100</strong>
            </span>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <div class="number">{len(findings)}</div>
                <div class="label">Total Findings</div>
            </div>
            <div class="summary-card">
                <div class="number">{risk_analysis.get('breakdown', {}).get('critical', 0)}</div>
                <div class="label">Critical Issues</div>
            </div>
            <div class="summary-card">
                <div class="number">{len(scan_data.get('open_ports', []))}</div>
                <div class="label">Open Ports</div>
            </div>
            <div class="summary-card">
                <div class="number">{risk_analysis.get('breakdown', {}).get('high', 0)}</div>
                <div class="label">High Priority</div>
            </div>
        </div>
        
        <h2>Open Ports & Services</h2>
        <table>
            <tr>
                <th>Port</th>
                <th>Protocol</th>
                <th>Service</th>
                <th>Version</th>
            </tr>
"""
        
        for port_info in scan_data.get("open_ports", []):
            html += f"""
            <tr>
                <td>{port_info.get('port')}</td>
                <td>{port_info.get('protocol', 'tcp')}</td>
                <td>{port_info.get('service', 'unknown')}</td>
                <td>{port_info.get('version', '')}</td>
            </tr>
"""
        
        html += """
        </table>
        
        <h2>Security Findings</h2>
"""
        
        for finding in findings:
            severity = finding.get("severity", "LOW")
            html += f"""
        <div class="finding {severity}">
            <div class="finding-severity severity-{severity}">{severity}</div>
            <div class="finding-title">{finding.get('title')}</div>
            <p><strong>Description:</strong> {finding.get('description')}</p>
            <p><strong>Affected Asset:</strong> {finding.get('affected_asset')}</p>
            <p><strong>Evidence:</strong> {finding.get('evidence')}</p>
"""
            
            if finding.get("mitigation"):
                html += "<p><strong>Mitigation:</strong><ul>"
                for mit in finding.get("mitigation", []):
                    html += f"<li>{mit}</li>"
                html += "</ul></p>"
            
            html += "</div>"
        
        html += f"""
        
        <h2>Recommendations</h2>
        <ol>
            <li>Address all CRITICAL findings <strong>immediately</strong></li>
            <li>Schedule fixes for HIGH findings within <strong>1 week</strong></li>
            <li>Plan MEDIUM findings for next <strong>maintenance window</strong></li>
            <li>Address LOW findings during <strong>routine updates</strong></li>
        </ol>
        
        <div class="footer">
            <p>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Security Monitor v1.0 | Legitimate Assessment Tool</p>
            <p>This report contains sensitive security information. Handle with care.</p>
        </div>
    </div>
</body>
</html>
"""
        
        filepath = self.output_dir / f"{report_name}.html"
        with open(filepath, 'w') as f:
            f.write(html)
        
        return str(filepath)
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get action recommendation based on risk level"""
        recommendations = {
            "CRITICAL": "🚨 STOP: System requires IMMEDIATE remediation. Do not use in production.",
            "HIGH": "⚠️  URGENT: Address critical issues before full deployment. Plan remediation.",
            "MEDIUM": "📋 Plan fixes for next maintenance window. Monitor closely.",
            "LOW": "✓ Address during routine maintenance. Monitor for changes."
        }
        return recommendations.get(risk_level, "Unknown risk level")
