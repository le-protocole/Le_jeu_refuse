#!/usr/bin/env python3
"""
Security Monitoring System - Web API Server
FastAPI backend for web interface
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from pathlib import Path

from core.resolver.dns import DNSResolver
from core.scanner.nmap import NmapScanner
from core.analysis.rules import VulnerabilityRules
from core.risk.scorer import RiskScorer
from core.fixes.recommendations import RecommendationEngine
from db.database import DatabaseManager

# Initialize FastAPI
app = FastAPI(
    title="Security Monitoring System",
    description="Blue-Team Security Posture Scanner",
    version="1.0"
)

# Initialize modules
resolver = DNSResolver()
scanner = NmapScanner()
rules = VulnerabilityRules()
scorer = RiskScorer()
recommendations = RecommendationEngine()
db = DatabaseManager()

# Ensure reports directory exists
Path("reports").mkdir(exist_ok=True)

# Pydantic models
class ScanRequest(BaseModel):
    target: str
    scan_type: str = "quick"  # quick, standard, thorough

class ScanResponse(BaseModel):
    target: str
    ip_address: str
    behind_cdn: bool
    open_ports: int
    vulnerabilities: int
    risk_score: int
    risk_level: str
    report_file: str

# API Routes
@app.get("/")
async def root():
    """Return web UI HTML"""
    return HTMLResponse(get_html_ui())

@app.get("/api/health")
async def health():
    """Health check"""
    return {"status": "ok", "version": "1.0"}

@app.post("/api/scan", response_model=ScanResponse)
async def scan_target(request: ScanRequest):
    """
    Scan a target website or IP
    
    Query Parameters:
    - target: URL or IP address (e.g., google.com, 1.2.3.4)
    - scan_type: quick, standard, or thorough
    """
    try:
        target = request.target.strip()
        scan_type = request.scan_type.lower()
        
        if not target:
            raise HTTPException(status_code=400, detail="Target cannot be empty")
        
        if scan_type not in ["quick", "standard", "thorough"]:
            raise HTTPException(status_code=400, detail="Invalid scan type")
        
        # Step 1: DNS Resolution
        dns_result = resolver.resolve_domain(target)
        
        if not dns_result['ips'] and not dns_result['cname_records']:
            raise HTTPException(status_code=404, detail=f"Could not resolve {target}")
        
        target_ip = dns_result['ips'][0] if dns_result['ips'] else None
        
        if not target_ip:
            raise HTTPException(status_code=404, detail="No IP address found")
        
        # Step 2: Port Scanning
        if scan_type == "quick":
            scan_result = scanner.quick_scan(target_ip)
        elif scan_type == "standard":
            scan_result = scanner.standard_scan(target_ip)
        else:
            scan_result = scanner.thorough_scan(target_ip)
        
        # If Nmap fails, return error (no demo data fallback)
        if not scan_result or 'error' in scan_result:
            return {
                "error": "Scan failed - Nmap not available or unreachable target",
                "target": target_ip
            }
        
        open_ports = scan_result.get('ports', [])
        
        # Step 3: Vulnerability Analysis
        findings = rules.analyze(scan_result)
        
        # Step 4: Risk Scoring
        risk_score = scorer.calculate_score(
            findings=[{
                'severity': f.severity.value,
                'title': f.title,
                'description': f.description
            } for f in findings],
            open_ports=open_ports
        )
        
        # Step 5: Generate Report
        report_data = {
            "scan_date": dns_result['timestamp'],
            "target": dns_result['target'],
            "ip_address": target_ip,
            "behind_cdn": dns_result['cdn'],
            "cdn_provider": dns_result['cdn_provider'],
            "open_ports": open_ports,
            "findings_count": len(findings),
            "risk_score": risk_score['score'],
            "risk_level": risk_score['level'].value,
            "findings": [
                {
                    "severity": f.severity.value,
                    "title": f.title,
                    "description": f.description
                }
                for f in findings[:5]
            ]
        }
        
        # Save report
        report_file = f"reports/{dns_result['target']}_report.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return ScanResponse(
            target=dns_result['target'],
            ip_address=target_ip,
            behind_cdn=dns_result['cdn'],
            open_ports=len(open_ports),
            vulnerabilities=len(findings),
            risk_score=risk_score['score'],
            risk_level=risk_score['level'].value,
            report_file=report_file
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
async def list_reports():
    """List all generated reports"""
    try:
        report_files = list(Path("reports").glob("*.json"))
        reports = []
        
        for report_file in sorted(report_files, reverse=True)[:20]:
            with open(report_file, 'r') as f:
                data = json.load(f)
                reports.append({
                    "file": report_file.name,
                    "target": data.get('target'),
                    "ip": data.get('ip_address'),
                    "risk_score": data.get('risk_score'),
                    "risk_level": data.get('risk_level'),
                    "scan_date": data.get('scan_date')
                })
        
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{report_name}")
async def get_report(report_name: str):
    """Get specific report details"""
    try:
        report_path = Path("reports") / report_name
        
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        return report_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_html_ui() -> str:
    """Return HTML UI for web interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Monitoring System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        header h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        header p {
            color: #666;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        input[type="text"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-scan {
            background: #667eea;
            color: white;
        }
        
        .btn-scan:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        .btn-reports {
            background: #764ba2;
            color: white;
        }
        
        .btn-reports:hover {
            background: #6a3d8f;
            transform: translateY(-2px);
        }
        
        .btn-scan:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            display: none;
            background: #f9f9f9;
            border-radius: 5px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .results.active {
            display: block;
        }
        
        .result-item {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            border-radius: 3px;
        }
        
        .result-item.critical {
            border-left-color: #f44336;
        }
        
        .result-item.high {
            border-left-color: #ff9800;
        }
        
        .result-item.medium {
            border-left-color: #ffc107;
        }
        
        .result-item.low {
            border-left-color: #4caf50;
        }
        
        .result-label {
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .result-value {
            color: #333;
            font-size: 16px;
            font-weight: 600;
        }
        
        .risk-score {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        
        .risk-level {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            font-size: 12px;
            margin-left: 10px;
        }
        
        .risk-level.low {
            background: #4caf50;
        }
        
        .risk-level.medium {
            background: #ffc107;
            color: #333;
        }
        
        .risk-level.high {
            background: #ff9800;
        }
        
        .risk-level.critical {
            background: #f44336;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            display: none;
        }
        
        .error.active {
            display: block;
        }
        
        .reports-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .report-item {
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.3s;
            border-left: 3px solid #667eea;
        }
        
        .report-item:hover {
            background: #f5f5f5;
            transform: translateX(5px);
        }
        
        .report-target {
            font-weight: 600;
            color: #333;
        }
        
        .report-meta {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Security Monitor</h1>
            <p>Blue-Team Security Posture Scanner</p>
        </header>
        
        <div class="form-group">
            <label for="target">Target URL or IP Address</label>
            <input 
                type="text" 
                id="target" 
                placeholder="e.g., google.com or 1.2.3.4"
                value="google.com"
            />
        </div>
        
        <div class="form-group">
            <label for="scanType">Scan Type</label>
            <select id="scanType">
                <option value="quick">Quick Scan (2 minutes)</option>
                <option value="standard">Standard Scan (10 minutes)</option>
                <option value="thorough">Deep Scan (30 minutes)</option>
            </select>
        </div>
        
        <div class="button-group">
            <button class="btn-scan" onclick="startScan()">Start Scan</button>
            <button class="btn-reports" onclick="showReports()">View Reports</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; color: #666;">Scanning... Please wait</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results"></div>
    </div>
    
    <script>
        async function startScan() {
            const target = document.getElementById('target').value.trim();
            const scanType = document.getElementById('scanType').value;
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const results = document.getElementById('results');
            
            if (!target) {
                error.textContent = 'Please enter a target URL or IP address';
                error.classList.add('active');
                return;
            }
            
            error.classList.remove('active');
            results.classList.remove('active');
            loading.classList.add('active');
            
            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        target: target,
                        scan_type: scanType
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Scan failed');
                }
                
                const data = await response.json();
                displayResults(data);
                
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.classList.add('active');
            } finally {
                loading.classList.remove('active');
            }
        }
        
        function displayResults(data) {
            const results = document.getElementById('results');
            const riskColor = data.risk_level.toLowerCase();
            
            results.innerHTML = `
                <div class="result-item">
                    <div class="result-label">Target</div>
                    <div class="result-value">${data.target} (${data.ip_address})</div>
                </div>
                
                <div class="result-item">
                    <div class="result-label">Risk Assessment</div>
                    <div class="result-value">
                        <span class="risk-score">${data.risk_score}/100</span>
                        <span class="risk-level ${riskColor}">${data.risk_level}</span>
                    </div>
                </div>
                
                <div class="result-item ${riskColor}">
                    <div class="result-label">Open Ports</div>
                    <div class="result-value">${data.open_ports}</div>
                </div>
                
                <div class="result-item ${riskColor}">
                    <div class="result-label">Vulnerabilities Found</div>
                    <div class="result-value">${data.vulnerabilities}</div>
                </div>
                
                <div class="result-item">
                    <div class="result-label">Behind CDN</div>
                    <div class="result-value">${data.behind_cdn ? 'Yes' : 'No'}</div>
                </div>
                
                <div class="result-item">
                    <div class="result-label">Report</div>
                    <div class="result-value">
                        <a href="/api/report/${data.report_file.split('/').pop()}" target="_blank">
                            View Full Report
                        </a>
                    </div>
                </div>
            `;
            
            results.classList.add('active');
        }
        
        async function showReports() {
            try {
                const response = await fetch('/api/reports');
                const data = await response.json();
                
                if (data.reports.length === 0) {
                    alert('No reports found yet');
                    return;
                }
                
                let reportsList = 'Recent Reports:\\n\\n';
                data.reports.forEach(report => {
                    reportsList += `${report.target} (${report.risk_level} - ${report.risk_score})\\n`;
                });
                
                alert(reportsList);
            } catch (err) {
                alert('Error loading reports: ' + err.message);
            }
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    print("""
================================================================================
  SECURITY MONITORING SYSTEM - WEB SERVER
================================================================================

[*] Starting FastAPI server...

Web Interface: http://localhost:8000
API Docs: http://localhost:8000/docs
Status: http://localhost:8000/api/health

Press CTRL+C to stop

================================================================================
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
