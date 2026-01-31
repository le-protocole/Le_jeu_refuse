"""
Nmap Scanner Wrapper
Purpose: Execute nmap scans safely and parse results
Includes Python socket fallback for systems without Nmap
"""

import subprocess
import json
import re
import socket
from typing import List, Dict, Optional
from datetime import datetime
import xml.etree.ElementTree as ET
import os
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

class NmapScanner:
    """
    Wrapper around nmap CLI tool
    Executes scans and parses results
    Falls back to Python socket scanning if Nmap unavailable
    """
    
    # Common ports database
    COMMON_PORTS = {
        20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
        53: "dns", 80: "http", 110: "pop3", 143: "imap", 443: "https",
        445: "smb", 465: "smtp-ssl", 587: "smtp", 993: "imaps", 995: "pop3s",
        1433: "mssql", 3306: "mysql", 3389: "rdp", 5432: "postgresql",
        5900: "vnc", 6379: "redis", 8000: "http-alt", 8080: "http-proxy",
        8443: "https-alt", 9200: "elasticsearch", 27017: "mongodb"
    }
    
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.nmap_bin = self._find_nmap()
        self.nmap_available = self.nmap_bin is not None
    
    def _find_nmap(self) -> Optional[str]:
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
        
        # Try generic command
        if self._check_nmap("nmap"):
            return "nmap"
        
        return None
    
    def _check_nmap(self, path: str) -> bool:
        """Check if nmap is available at path"""
        try:
            subprocess.run(
                [path, "-V"],
                capture_output=True,
                timeout=5
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return False
    
    def quick_scan(self, target: str) -> Dict:
        """Quick scan of common ports - uses Nmap or Python fallback"""
        if self.nmap_available:
            ports = "22,80,443,3306,5432,5900,8080,8443"
            args = [
                self.nmap_bin,
                "-Pn", "-sS", "-T4",
                f"-p{ports}",
                "--script", "banner",
                "-oX", "-",
                target
            ]
            return self._run_scan(args, target, "quick")
        else:
            return self._python_quick_scan(target)
    
    def standard_scan(self, target: str) -> Dict:
        """Standard scan - uses Nmap or Python fallback"""
        if self.nmap_available:
            args = [
                self.nmap_bin,
                "-Pn", "-sV", "-T3",
                "-p", "1-10000",
                "-oX", "-",
                target
            ]
            return self._run_scan(args, target, "standard")
        else:
            return self._python_standard_scan(target)
    
    def thorough_scan(self, target: str) -> Dict:
        """Thorough scan - uses Nmap or Python fallback"""
        if self.nmap_available:
            args = [
                self.nmap_bin,
                "-Pn", "-sV", "-O", "-A", "-T2",
                "-p-",
                "-oX", "-",
                target
            ]
            return self._run_scan(args, target, "thorough")
        else:
            return self._python_standard_scan(target)
    
    def _run_scan(self, args: List[str], target: str, scan_type: str) -> Dict:
        """Execute nmap and parse XML output with error handling"""
        
        result = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "os_detection": [],
            "method": "nmap",
            "error": None
        }
        
        try:
            # Execute scan with better timeout handling
            process = subprocess.run(
                args,
                capture_output=True,
                timeout=self.timeout,
                text=True
            )
            
            if process.returncode != 0:
                if "No targets were specified" not in process.stderr:
                    # Try fallback if Nmap fails
                    return self._python_quick_scan(target, scan_type)
            
            # Parse XML output
            if process.stdout:
                result = self._parse_nmap_xml(process.stdout, result)
            else:
                # Fallback if no output
                return self._python_quick_scan(target, scan_type)
            
        except subprocess.TimeoutExpired:
            # Use fallback on timeout
            return self._python_quick_scan(target, scan_type)
        except Exception as e:
            # Use fallback on any error
            return self._python_quick_scan(target, scan_type)
        
        return result
    
    def _python_quick_scan(self, target: str, scan_type: str = "quick") -> Dict:
        """Pure Python socket scan - fallback when Nmap unavailable"""
        result = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "method": "python-socket",
            "error": None
        }
        
        # Resolve hostname
        try:
            ip = socket.gethostbyname(target)
            result["ip_address"] = ip
        except socket.gaierror:
            result["error"] = f"Cannot resolve hostname: {target}"
            return result
        
        # Scan common ports
        ports = [22, 80, 443, 3306, 5432, 5900, 8080, 8443, 21, 25, 53, 110, 143, 445]
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in ports}
            
            for future in as_completed(futures):
                port = futures[future]
                try:
                    is_open = future.result()
                    port_info = {
                        "port": port,
                        "protocol": "tcp",
                        "state": "open" if is_open else "closed",
                        "service": self.COMMON_PORTS.get(port, "unknown"),
                        "version": "",
                        "extrainfo": ""
                    }
                    
                    if is_open:
                        result["open_ports"].append(port_info)
                    else:
                        result["closed_ports"].append(port_info)
                except:
                    pass
        
        return result
    
    def _python_standard_scan(self, target: str) -> Dict:
        """Python socket scan for standard ports"""
        result = {
            "target": target,
            "scan_type": "standard",
            "timestamp": datetime.now().isoformat(),
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "method": "python-socket",
            "error": None
        }
        
        # Resolve hostname
        try:
            ip = socket.gethostbyname(target)
            result["ip_address"] = ip
        except socket.gaierror:
            result["error"] = f"Cannot resolve hostname: {target}"
            return result
        
        # Scan all common ports
        ports = list(self.COMMON_PORTS.keys())
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in ports}
            
            for future in as_completed(futures):
                port = futures[future]
                try:
                    is_open = future.result()
                    port_info = {
                        "port": port,
                        "protocol": "tcp",
                        "state": "open" if is_open else "closed",
                        "service": self.COMMON_PORTS.get(port, "unknown"),
                        "version": "",
                        "extrainfo": ""
                    }
                    
                    if is_open:
                        result["open_ports"].append(port_info)
                    else:
                        result["closed_ports"].append(port_info)
                except:
                    pass
        
        # Sort by port number
        result["open_ports"] = sorted(result["open_ports"], key=lambda x: x["port"])
        result["closed_ports"] = sorted(result["closed_ports"], key=lambda x: x["port"])
        
        return result
    
    def _check_port(self, host: str, port: int, timeout: int = 2) -> bool:
        """Check if a single port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _parse_nmap_xml(self, xml_output: str, result: Dict) -> Dict:
        """Parse nmap XML output with robust error handling"""
        try:
            root = ET.fromstring(xml_output)
            
            # Parse host information
            for host in root.findall(".//host"):
                # Get host status
                status = host.find(".//status")
                if status is not None and status.get("state") != "up":
                    result["error"] = "Host is down or unreachable"
                    continue
                
                # Get IP address
                address = host.find(".//address[@addrtype='ipv4']")
                if address is not None:
                    result["ip_address"] = address.get("addr")
                
                # Parse ports
                for port in host.findall(".//port"):
                    try:
                        port_id = port.get("portid")
                        protocol = port.get("protocol")
                        
                        if not port_id:
                            continue
                        
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
                    except (ValueError, AttributeError):
                        continue
                
                # Parse OS detection
                for osmatch in host.findall(".//osmatch"):
                    try:
                        os_data = {
                            "name": osmatch.get("name"),
                            "accuracy": osmatch.get("accuracy")
                        }
                        result["os_detection"].append(os_data)
                    except:
                        continue
        
        except ET.ParseError as e:
            # On parse error, use fallback
            result["error"] = f"XML parse error, using fallback"
            result["method"] = "python-socket (fallback)"
        except Exception as e:
            result["error"] = f"Parse error: {str(e)}"
        
        return result


# Example usage
if __name__ == "__main__":
    scanner = NmapScanner()
    
    # Test scan
    print("Testing quick scan on localhost...")
    result = scanner.quick_scan("127.0.0.1")
    
    print(json.dumps(result, indent=2))
