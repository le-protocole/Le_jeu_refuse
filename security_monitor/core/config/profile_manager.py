"""
Scan Profiles - Custom Scan Configuration Templates
Allows users to create and save custom scan profiles for different scenarios
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ScanProfile:
    """Represents a scan profile configuration"""
    name: str
    description: str
    enabled_modules: List[str]
    port_range: str
    timeout: int
    deep_scan: bool
    check_ssl: bool
    check_headers: bool
    check_cloud: bool
    check_tech: bool
    check_geo: bool
    created_at: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class ProfileManager:
    """Manage scan profiles"""
    
    # Predefined profiles
    PROFILES = {
        "quick": {
            "name": "Quick Scan",
            "description": "Fast basic vulnerability scan (5 modules)",
            "enabled_modules": ["dns", "scanner", "ssl", "headers", "tech"],
            "port_range": "80,443,8080",
            "timeout": 30,
            "deep_scan": False,
            "check_ssl": True,
            "check_headers": True,
            "check_cloud": False,
            "check_tech": True,
            "check_geo": False,
            "tags": ["fast", "basic"]
        },
        "standard": {
            "name": "Standard Scan",
            "description": "Complete security assessment (8 modules)",
            "enabled_modules": ["dns", "scanner", "analysis", "ssl", "headers", "cloud", "tech", "geo"],
            "port_range": "1-65535",
            "timeout": 120,
            "deep_scan": True,
            "check_ssl": True,
            "check_headers": True,
            "check_cloud": True,
            "check_tech": True,
            "check_geo": True,
            "tags": ["comprehensive", "default"]
        },
        "pci_dss": {
            "name": "PCI-DSS Compliance",
            "description": "Scan for PCI-DSS compliance requirements (SSL, encryption)",
            "enabled_modules": ["dns", "scanner", "ssl", "headers", "tech", "compliance"],
            "port_range": "443,8443",
            "timeout": 90,
            "deep_scan": True,
            "check_ssl": True,
            "check_headers": True,
            "check_cloud": False,
            "check_tech": True,
            "check_geo": False,
            "tags": ["compliance", "pci", "encryption"]
        },
        "owasp": {
            "name": "OWASP Top 10",
            "description": "Check for OWASP Top 10 vulnerabilities",
            "enabled_modules": ["dns", "scanner", "headers", "analysis", "tech", "compliance"],
            "port_range": "80,443",
            "timeout": 100,
            "deep_scan": True,
            "check_ssl": True,
            "check_headers": True,
            "check_cloud": False,
            "check_tech": True,
            "check_geo": False,
            "tags": ["owasp", "web", "vulnerabilities"]
        },
        "infrastructure": {
            "name": "Infrastructure Assessment",
            "description": "Deep infrastructure and cloud analysis",
            "enabled_modules": ["dns", "scanner", "cloud", "geo", "tech", "analysis"],
            "port_range": "1-10000",
            "timeout": 150,
            "deep_scan": True,
            "check_ssl": True,
            "check_headers": False,
            "check_cloud": True,
            "check_tech": True,
            "check_geo": True,
            "tags": ["infrastructure", "cloud", "network"]
        },
        "api_security": {
            "name": "API Security Scan",
            "description": "Scan for API vulnerabilities and misconfigurations",
            "enabled_modules": ["dns", "scanner", "headers", "ssl", "analysis"],
            "port_range": "80,443,8000,8080,8443",
            "timeout": 120,
            "deep_scan": True,
            "check_ssl": True,
            "check_headers": True,
            "check_cloud": False,
            "check_tech": True,
            "check_geo": False,
            "tags": ["api", "rest", "security"]
        }
    }
    
    def __init__(self, profiles_dir: str = "profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
    
    def get_predefined_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all predefined profiles"""
        return self.PROFILES
    
    def get_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific profile by name"""
        # Check custom profiles first
        custom_file = self.profiles_dir / f"{profile_name}.json"
        if custom_file.exists():
            try:
                with open(custom_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Check predefined profiles
        if profile_name in self.PROFILES:
            return self.PROFILES[profile_name]
        
        return None
    
    def create_custom_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Create a custom profile"""
        try:
            profile_name = profile_data.get("name", "custom_profile").replace(" ", "_").lower()
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            # Add creation timestamp if not present
            if "created_at" not in profile_data:
                from datetime import datetime
                profile_data["created_at"] = datetime.now().isoformat()
            
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            return True
        except Exception as e:
            return False
    
    def delete_custom_profile(self, profile_name: str) -> bool:
        """Delete a custom profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            if profile_file.exists():
                profile_file.unlink()
                return True
        except:
            pass
        return False
    
    def list_custom_profiles(self) -> List[str]:
        """List all custom profiles"""
        profiles = []
        for file in self.profiles_dir.glob("*.json"):
            profiles.append(file.stem)
        return profiles
    
    def list_all_profiles(self) -> Dict[str, List[str]]:
        """List both predefined and custom profiles"""
        return {
            "predefined": list(self.PROFILES.keys()),
            "custom": self.list_custom_profiles()
        }
    
    def export_profile(self, profile_name: str, export_path: str = None) -> Optional[str]:
        """Export a profile to file"""
        profile = self.get_profile(profile_name)
        if not profile:
            return None
        
        if not export_path:
            export_path = f"exported_{profile_name}.json"
        
        try:
            with open(export_path, 'w') as f:
                json.dump(profile, f, indent=2)
            return export_path
        except:
            return None
    
    def import_profile(self, import_path: str) -> bool:
        """Import a profile from file"""
        try:
            with open(import_path, 'r') as f:
                profile_data = json.load(f)
            return self.create_custom_profile(profile_data)
        except:
            return False
    
    def get_profile_by_tag(self, tag: str) -> Dict[str, Dict[str, Any]]:
        """Get all profiles with a specific tag"""
        matching_profiles = {}
        
        # Check predefined profiles
        for name, profile in self.PROFILES.items():
            if tag in profile.get("tags", []):
                matching_profiles[name] = profile
        
        # Check custom profiles
        for custom_name in self.list_custom_profiles():
            profile = self.get_profile(custom_name)
            if profile and tag in profile.get("tags", []):
                matching_profiles[custom_name] = profile
        
        return matching_profiles
    
    def modify_profile(self, profile_name: str, updates: Dict[str, Any]) -> bool:
        """Modify an existing custom profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return False
        
        # Can only modify custom profiles
        if profile_name not in self.PROFILES:
            profile.update(updates)
            return self.create_custom_profile(profile)
        
        return False
    
    def get_profile_summary(self, profile_name: str) -> Optional[str]:
        """Get a human-readable summary of a profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return None
        
        summary = f"""
        Profile: {profile.get('name')}
        Description: {profile.get('description')}
        Enabled Modules: {', '.join(profile.get('enabled_modules', []))}
        Port Range: {profile.get('port_range')}
        Timeout: {profile.get('timeout')}s
        Deep Scan: {'Yes' if profile.get('deep_scan') else 'No'}
        SSL Check: {'Yes' if profile.get('check_ssl') else 'No'}
        Headers Check: {'Yes' if profile.get('check_headers') else 'No'}
        Cloud Check: {'Yes' if profile.get('check_cloud') else 'No'}
        Tech Stack: {'Yes' if profile.get('check_tech') else 'No'}
        Geolocation: {'Yes' if profile.get('check_geo') else 'No'}
        Tags: {', '.join(profile.get('tags', []))}
        """
        
        return summary.strip()


def get_profile(profile_name: str) -> Optional[Dict[str, Any]]:
    """Quick function to get a profile"""
    manager = ProfileManager()
    return manager.get_profile(profile_name)


def list_profiles() -> Dict[str, List[str]]:
    """Quick function to list all profiles"""
    manager = ProfileManager()
    return manager.list_all_profiles()
