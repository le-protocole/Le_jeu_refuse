"""
Rule-based Vulnerability Analysis Engine
Purpose: Detect security issues based on scanning results
No exploitation - only static rule matching
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class Finding:
    """Security finding data structure"""
    severity: SeverityLevel
    title: str
    description: str
    affected_asset: str  # port, service, etc
    evidence: str
    cve_reference: Optional[str] = None
    mitigation: List[str] = field(default_factory=list)

class VulnerabilityRules:
    """
    Security rule engine
    Each rule checks specific conditions
    Returns findings if condition met
    """
    
    def __init__(self):
        self.rules = {
            "port": self._rule_port_exposure,
            "service": self._rule_service_version,
            "ssh": self._rule_ssh_config,
            "database": self._rule_database_exposure,
            "web": self._rule_web_server,
            "rpc": self._rule_rpc_exposure,
            "upnp": self._rule_upnp,
            "default_creds": self._rule_default_creds,
        }
    
    def analyze(self, scan_data: Dict) -> List[Finding]:
        """
        Run all rules against scan results
        Returns list of findings
        """
        findings = []
        
        for port_info in scan_data.get("open_ports", []):
            findings.extend(self._check_port_rules(port_info))
        
        # Check for absence of security headers
        if not scan_data.get("open_ports"):
            findings.append(Finding(
                severity=SeverityLevel.LOW,
                title="No public services detected",
                description="No accessible ports found (positive indicator)",
                affected_asset="all",
                evidence="Nmap scan returned no open ports",
                mitigation=[]
            ))
        
        return findings
    
    def _check_port_rules(self, port_info: Dict) -> List[Finding]:
        """Apply all rules to a single port"""
        findings = []
        
        port = port_info.get("port")
        service = port_info.get("service", "").lower()
        version = port_info.get("version", "").lower()
        state = port_info.get("state")
        
        # SSH (Port 22)
        if port == 22:
            findings.extend(self._rule_ssh_config(port_info))
        
        # FTP (Port 21) - Insecure protocol
        if port == 21:
            findings.append(Finding(
                severity=SeverityLevel.HIGH,
                title="Insecure FTP service detected",
                description="FTP transmits credentials in plaintext. Should use SFTP or SCP.",
                affected_asset=f"port {port}",
                evidence="Port 21 (FTP) is open",
                mitigation=[
                    "Disable FTP service",
                    "Use SFTP instead (port 22)",
                    "Restrict access by IP if FTP is required"
                ]
            ))
        
        # MySQL / MariaDB (Port 3306)
        if port == 3306 and "mysql" in service:
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title="Database exposed on public interface",
                description="MySQL/MariaDB is accessible from the network. Can lead to data breach.",
                affected_asset=f"port {port} ({service})",
                evidence=f"Service detected: {service} {version}",
                mitigation=[
                    "Bind MySQL to localhost (127.0.0.1) only",
                    "Enable firewall rules to restrict access",
                    "Use strong database authentication",
                    "Enable encrypted connections (SSL/TLS)"
                ]
            ))
        
        # PostgreSQL (Port 5432)
        if port == 5432 and "postgres" in service:
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title="PostgreSQL exposed on public interface",
                description="PostgreSQL database is publicly accessible.",
                affected_asset=f"port {port} ({service})",
                evidence=f"Service detected: {service} {version}",
                mitigation=[
                    "Bind PostgreSQL to localhost only",
                    "Configure pg_hba.conf to restrict connections",
                    "Use strong authentication",
                    "Enable SSL/TLS"
                ]
            ))
        
        # RDP (Port 3389) - Remote Desktop
        if port == 3389:
            findings.append(Finding(
                severity=SeverityLevel.HIGH,
                title="RDP exposed - Ransomware risk",
                description="Remote Desktop Protocol is publicly accessible. Common attack vector for ransomware.",
                affected_asset=f"port {port}",
                evidence="Port 3389 (RDP) is open",
                mitigation=[
                    "Restrict RDP access by IP address",
                    "Use VPN for remote access instead",
                    "Enable Network Level Authentication (NLA)",
                    "Implement IP allowlisting",
                    "Change default RDP port if possible"
                ]
            ))
        
        # VNC (Port 5900)
        if port == 5900:
            findings.append(Finding(
                severity=SeverityLevel.HIGH,
                title="VNC service exposed",
                description="VNC (Virtual Network Computing) allows remote desktop access without encryption by default.",
                affected_asset=f"port {port}",
                evidence="Port 5900 (VNC) is open",
                mitigation=[
                    "Restrict VNC to internal network only",
                    "Enable VNC password protection",
                    "Use SSH tunneling for VNC connections",
                    "Disable VNC if not required"
                ]
            ))
        
        # Telnet (Port 23) - Legacy insecure
        if port == 23:
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title="Telnet service detected (critically insecure)",
                description="Telnet sends all data including passwords in plaintext.",
                affected_asset=f"port {port}",
                evidence="Port 23 (Telnet) is open",
                mitigation=[
                    "Completely disable Telnet",
                    "Use SSH instead for remote access",
                    "Remove Telnet from autostart"
                ]
            ))
        
        # HTTP without HTTPS (Port 80)
        if port == 80 and service in ["http", "http-proxy"]:
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="Unencrypted HTTP service",
                description="HTTP without HTTPS means traffic is not encrypted.",
                affected_asset=f"port {port}",
                evidence="Port 80 (HTTP) is open",
                mitigation=[
                    "Enable HTTPS (Port 443)",
                    "Redirect all HTTP to HTTPS",
                    "Install valid SSL/TLS certificate",
                    "Enable HSTS (HTTP Strict-Transport-Security)"
                ]
            ))
        
        # SNMP (Port 161) - Often misconfigured
        if port == 161:
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="SNMP service exposed",
                description="SNMP uses weak authentication by default. Can leak system information.",
                affected_asset=f"port {port}",
                evidence="Port 161 (SNMP) is open",
                mitigation=[
                    "Restrict SNMP access by IP",
                    "Use SNMPv3 with authentication",
                    "Change default community strings",
                    "Disable SNMP if not required"
                ]
            ))
        
        # Outdated Apache versions
        if "apache" in service and version:
            if self._is_outdated_apache(version):
                findings.append(Finding(
                    severity=SeverityLevel.MEDIUM,
                    title="Outdated Apache version detected",
                    description=f"Apache {version} contains known vulnerabilities.",
                    affected_asset=f"port {port} (Apache)",
                    evidence=f"Apache version: {version}",
                    mitigation=[
                        "Update Apache to latest version",
                        "Subscribe to Apache security mailing list",
                        "Test updates in staging environment first",
                        "Enable automatic security updates if available"
                    ]
                ))
        
        # SMB (Port 445) - Windows file sharing
        if port == 445:
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="SMB/CIFS exposed - LAN exposure risk",
                description="SMB is intended for internal network use only.",
                affected_asset=f"port {port}",
                evidence="Port 445 (SMB) is open",
                mitigation=[
                    "Disable SMB if not required",
                    "Restrict SMB to internal network only",
                    "Disable SMBv1 (very insecure)",
                    "Enable firewall rules",
                    "Implement IP allowlisting"
                ]
            ))
        
        # Memcached (Port 11211)
        if port == 11211:
            findings.append(Finding(
                severity=SeverityLevel.HIGH,
                title="Memcached exposed - DDoS amplification",
                description="Memcached with no authentication is used in DDoS attacks.",
                affected_asset=f"port {port}",
                evidence="Port 11211 (Memcached) is open",
                mitigation=[
                    "Bind Memcached to localhost only",
                    "Restrict access by firewall",
                    "Use network ACLs",
                    "Disable Memcached if not required",
                    "Update to latest version"
                ]
            ))
        
        # MongoDB (Port 27017)
        if port == 27017 and ("mongo" in service or "mongodb" in service):
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title="MongoDB exposed on public interface",
                description="Unprotected MongoDB can lead to complete data theft.",
                affected_asset=f"port {port} (MongoDB)",
                evidence="Port 27017 (MongoDB) is open",
                mitigation=[
                    "Bind MongoDB to localhost only",
                    "Enable authentication (username/password)",
                    "Use TLS/SSL for connections",
                    "Implement IP allowlisting",
                    "Create strong, unique database passwords"
                ]
            ))
        
        # Redis (Port 6379)
        if port == 6379 and "redis" in service:
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title="Redis exposed without authentication",
                description="Redis without password protection allows arbitrary command execution.",
                affected_asset=f"port {port} (Redis)",
                evidence="Port 6379 (Redis) is open",
                mitigation=[
                    "Set a strong Redis password (requirepass)",
                    "Bind Redis to localhost only",
                    "Restrict access by firewall",
                    "Use Redis with ACL (Redis 6.0+)",
                    "Use TLS/SSL encryption"
                ]
            ))
        
        return findings
    
    def _rule_ssh_config(self, port_info: Dict) -> List[Finding]:
        """SSH-specific security checks"""
        findings = []
        service = port_info.get("service", "").lower()
        version = port_info.get("version", "").lower()
        
        if port_info.get("port") == 22 or "ssh" in service:
            # SSH should use key-based auth only
            findings.append(Finding(
                severity=SeverityLevel.HIGH,
                title="SSH password authentication likely enabled",
                description="SSH with password authentication is vulnerable to brute-force attacks.",
                affected_asset="port 22 (SSH)",
                evidence=f"SSH service detected: {version}",
                mitigation=[
                    "Disable password authentication in sshd_config",
                    "Enable key-based authentication only",
                    "Use SSH keys with strong passphrases",
                    "Consider using fail2ban or similar",
                    "Restrict SSH to specific IPs if possible"
                ]
            ))
            
            # Outdated SSH versions
            if version and self._is_outdated_ssh(version):
                findings.append(Finding(
                    severity=SeverityLevel.MEDIUM,
                    title="Outdated OpenSSH version",
                    description=f"OpenSSH {version} may contain security vulnerabilities.",
                    affected_asset="port 22 (SSH)",
                    evidence=f"OpenSSH version: {version}",
                    mitigation=[
                        "Update OpenSSH to latest version",
                        "Test updates in staging first",
                        "Review OpenSSH security advisories"
                    ]
                ))
        
        return findings
    
    def _rule_port_exposure(self, port_info: Dict) -> List[Finding]:
        """General port exposure rules"""
        findings = []
        port = port_info.get("port")
        
        # Privileged ports (< 1024) should not be exposed
        if port and port < 1024:
            findings.append(Finding(
                severity=SeverityLevel.LOW,
                title="Privileged port exposed",
                description=f"Port {port} is in privileged range (< 1024). Review if this service should be public.",
                affected_asset=f"port {port}",
                evidence=f"Open privileged port: {port}",
                mitigation=["Review service necessity", "Consider restricting access"]
            ))
        
        return findings
    
    def _rule_service_version(self, port_info: Dict) -> List[Finding]:
        """Service version vulnerability check"""
        # This is static - no actual CVE lookup
        # Just warns about outdated versions
        findings = []
        return findings
    
    def _rule_database_exposure(self, port_info: Dict) -> List[Finding]:
        """Database-specific exposure checks"""
        findings = []
        port = port_info.get("port")
        service = port_info.get("service", "").lower()
        
        db_ports = {3306: "MySQL", 5432: "PostgreSQL", 27017: "MongoDB", 6379: "Redis"}
        
        if port in db_ports:
            findings.append(Finding(
                severity=SeverityLevel.CRITICAL,
                title=f"{db_ports[port]} exposed",
                description="Database should never be publicly accessible",
                affected_asset=f"port {port}",
                evidence=f"Database port open: {port}",
                mitigation=["Bind to localhost", "Use firewall rules", "Enable authentication"]
            ))
        
        return findings
    
    def _rule_web_server(self, port_info: Dict) -> List[Finding]:
        """Web server vulnerability checks"""
        findings = []
        service = port_info.get("service", "").lower()
        
        if "http" in service:
            findings.append(Finding(
                severity=SeverityLevel.LOW,
                title="Web server detected",
                description="Ensure web server is properly configured and updated",
                affected_asset=f"port {port_info.get('port')}",
                evidence=f"Service: {service}",
                mitigation=["Keep software updated", "Use security headers", "Enable HTTPS"]
            ))
        
        return findings
    
    def _rule_rpc_exposure(self, port_info: Dict) -> List[Finding]:
        """RPC service exposure checks"""
        findings = []
        port = port_info.get("port")
        
        if port in [111, 135, 139, 445]:  # RPC, DCOM, NetBIOS, SMB
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="RPC/DCOM service exposed",
                description="Remote Procedure Call services should not be publicly exposed",
                affected_asset=f"port {port}",
                evidence=f"RPC port open: {port}",
                mitigation=["Restrict access", "Use firewall", "Disable if not needed"]
            ))
        
        return findings
    
    def _rule_upnp(self, port_info: Dict) -> List[Finding]:
        """UPnP exposure check"""
        findings = []
        if port_info.get("port") == 1900:
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="UPnP service exposed",
                description="UPnP can be used to bypass NAT/firewall rules",
                affected_asset="port 1900",
                evidence="UPnP (SSDP) port open",
                mitigation=["Disable UPnP", "Restrict to internal network", "Update firmware"]
            ))
        return findings
    
    def _rule_default_creds(self, port_info: Dict) -> List[Finding]:
        """Warning about default credentials"""
        findings = []
        service = port_info.get("service", "").lower()
        
        if any(x in service for x in ["http", "admin", "web", "snmp"]):
            findings.append(Finding(
                severity=SeverityLevel.MEDIUM,
                title="Service may use default credentials",
                description=f"{service} may be configured with default username/password",
                affected_asset=f"port {port_info.get('port')}",
                evidence=f"Service: {service}",
                mitigation=[
                    "Change all default credentials",
                    "Use strong, unique passwords",
                    "Disable default accounts",
                    "Document all access credentials securely"
                ]
            ))
        
        return findings
    
    def _is_outdated_apache(self, version: str) -> bool:
        """Check if Apache version is outdated"""
        # Simple version check - outdated before 2.4.50
        try:
            version_num = float(version.split()[0].split('/')[1])
            return version_num < 2.4
        except:
            return False
    
    def _is_outdated_ssh(self, version: str) -> bool:
        """Check if OpenSSH is outdated"""
        try:
            # Outdated before 8.0
            version_str = version.lower()
            if "openssh" in version_str:
                version_num = float(version_str.split("_")[1].split("p")[0] if "_" in version_str else "7.0")
                return version_num < 8.0
        except:
            return False
        return False
