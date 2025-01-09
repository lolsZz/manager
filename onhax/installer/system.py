"""
System-level operations for Dify installer.
"""
import os
import subprocess
import platform
import shutil
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class SystemPackageManager:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.package_manager = self._detect_package_manager()

    def _detect_package_manager(self) -> str:
        """Detect the system package manager."""
        if self.os_type == "linux":
            # Check for apt (Debian/Ubuntu)
            if shutil.which("apt"):
                return "apt"
            # Check for dnf (Fedora)
            elif shutil.which("dnf"):
                return "dnf"
            # Check for yum (CentOS/RHEL)
            elif shutil.which("yum"):
                return "yum"
        elif self.os_type == "darwin":
            if shutil.which("brew"):
                return "brew"
        return "unknown"

    def _run_command(self, cmd: List[str], sudo: bool = False) -> bool:
        """Run a system command."""
        try:
            if sudo and os.geteuid() != 0:
                cmd = ["sudo"] + cmd
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"Error: {str(e)}")
            return False

    def install_package(self, package: str, sudo: bool = True) -> bool:
        """Install a system package."""
        if self.package_manager == "apt":
            return self._run_command(["apt-get", "install", "-y", package], sudo)
        elif self.package_manager == "dnf":
            return self._run_command(["dnf", "install", "-y", package], sudo)
        elif self.package_manager == "yum":
            return self._run_command(["yum", "install", "-y", package], sudo)
        elif self.package_manager == "brew":
            return self._run_command(["brew", "install", package], False)
        return False

    def update_package_list(self, sudo: bool = True) -> bool:
        """Update package list."""
        if self.package_manager == "apt":
            return self._run_command(["apt-get", "update"], sudo)
        elif self.package_manager == "dnf":
            return self._run_command(["dnf", "check-update"], sudo)
        elif self.package_manager == "yum":
            return self._run_command(["yum", "check-update"], sudo)
        elif self.package_manager == "brew":
            return self._run_command(["brew", "update"], False)
        return False

    def install_docker(self) -> bool:
        """Install Docker if not present."""
        if shutil.which("docker"):
            return True
        
        if self.package_manager == "apt":
            commands = [
                ["apt-get", "update"],
                ["apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl", "software-properties-common"],
                ["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "|", "sudo", "apt-key", "add", "-"],
                ["add-apt-repository", "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"],
                ["apt-get", "update"],
                ["apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"]
            ]
            for cmd in commands:
                if not self._run_command(cmd, True):
                    return False
            return True
        
        elif self.package_manager in ["dnf", "yum"]:
            commands = [
                ["yum", "install", "-y", "yum-utils"],
                ["yum-config-manager", "--add-repo", "https://download.docker.com/linux/centos/docker-ce.repo"],
                [self.package_manager, "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"]
            ]
            for cmd in commands:
                if not self._run_command(cmd, True):
                    return False
            return True
        
        elif self.package_manager == "brew":
            return self._run_command(["brew", "install", "--cask", "docker"], False)
        
        return False

    def install_nodejs(self, version: str = "16") -> bool:
        """Install Node.js if not present."""
        if shutil.which("node"):
            return True

        if self.package_manager == "apt":
            commands = [
                ["curl", "-fsSL", f"https://deb.nodesource.com/setup_{version}.x", "|", "sudo", "-E", "bash", "-"],
                ["apt-get", "install", "-y", "nodejs"]
            ]
            for cmd in commands:
                if not self._run_command(cmd, True):
                    return False
            return True
        
        elif self.package_manager in ["dnf", "yum"]:
            commands = [
                ["curl", "-fsSL", f"https://rpm.nodesource.com/setup_{version}.x", "|", "sudo", "-E", "bash", "-"],
                [self.package_manager, "install", "-y", "nodejs"]
            ]
            for cmd in commands:
                if not self._run_command(cmd, True):
                    return False
            return True
        
        elif self.package_manager == "brew":
            return self._run_command(["brew", "install", "node@16"], False)
        
        return False

    def start_service(self, service: str) -> bool:
        """Start a system service."""
        if self.os_type == "linux":
            return self._run_command(["systemctl", "start", service], True)
        elif self.os_type == "darwin" and self.package_manager == "brew":
            return self._run_command(["brew", "services", "start", service], False)
        return False

    def enable_service(self, service: str) -> bool:
        """Enable a system service to start on boot."""
        if self.os_type == "linux":
            return self._run_command(["systemctl", "enable", service], True)
        elif self.os_type == "darwin" and self.package_manager == "brew":
            return self._run_command(["brew", "services", "start", service], False)
        return False

system_manager = SystemPackageManager()