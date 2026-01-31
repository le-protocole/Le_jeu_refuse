"""
SQLite Database Manager
Purpose: Store scan results, findings, and audit logs
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class DatabaseManager:
    """
    SQLite database for Security Monitor
    Stores: targets, scans, results, findings, audit logs
    """
    
    def __init__(self, db_path: str = "security_monitor.db"):
        self.db_path = Path(db_path)
        self.connection = None
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Targets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    url TEXT,
                    ip_address TEXT,
                    owner TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_scanned TIMESTAMP,
                    confirmed_ownership BOOLEAN DEFAULT 0
                )
            """)
            
            # Scans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_id INTEGER NOT NULL,
                    scan_type TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT DEFAULT 'in_progress',
                    scan_data JSON,
                    FOREIGN KEY(target_id) REFERENCES targets(id)
                )
            """)
            
            # Findings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id INTEGER NOT NULL,
                    severity TEXT,
                    title TEXT,
                    description TEXT,
                    affected_asset TEXT,
                    evidence TEXT,
                    mitigation JSON,
                    found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'open',
                    FOREIGN KEY(scan_id) REFERENCES scans(id)
                )
            """)
            
            # Risk assessments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS risk_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id INTEGER NOT NULL,
                    score INTEGER,
                    level TEXT,
                    breakdown JSON,
                    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(scan_id) REFERENCES scans(id)
                )
            """)
            
            # Reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id INTEGER NOT NULL,
                    format TEXT,
                    file_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(scan_id) REFERENCES scans(id)
                )
            """)
            
            # Audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    admin_user TEXT,
                    target TEXT,
                    details JSON,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    # Target management
    def add_target(self, name: str, url: str, owner: str = "admin") -> int:
        """Add new target for scanning"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO targets (name, url, owner, confirmed_ownership)
                VALUES (?, ?, ?, 1)
            """, (name, url, owner))
            conn.commit()
            return cursor.lastrowid
    
    def get_targets(self) -> List[Dict]:
        """Get all targets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, url, owner, created_at, last_scanned
                FROM targets
                ORDER BY created_at DESC
            """)
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Scan management
    def add_scan(self, target_id: int, scan_type: str) -> int:
        """Create new scan record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scans (target_id, scan_type, status)
                VALUES (?, ?, 'in_progress')
            """, (target_id, scan_type))
            conn.commit()
            return cursor.lastrowid
    
    def complete_scan(self, scan_id: int, scan_data: Dict):
        """Mark scan as complete and store results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE scans
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP, scan_data = ?
                WHERE id = ?
            """, (json.dumps(scan_data), scan_id))
            conn.commit()
    
    # Findings management
    def add_finding(self, scan_id: int, finding: Dict):
        """Add finding from scan"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO findings 
                (scan_id, severity, title, description, affected_asset, evidence, mitigation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                scan_id,
                finding.get('severity'),
                finding.get('title'),
                finding.get('description'),
                finding.get('affected_asset'),
                finding.get('evidence'),
                json.dumps(finding.get('mitigation', []))
            ))
            conn.commit()
    
    def get_findings(self, scan_id: int) -> List[Dict]:
        """Get findings for specific scan"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, severity, title, description, affected_asset, evidence, mitigation, found_at
                FROM findings
                WHERE scan_id = ?
                ORDER BY 
                    CASE severity
                        WHEN 'CRITICAL' THEN 1
                        WHEN 'HIGH' THEN 2
                        WHEN 'MEDIUM' THEN 3
                        WHEN 'LOW' THEN 4
                    END
            """, (scan_id,))
            
            columns = [desc[0] for desc in cursor.description]
            findings = []
            for row in cursor.fetchall():
                finding = dict(zip(columns, row))
                finding['mitigation'] = json.loads(finding.get('mitigation', '[]'))
                findings.append(finding)
            
            return findings
    
    # Risk management
    def add_risk_assessment(self, scan_id: int, risk_analysis: Dict):
        """Store risk assessment results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO risk_assessments
                (scan_id, score, level, breakdown)
                VALUES (?, ?, ?, ?)
            """, (
                scan_id,
                risk_analysis.get('score'),
                risk_analysis.get('level'),
                json.dumps(risk_analysis.get('breakdown', {}))
            ))
            conn.commit()
    
    # Report management
    def add_report(self, scan_id: int, format: str, file_path: str):
        """Record generated report"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reports (scan_id, format, file_path)
                VALUES (?, ?, ?)
            """, (scan_id, format, file_path))
            conn.commit()
    
    # Audit logging
    def log_action(self, action: str, admin_user: str = "admin", 
                  target: str = "", details: Dict = None):
        """Log administrative action for audit trail"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_log (action, admin_user, target, details)
                VALUES (?, ?, ?, ?)
            """, (
                action,
                admin_user,
                target,
                json.dumps(details or {})
            ))
            conn.commit()
    
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Retrieve audit log"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT action, admin_user, target, details, timestamp
                FROM audit_log
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            logs = []
            for row in cursor.fetchall():
                log = dict(zip(columns, row))
                log['details'] = json.loads(log.get('details', '{}'))
                logs.append(log)
            
            return logs
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
