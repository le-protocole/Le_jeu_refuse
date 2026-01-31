"""
Risk Scoring Engine
Purpose: Calculate overall risk score based on findings
"""

from typing import List, Dict, Tuple
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskScorer:
    """
    Calculates risk score from security findings
    Weighs different types of findings
    """
    
    # Severity weights
    SEVERITY_WEIGHTS = {
        "CRITICAL": 30,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 3
    }
    
    # Port exposure multiplier
    PORT_WEIGHTS = {
        22: 1.5,    # SSH - high attack target
        3306: 2.0,  # MySQL - DB exposure
        5432: 2.0,  # PostgreSQL
        27017: 2.0, # MongoDB
        6379: 2.0,  # Redis
        3389: 1.8,  # RDP - ransomware vector
        5900: 1.5,  # VNC
        445: 1.5,   # SMB
        3389: 1.8,  # RDP
        21: 1.5,    # FTP
    }
    
    # Service criticality
    SERVICE_CRITICALITY = {
        "mysql": 2.0,
        "postgresql": 2.0,
        "mongodb": 2.0,
        "redis": 2.0,
        "ssh": 1.5,
        "http": 1.2,
        "https": 0.8,
        "ftp": 1.8,
        "telnet": 2.5,
    }
    
    def calculate_score(self, findings: List[Dict], open_ports: List[Dict]) -> Dict:
        """
        Calculate risk score from findings
        
        Returns:
        {
            "score": 0-100,
            "level": "LOW|MEDIUM|HIGH|CRITICAL",
            "breakdown": {
                "finding_count": int,
                "critical_count": int,
                "high_count": int,
                ...
            },
            "recommendation_priority": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        }
        """
        
        score = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        # Score each finding
        for finding in findings:
            severity = finding.get("severity", "LOW")
            
            weight = self.SEVERITY_WEIGHTS.get(severity, 0)
            score += weight
            
            if severity == "CRITICAL":
                critical_count += 1
            elif severity == "HIGH":
                high_count += 1
            elif severity == "MEDIUM":
                medium_count += 1
            elif severity == "LOW":
                low_count += 1
        
        # Bonus points for dangerous port combinations
        open_port_numbers = [p.get("port") for p in open_ports]
        
        # Database + web server = higher risk
        if any(p in open_port_numbers for p in [3306, 5432, 27017, 6379]):
            if any(p in open_port_numbers for p in [80, 443, 8080]):
                score += 15
        
        # Multiple RPC/admin ports = higher risk
        rpc_ports = [135, 139, 445, 111]
        rpc_open = sum(1 for p in open_port_numbers if p in rpc_ports)
        if rpc_open >= 2:
            score += 10
        
        # SSH + RDP both open = increased risk
        if 22 in open_port_numbers and 3389 in open_port_numbers:
            score += 10
        
        # Cap score at 100
        score = min(score, 100)
        
        # Determine risk level
        risk_level = self._score_to_level(score)
        
        return {
            "score": score,
            "level": risk_level,
            "breakdown": {
                "total_findings": len(findings),
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "open_port_count": len(open_ports),
            "risk_factors": {
                "databases_exposed": any(p in open_port_numbers for p in [3306, 5432, 27017, 6379]),
                "ssh_exposed": 22 in open_port_numbers,
                "rdp_exposed": 3389 in open_port_numbers,
                "ftp_exposed": 21 in open_port_numbers,
                "telnet_exposed": 23 in open_port_numbers,
                "web_exposed": any(p in open_port_numbers for p in [80, 443, 8080, 8443])
            }
        }
    
    def _score_to_level(self, score: int) -> RiskLevel:
        """Convert numerical score to risk level"""
        if score >= 81:
            return RiskLevel.CRITICAL
        elif score >= 61:
            return RiskLevel.HIGH
        elif score >= 31:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def prioritize_findings(self, findings: List[Dict]) -> List[Dict]:
        """
        Sort findings by severity for priority fixing
        CRITICAL → HIGH → MEDIUM → LOW
        """
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        
        sorted_findings = sorted(
            findings,
            key=lambda x: severity_order.get(x.get("severity", "LOW"), 999)
        )
        
        return sorted_findings


# Risk level guidance
RISK_GUIDANCE = {
    "CRITICAL": {
        "description": "System is at immediate risk of compromise",
        "action": "Fix immediately - system should not be in production",
        "timeframe": "Within 24 hours"
    },
    "HIGH": {
        "description": "System has significant security issues",
        "action": "Fix urgent before full production deployment",
        "timeframe": "Within 1 week"
    },
    "MEDIUM": {
        "description": "System has notable security concerns",
        "action": "Plan fixes for next maintenance window",
        "timeframe": "Within 1 month"
    },
    "LOW": {
        "description": "System has minor security recommendations",
        "action": "Address during regular maintenance",
        "timeframe": "Within 3 months"
    }
}
