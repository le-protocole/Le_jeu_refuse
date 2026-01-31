"""
Nmap Scanner Wrapper
Purpose: Execute nmap scans safely and parse results
"""

import subprocess
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
import xml.etree.ElementTree as ET
import os
import platform

class NmapScanner:
    """
    Wrapper around nmap CLI tool
    Executes scans and parses results
    """
    
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.nmap_bin = self._find_nmap()
    
    def _find_nmap(self) -> str:
        """Find nmap binary in system PATH"""
        system = platform.system()
        
        if system == "Windows":
            # Common Windows nmap paths
            possible_paths = [
                "C:\\Program Files\\Nmap\\nmap.exe",
                "C:\\Program Files (x86)\\Nmap\\nmap.exe",
                "nmap.exe"
            ]
        else:
            possible_paths = ["/usr/bin/nmap", "/usr/local/bin/nmap", "nmap"]
        
        for path in possible_paths:
            if self._check_nmap(path):
                return path
        
        return "nmap"  # Fallback to PATH
    
    def _check_nmap(self, path: str) -> bool:
        """Check if nmap is available at path"""
        try:
            subprocess.run(
                [path, "-V"],
                capture_output=True,
                timeout=5
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def quick_scan(self, target: str) -> Dict:
        """
        Quick scan of common ports
        nmap -Pn -sS -T4 -p 22,80,443,3306,5432,8080,8443
        """
        ports = "22,80,443,3306,5432,5900,8080,8443"
        args = [
            self.nmap_bin,
            "-Pn",          # Skip ping
            "-sS",          # TCP SYN scan
            "-T4",          # Timing template (aggressive)
            f"-p{ports}",   # Specific ports
            "--script", "banner",  # Banner grabbing
            "-oX", "-",     # XML output to stdout
            target
        ]
        
        return self._run_scan(args, target, "quick")
    
    def standard_scan(self, target: str) -> Dict:
        """
        Standard scan - common ports + service version detection
        nmap -Pn -sV -T3 -p 1-10000
        """
        args = [
            self.nmap_bin,
            "-Pn",          # Skip ping
            "-sV",          # Version detection
            "-T3",          # Timing (normal)
            "-p", "1-10000",  # Top 10k ports
            "-oX", "-",
            target
        ]
        
        return self._run_scan(args, target, "standard")
    
    def thorough_scan(self, target: str) -> Dict:
        """
        Thorough scan - all ports + OS detection + script scanning
        nmap -Pn -sV -O -A --script vuln -T2 -p-
        """
        args = [
            self.nmap_bin,
            "-Pn",
            "-sV",          # Version detection
            "-O",           # OS detection
            "-A",           # Aggressive options
            "-T2",          # Timing (sneaky)
            "-p-",          # All ports
            "-oX", "-",
            target
        ]
        
        return self._run_scan(args, target, "thorough")
    
    def _run_scan(self, args: List[str], target: str, scan_type: str) -> Dict:
        """Execute nmap and parse XML output"""
        
        result = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "os_detection": [],
            "error": None
        }
        
        try:
            # Execute scan
            process = subprocess.run(
                args,
                capture_output=True,
                timeout=self.timeout,
                text=True
            )
            
            if process.returncode != 0 and "No targets were specified" not in process.stderr:
                result["error"] = f"Nmap error: {process.stderr}"
                return result
            
            # Parse XML output
            if process.stdout:
                result = self._parse_nmap_xml(process.stdout, result)
            
        except subprocess.TimeoutExpired:
            result["error"] = f"Scan timeout (>{self.timeout}s)"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _parse_nmap_xml(self, xml_output: str, result: Dict) -> Dict:
        """Parse nmap XML output"""
        try:
            root = ET.fromstring(xml_output)
            
            # Parse host information
            for host in root.findall(".//host"):
                # Get host status
                status = host.find(".//status")
                if status is not None and status.get("state") != "up":
                    result["error"] = "Host is down or unreachable"
                    continue
                
                # Parse ports
                for port in host.findall(".//port"):
                    port_id = port.get("portid")
                    protocol = port.get("protocol")
                    
                    # Port state
                    port_state = port.find(".//state")
                    state = port_state.get("state") if port_state is not None else "unknown"
                    
                    # Service information
                    service_info = port.find(".//service")
                    service_name = service_info.get("name") if service_info is not None else "unknown"
                    service_version = service_info.get("version") if service_info is not None else ""
                    service_extrainfo = service_info.get("extrainfo") if service_info is not None else ""
                    
                    port_data = {
                        "port": int(port_id),
                        "protocol": protocol,
                        "state": state,
                        "service": service_name,
                        "version": service_version,
                        "extrainfo": service_extrainfo
                    }
                    
                    if state == "open":
                        result["open_ports"].append(port_data)
                    elif state == "filtered":
                        result["filtered_ports"].append(port_data)
                    elif state == "closed":
                        result["closed_ports"].append(port_data)
                
                # Parse OS detection
                for osmatch in host.findall(".//osmatch"):
                    os_data = {
                        "name": osmatch.get("name"),
                        "accuracy": osmatch.get("accuracy")
                    }
                    result["os_detection"].append(os_data)
        
        except ET.ParseError as e:
            result["error"] = f"XML parse error: {str(e)}"
        
        return result


# Example usage
if __name__ == "__main__":
    scanner = NmapScanner()
    
    # Test scan
    print("Testing quick scan on localhost...")
    result = scanner.quick_scan("127.0.0.1")
    
    print(json.dumps(result, indent=2))
