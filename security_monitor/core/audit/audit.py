"""
Audit Logging Module
Purpose: Track all administrative actions for compliance
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class AuditLogger:
    """Audit trail for all system operations"""
    
    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
    
    def log(self, 
            action: str,
            admin_user: str = "admin",
            target: str = "",
            status: str = "success",
            details: Dict = None):
        """
        Log an administrative action
        
        Args:
            action: Action being performed (scan, config_change, etc)
            admin_user: User performing action
            target: Target being acted upon
            status: success/failure
            details: Additional context
        """
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "admin_user": admin_user,
            "target": target,
            "status": status,
            "details": details or {}
        }
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Also print to console
        print(f"[AUDIT] {log_entry['timestamp']} | {action} | {status}")
    
    def log_scan_start(self, target: str, scan_type: str, admin: str = "admin"):
        """Log scan initiation"""
        self.log(
            action="SCAN_INITIATED",
            admin_user=admin,
            target=target,
            details={"scan_type": scan_type}
        )
    
    def log_scan_complete(self, target: str, findings_count: int, 
                         risk_level: str, admin: str = "admin"):
        """Log scan completion"""
        self.log(
            action="SCAN_COMPLETED",
            admin_user=admin,
            target=target,
            details={
                "findings": findings_count,
                "risk_level": risk_level
            }
        )
    
    def log_report_generated(self, target: str, format: str, 
                            file_path: str, admin: str = "admin"):
        """Log report generation"""
        self.log(
            action="REPORT_GENERATED",
            admin_user=admin,
            target=target,
            details={"format": format, "file_path": file_path}
        )
    
    def log_config_change(self, config_key: str, old_value: str, 
                         new_value: str, admin: str = "admin"):
        """Log configuration change"""
        self.log(
            action="CONFIG_CHANGED",
            admin_user=admin,
            details={
                "config_key": config_key,
                "old_value": str(old_value),
                "new_value": str(new_value)
            }
        )
    
    def log_access(self, action: str, ip_address: str = "localhost", 
                  success: bool = True):
        """Log system access"""
        self.log(
            action="SYSTEM_ACCESS",
            status="success" if success else "failure",
            details={"ip_address": ip_address, "action": action}
        )
