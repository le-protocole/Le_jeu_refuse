"""
Export Manager - CSV/PDF Report Generation
Exports security scan results to multiple formats
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class ExportManager:
    """Manages report export in CSV and PDF formats"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
    
    def export_to_csv(self, scan_data: Dict[str, Any], filename: str = None) -> str:
        """Export scan results to CSV format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = scan_data.get("domain", "scan")
            filename = f"report_{domain}_{timestamp}.csv"
        
        filepath = self.reports_dir / filename
        
        # Flatten the data structure
        rows = self._flatten_data(scan_data)
        
        if not rows:
            return str(filepath)
        
        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        return str(filepath)
    
    def export_to_pdf(self, scan_data: Dict[str, Any], filename: str = None) -> str:
        """Export scan results to PDF format"""
        if not HAS_REPORTLAB:
            raise ImportError("reportlab not installed. Install with: pip install reportlab")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = scan_data.get("domain", "scan")
            filename = f"report_{domain}_{timestamp}.pdf"
        
        filepath = self.reports_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph("Security Scan Report", title_style))
        
        # Scan metadata
        domain = scan_data.get("domain", "Unknown")
        timestamp = scan_data.get("timestamp", "Unknown")
        risk_score = scan_data.get("risk_score", 0)
        risk_level = scan_data.get("risk_level", "UNKNOWN")
        
        metadata_text = f"""
        <b>Domain:</b> {domain}<br/>
        <b>Scan Date:</b> {timestamp}<br/>
        <b>Risk Score:</b> {risk_score}/100<br/>
        <b>Risk Level:</b> {risk_level}<br/>
        """
        elements.append(Paragraph(metadata_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        summary = scan_data.get("summary", "No summary available")
        elements.append(Paragraph(summary, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Findings section
        if "findings" in scan_data:
            elements.append(Paragraph("Findings", styles['Heading2']))
            findings = scan_data["findings"]
            
            if isinstance(findings, list):
                for finding in findings:
                    if isinstance(finding, dict):
                        title = finding.get("title", "Unknown")
                        severity = finding.get("severity", "Info")
                        description = finding.get("description", "N/A")
                        finding_text = f"<b>{title}</b> [{severity}]<br/>{description}"
                        elements.append(Paragraph(finding_text, styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations section
        if "recommendations" in scan_data:
            elements.append(PageBreak())
            elements.append(Paragraph("Recommendations", styles['Heading2']))
            recommendations = scan_data["recommendations"]
            
            if isinstance(recommendations, list):
                for i, rec in enumerate(recommendations, 1):
                    if isinstance(rec, dict):
                        rec_text = f"{i}. {rec.get('action', rec)}"
                        elements.append(Paragraph(rec_text, styles['Normal']))
                    else:
                        elements.append(Paragraph(f"{i}. {rec}", styles['Normal']))
                    elements.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(elements)
        return str(filepath)
    
    def _flatten_data(self, data: Dict[str, Any], parent_key: str = '') -> List[Dict]:
        """Flatten nested dictionary for CSV export"""
        rows = []
        
        def flatten_item(item, prefix=''):
            if isinstance(item, dict):
                flat = {}
                for key, value in item.items():
                    new_key = f"{prefix}{key}" if prefix else key
                    if isinstance(value, (dict, list)):
                        sub_flat = flatten_item(value, f"{new_key}_")
                        if isinstance(sub_flat, list):
                            for sf in sub_flat:
                                flat.update(sf)
                        else:
                            flat.update(sub_flat)
                    else:
                        flat[new_key] = str(value)
                return flat
            elif isinstance(item, list):
                result = []
                for idx, list_item in enumerate(item):
                    result.append(flatten_item(list_item, f"{prefix}[{idx}]_"))
                return result
            else:
                return {prefix: str(item)}
        
        flattened = flatten_item(data)
        
        if isinstance(flattened, dict):
            rows.append(flattened)
        elif isinstance(flattened, list):
            rows.extend(flattened)
        
        return rows if rows else [{"data": json.dumps(data)}]
    
    def export_json(self, scan_data: Dict[str, Any], filename: str = None) -> str:
        """Export scan results to JSON format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = scan_data.get("domain", "scan")
            filename = f"report_{domain}_{timestamp}.json"
        
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scan_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def list_exports(self) -> Dict[str, List[str]]:
        """List all exported reports by format"""
        reports = {
            "csv": [],
            "pdf": [],
            "json": []
        }
        
        for file in self.reports_dir.iterdir():
            if file.suffix == '.csv':
                reports["csv"].append(file.name)
            elif file.suffix == '.pdf':
                reports["pdf"].append(file.name)
            elif file.suffix == '.json':
                reports["json"].append(file.name)
        
        return reports


def export_report(scan_data: Dict[str, Any], format: str = "json") -> str:
    """Quick export function
    
    Args:
        scan_data: Dictionary of scan results
        format: Export format ('json', 'csv', 'pdf')
    
    Returns:
        Path to exported file
    """
    manager = ExportManager()
    
    if format.lower() == "csv":
        return manager.export_to_csv(scan_data)
    elif format.lower() == "pdf":
        return manager.export_to_pdf(scan_data)
    else:  # Default to JSON
        return manager.export_json(scan_data)
