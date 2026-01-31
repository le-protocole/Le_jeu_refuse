"""
Recommendations Engine
Purpose: Provide actionable hardening recommendations
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Recommendation:
    """Single actionable recommendation"""
    title: str
    description: str
    difficulty: str  # EASY, MEDIUM, HARD
    impact: str  # LOW, MEDIUM, HIGH
    steps: List[str]
    tools_needed: List[str] = None
    estimated_time: str = "Unknown"
    
    def __post_init__(self):
        if self.tools_needed is None:
            self.tools_needed = []

class RecommendationEngine:
    """
    Maps findings to actionable fixes
    Provides step-by-step hardening guidance
    """
    
    def __init__(self):
        self.recommendations_db = self._build_recommendations()
    
    def get_recommendations_for_finding(self, finding: Dict) -> List[Recommendation]:
        """Get recommendations for a specific finding"""
        title = finding.get("title", "").lower()
        severity = finding.get("severity", "LOW")
        
        recommendations = []
        
        # Match finding title to recommendation templates
        for rec_key, rec_template in self.recommendations_db.items():
            if rec_key.lower() in title:
                recommendations.append(rec_template)
        
        # Add general recommendations based on severity
        if not recommendations:
            recommendations.extend(self._generic_recommendations(finding))
        
        return recommendations
    
    def _build_recommendations(self) -> Dict[str, Recommendation]:
        """Build comprehensive recommendation database"""
        return {
            # SSH recommendations
            "ssh_password": Recommendation(
                title="Disable SSH Password Authentication",
                description="Force SSH key-based authentication to prevent brute-force attacks",
                difficulty="EASY",
                impact="HIGH",
                steps=[
                    "Connect to server via SSH or console",
                    "Edit /etc/ssh/sshd_config",
                    "Find line: #PasswordAuthentication yes",
                    "Change to: PasswordAuthentication no",
                    "Find line: #PubkeyAuthentication yes",
                    "Ensure it reads: PubkeyAuthentication yes",
                    "Save file and exit",
                    "Restart SSH service: sudo systemctl restart ssh",
                    "IMPORTANT: Verify SSH key access works BEFORE exiting current session",
                    "Consider setting: PermitRootLogin prohibit-password",
                    "Consider setting: AllowUsers username (restrict users)",
                ],
                tools_needed=["ssh", "nano/vi"],
                estimated_time="15 minutes"
            ),
            
            "ssh_port": Recommendation(
                title="Change SSH Port from Default 22",
                description="Moving SSH to non-standard port reduces automated attacks",
                difficulty="EASY",
                impact="LOW",
                steps=[
                    "Edit /etc/ssh/sshd_config",
                    "Find: #Port 22",
                    "Change to: Port 2222 (or your chosen port > 1024)",
                    "Ensure port is not already in use",
                    "Test with: sudo sshd -t",
                    "Restart SSH: sudo systemctl restart ssh",
                    "Test connection on new port before closing old session",
                    "Update firewall to allow new port",
                    "Document new port for team"
                ],
                tools_needed=["ssh"],
                estimated_time="15 minutes"
            ),
            
            # Database recommendations
            "database_exposure": Recommendation(
                title="Bind Database to Localhost",
                description="Restrict database to internal access only",
                difficulty="MEDIUM",
                impact="CRITICAL",
                steps=[
                    "Stop database service: sudo systemctl stop mysql/postgres",
                    "Edit configuration file:",
                    "  MySQL: /etc/mysql/mysql.conf.d/mysqld.cnf",
                    "  PostgreSQL: /etc/postgresql/*/main/postgresql.conf",
                    "Set bind address to: bind-address = 127.0.0.1",
                    "Save file",
                    "Start database: sudo systemctl start mysql/postgres",
                    "Verify binding: netstat -tlnp | grep mysql",
                    "Test internal connection works",
                    "Update application connection strings if needed"
                ],
                tools_needed=["ssh", "nano/vi"],
                estimated_time="30 minutes"
            ),
            
            "database_auth": Recommendation(
                title="Enable Strong Database Authentication",
                description="Require complex passwords for database access",
                difficulty="MEDIUM",
                impact="HIGH",
                steps=[
                    "Connect to database as root/admin",
                    "Change root password: ALTER USER 'root'@'localhost' IDENTIFIED BY 'StrongPassword123!';",
                    "Delete anonymous accounts: DELETE FROM mysql.user WHERE user='';",
                    "Remove remote root access: DELETE FROM mysql.user WHERE user='root' AND Host!='localhost';",
                    "Flush privileges: FLUSH PRIVILEGES;",
                    "Create application-specific users with limited privileges",
                    "Document passwords securely (password manager)",
                    "Consider using TLS/SSL for connections"
                ],
                tools_needed=["mysql/psql", "password manager"],
                estimated_time="30 minutes"
            ),
            
            # FTP recommendations
            "ftp_insecure": Recommendation(
                title="Replace FTP with SFTP",
                description="FTP transmits credentials in plaintext - use SSH-based SFTP instead",
                difficulty="HARD",
                impact="CRITICAL",
                steps=[
                    "Disable FTP service: sudo systemctl disable vsftpd",
                    "Stop FTP service: sudo systemctl stop vsftpd",
                    "Verify FTP is no longer listening: netstat -tlnp",
                    "For file transfers, use SFTP (port 22) instead",
                    "SSH key management is used for SFTP (already secured)",
                    "For legacy systems, set up SFTP chroot jails:",
                    "  Create dedicated user: sudo useradd -m -s /usr/lib/openssh/sftp-server sftpuser",
                    "  Configure OpenSSH subsystem in sshd_config",
                    "Notify users of FTP→SFTP migration",
                    "Update application configs to use SFTP"
                ],
                tools_needed=["ssh", "system-admin"],
                estimated_time="2-4 hours"
            ),
            
            # Web server recommendations
            "http_unencrypted": Recommendation(
                title="Enable HTTPS (SSL/TLS)",
                description="Encrypt web traffic to prevent interception",
                difficulty="MEDIUM",
                impact="HIGH",
                steps=[
                    "Obtain SSL certificate (free via Let's Encrypt)",
                    "For Let's Encrypt: sudo apt install certbot python3-certbot-apache/nginx",
                    "Generate certificate: sudo certbot certonly --standalone -d example.com",
                    "Configure web server to use certificate",
                    "Apache: Enable SSL module: sudo a2enmod ssl",
                    "Apache: Create/update vhost with SSL directives",
                    "Nginx: Add ssl_certificate and ssl_certificate_key in server block",
                    "Redirect all HTTP to HTTPS",
                    "Test with: https://www.ssllabs.com/ssltest/",
                    "Enable HSTS header: Strict-Transport-Security: max-age=31536000",
                    "Set up auto-renewal: sudo certbot renew --dry-run"
                ],
                tools_needed=["certbot", "apache/nginx"],
                estimated_time="1 hour"
            ),
            
            # Firewall recommendations
            "firewall_missing": Recommendation(
                title="Configure Host-Based Firewall",
                description="Use UFW (Ubuntu) or firewalld to restrict ports",
                difficulty="MEDIUM",
                impact="HIGH",
                steps=[
                    "Check firewall status: sudo ufw status",
                    "If not installed: sudo apt install ufw",
                    "Set default policies:",
                    "  sudo ufw default deny incoming",
                    "  sudo ufw default allow outgoing",
                    "Allow essential services:",
                    "  sudo ufw allow 22/tcp  (SSH)",
                    "  sudo ufw allow 80/tcp  (HTTP)",
                    "  sudo ufw allow 443/tcp (HTTPS)",
                    "Block unnecessary ports automatically",
                    "Enable firewall: sudo ufw enable",
                    "Verify rules: sudo ufw show added",
                    "Test connectivity after enabling"
                ],
                tools_needed=["ufw/firewalld"],
                estimated_time="30 minutes"
            ),
            
            # RDP recommendations
            "rdp_exposed": Recommendation(
                title="Restrict RDP Access",
                description="Limit Remote Desktop Protocol to trusted IPs only",
                difficulty="MEDIUM",
                impact="HIGH",
                steps=[
                    "Open Windows Defender Firewall with Advanced Security",
                    "Go to Inbound Rules",
                    "Find 'Remote Desktop' rule",
                    "Set to 'Allow' only for trusted networks",
                    "Or create new rule limiting to specific IP range",
                    "Consider changing RDP port from 3389 to non-standard port",
                    "Edit Registry: HKLM\\System\\CurrentControlSet\\Control\\Terminal Server",
                    "Modify: PortNumber (default 3389)",
                    "Restart Terminal Services",
                    "Enable Network Level Authentication (NLA)",
                    "Require strong passwords for RDP accounts",
                    "Consider using VPN for remote access instead"
                ],
                tools_needed=["Windows Admin tools"],
                estimated_time="1 hour"
            ),
            
            # General recommendations
            "firewall_general": Recommendation(
                title="Implement Firewall Rules",
                description="Create network ACLs to whitelist traffic",
                difficulty="HARD",
                impact="HIGH",
                steps=[
                    "Document all required ports and services",
                    "Create whitelist of allowed source IPs",
                    "Implement firewall rules:",
                    "  1. Deny all inbound by default",
                    "  2. Allow only required ports from trusted IPs",
                    "  3. Allow all outbound (or restrict as needed)",
                    "Test each service after enabling firewall",
                    "Monitor firewall logs for blocked traffic",
                    "Review rules quarterly for obsolete entries",
                    "Automate firewall management if possible"
                ],
                tools_needed=["Network admin access"],
                estimated_time="4-8 hours"
            ),
            
            "port_closure": Recommendation(
                title="Close Unnecessary Ports",
                description="Disable services that are not actively used",
                difficulty="EASY",
                impact="MEDIUM",
                steps=[
                    "Identify service running on port",
                    "Verify it's not required for production",
                    "Stop service: sudo systemctl stop [service]",
                    "Disable auto-start: sudo systemctl disable [service]",
                    "Verify port is closed: sudo netstat -tlnp",
                    "Document why service was disabled",
                    "Monitor for issues for 24-48 hours",
                    "Plan complete uninstallation if safe"
                ],
                tools_needed=["ssh", "systemctl"],
                estimated_time="15-30 minutes per port"
            ),
            
            "service_update": Recommendation(
                title="Update Service Software",
                description="Install latest security patches",
                difficulty="MEDIUM",
                impact="HIGH",
                steps=[
                    "Plan maintenance window",
                    "Backup configuration files",
                    "Test update in staging environment first",
                    "Ubuntu/Debian: sudo apt update && sudo apt upgrade [package]",
                    "CentOS/RHEL: sudo yum update [package]",
                    "Windows: Check Windows Update / vendor updates",
                    "Verify service restarts successfully",
                    "Run security scan again to confirm fix",
                    "Monitor logs for any issues post-update",
                    "Document update in change log"
                ],
                tools_needed=["package manager", "root access"],
                estimated_time="1-2 hours"
            ),
        }
    
    def _generic_recommendations(self, finding: Dict) -> List[Recommendation]:
        """Generate generic recommendations for unknown findings"""
        severity = finding.get("severity", "LOW")
        
        generic_recs = []
        
        if severity in ["CRITICAL", "HIGH"]:
            generic_recs.append(Recommendation(
                title="Immediate Mitigation Required",
                description="This finding requires urgent attention",
                difficulty="HARD",
                impact=severity,
                steps=[
                    "Contact system administrator immediately",
                    "Assess business impact of the vulnerability",
                    "Determine if system should remain in production",
                    "Plan mitigation steps based on recommendations",
                    "Implement safeguards (firewall, ACLs) as temporary measure",
                    "Schedule permanent fix with change management",
                    "Monitor for exploitation attempts"
                ],
                estimated_time="Varies"
            ))
        
        return generic_recs
    
    def get_all_recommendations(self) -> List[Recommendation]:
        """Get all available recommendations"""
        return list(self.recommendations_db.values())
    
    def categorize_recommendations(self, recommendations: List[Recommendation]) -> Dict[str, List[Recommendation]]:
        """Group recommendations by difficulty"""
        categorized = {
            "EASY": [],
            "MEDIUM": [],
            "HARD": []
        }
        
        for rec in recommendations:
            difficulty = rec.difficulty
            if difficulty in categorized:
                categorized[difficulty].append(rec)
        
        return categorized
