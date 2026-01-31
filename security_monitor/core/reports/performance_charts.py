"""
Performance Chart Generator - Visualization of Security Trends
Creates charts for risk trends, vulnerability distribution, compliance scores
"""

import json
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class PerformanceChartGenerator:
    """Generate performance and trend charts"""
    
    def __init__(self, charts_dir: str = "charts"):
        self.charts_dir = Path(charts_dir)
        self.charts_dir.mkdir(exist_ok=True)
    
    def generate_risk_trend_chart(self, scan_history: List[Dict[str, Any]], filename: str = None) -> str:
        """Generate risk score trend chart over time"""
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib not installed. Install with: pip install matplotlib")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"risk_trend_{timestamp}.png"
        
        filepath = self.charts_dir / filename
        
        # Extract data
        dates = []
        scores = []
        
        for scan in sorted(scan_history, key=lambda x: x.get("timestamp", "")):
            try:
                dates.append(datetime.fromisoformat(scan.get("timestamp", datetime.now().isoformat())))
                scores.append(int(scan.get("risk_score", 0)))
            except:
                continue
        
        if not scores:
            raise ValueError("No valid scan data found")
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, scores, marker='o', linewidth=2, markersize=8, color='#FF6B6B')
        ax.fill_between(dates, scores, alpha=0.3, color='#FF6B6B')
        
        # Add risk zones
        ax.axhspan(0, 30, alpha=0.1, color='green', label='Low Risk (0-30)')
        ax.axhspan(30, 60, alpha=0.1, color='yellow', label='Medium Risk (30-60)')
        ax.axhspan(60, 100, alpha=0.1, color='red', label='High Risk (60-100)')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Risk Score', fontsize=12, fontweight='bold')
        ax.set_title('Security Risk Score Trend', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def generate_vulnerability_distribution_chart(self, vulnerabilities: Dict[str, int], filename: str = None) -> str:
        """Generate pie chart of vulnerability severity distribution"""
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib not installed. Install with: pip install matplotlib")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vuln_distribution_{timestamp}.png"
        
        filepath = self.charts_dir / filename
        
        # Prepare data
        labels = list(vulnerabilities.keys())
        sizes = list(vulnerabilities.values())
        colors = {
            'CRITICAL': '#FF0000',
            'HIGH': '#FF6B6B',
            'MEDIUM': '#FFA500',
            'LOW': '#FFD700',
            'INFO': '#87CEEB'
        }
        pie_colors = [colors.get(label, '#CCCCCC') for label in labels]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        ax.set_title('Vulnerability Severity Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Make percentage text white and bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def generate_compliance_scorecard(self, compliance_data: Dict[str, float], filename: str = None) -> str:
        """Generate compliance score scorecard"""
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib not installed. Install with: pip install matplotlib")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compliance_scorecard_{timestamp}.png"
        
        filepath = self.charts_dir / filename
        
        # Prepare data
        frameworks = list(compliance_data.keys())
        scores = list(compliance_data.values())
        colors = ['#2ECC71' if s >= 70 else '#F39C12' if s >= 40 else '#E74C3C' for s in scores]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(frameworks, scores, color=colors, height=0.6)
        
        # Add score labels on bars
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 2, i, f'{int(score)}/100', va='center', fontweight='bold')
        
        ax.set_xlim(0, 110)
        ax.set_xlabel('Compliance Score (%)', fontsize=12, fontweight='bold')
        ax.set_title('Compliance Framework Scores', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Add reference lines
        ax.axvline(x=70, color='green', linestyle='--', alpha=0.5, label='Target (70%)')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def generate_module_coverage_chart(self, module_data: Dict[str, Any], filename: str = None) -> str:
        """Generate module coverage/execution chart"""
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib not installed. Install with: pip install matplotlib")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"module_coverage_{timestamp}.png"
        
        filepath = self.charts_dir / filename
        
        # Prepare data
        modules = list(module_data.keys())
        results = list(module_data.values())
        colors_map = {
            'completed': '#2ECC71',
            'partial': '#F39C12',
            'failed': '#E74C3C',
            'skipped': '#95A5A6'
        }
        colors = [colors_map.get(r.lower(), '#95A5A6') for r in results]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(modules, [1]*len(modules), color=colors, height=0.7)
        
        # Add status labels
        for i, (bar, result) in enumerate(zip(bars, results)):
            ax.text(i, 0.5, result, ha='center', va='center', fontweight='bold', color='white')
        
        ax.set_ylim(0, 1.2)
        ax.set_ylabel('Module Status', fontsize=12, fontweight='bold')
        ax.set_title('Scan Module Coverage', fontsize=14, fontweight='bold')
        ax.set_yticks([])
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ECC71', label='Completed'),
            Patch(facecolor='#F39C12', label='Partial'),
            Patch(facecolor='#E74C3C', label='Failed'),
            Patch(facecolor='#95A5A6', label='Skipped')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def generate_summary_report(self, scan_history: List[Dict[str, Any]], filename: str = None) -> str:
        """Generate a complete summary report with multiple charts"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_report_{timestamp}.html"
        
        filepath = self.charts_dir / filename
        
        # Calculate statistics
        total_scans = len(scan_history)
        avg_risk = sum(s.get("risk_score", 0) for s in scan_history) / total_scans if scan_history else 0
        max_risk = max(s.get("risk_score", 0) for s in scan_history) if scan_history else 0
        min_risk = min(s.get("risk_score", 0) for s in scan_history) if scan_history else 0
        
        # Generate HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Scan Summary Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .header {{ background-color: #1f4788; color: white; padding: 20px; border-radius: 5px; }}
                .stats-container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
                .stat-card {{ background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .stat-value {{ font-size: 28px; font-weight: bold; color: #1f4788; }}
                .stat-label {{ font-size: 14px; color: #666; margin-top: 10px; }}
                .chart-container {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #1f4788; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Security Scan Summary Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-value">{total_scans}</div>
                    <div class="stat-label">Total Scans</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{int(avg_risk)}</div>
                    <div class="stat-label">Average Risk Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{int(max_risk)}</div>
                    <div class="stat-label">Highest Risk</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{int(min_risk)}</div>
                    <div class="stat-label">Lowest Risk</div>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>Recent Scans</h2>
                <table>
                    <tr>
                        <th>Domain</th>
                        <th>Date</th>
                        <th>Risk Score</th>
                        <th>Risk Level</th>
                    </tr>
        """
        
        # Add recent scans
        for scan in sorted(scan_history, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]:
            risk_score = int(scan.get("risk_score", 0))
            risk_level = scan.get("risk_level", "UNKNOWN")
            domain = scan.get("domain", "Unknown")
            timestamp = scan.get("timestamp", "Unknown")
            html_content += f"""
                    <tr>
                        <td>{domain}</td>
                        <td>{timestamp}</td>
                        <td>{risk_score}</td>
                        <td>{risk_level}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def list_charts(self) -> Dict[str, List[str]]:
        """List all generated charts"""
        charts = {
            "risk_trends": [],
            "vulnerability_distribution": [],
            "compliance_scores": [],
            "module_coverage": [],
            "html_reports": []
        }
        
        for file in self.charts_dir.glob("*"):
            if "risk_trend" in file.name:
                charts["risk_trends"].append(file.name)
            elif "vuln_distribution" in file.name:
                charts["vulnerability_distribution"].append(file.name)
            elif "compliance" in file.name:
                charts["compliance_scores"].append(file.name)
            elif "module_coverage" in file.name:
                charts["module_coverage"].append(file.name)
            elif file.suffix == ".html":
                charts["html_reports"].append(file.name)
        
        return charts


def generate_risk_chart(scan_history: List[Dict[str, Any]]) -> str:
    """Quick function to generate risk trend chart"""
    generator = PerformanceChartGenerator()
    return generator.generate_risk_trend_chart(scan_history)
