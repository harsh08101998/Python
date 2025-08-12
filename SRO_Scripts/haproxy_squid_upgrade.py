#!/usr/bin/env python3
"""
HAProxy and Squid Upgrade Automation Script
Author: Automation Team
Description: Automates the upgrade process for HAProxy 2.4.2 and Squid 3.5.28 on CentOS 7
"""

import subprocess
import os
import time
import logging
import sys
from datetime import datetime
import json

class HAProxySquidUpgrade:
    def __init__(self, target_server=None, ssh_port=22000):
        """Initialize the upgrade automation"""
        self.target_server = target_server
        self.ssh_port = ssh_port
        self.log_file = f"haproxy_squid_upgrade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.setup_logging()
        
        # Version information
        self.haproxy_version = "2.4.2"
        self.squid_version = "3.5.28"
        self.expected_haproxy_version = "2.4.2-553dee3 2021/07/07"
        
        # URLs for downloads
        self.haproxy_url = "https://www.haproxy.org/download/2.4/src/haproxy-2.4.2.tar.gz"
        self.squid_url = "http://www.squid-cache.org/Versions/v3/3.5/squid-3.5.28.tar.gz"
        
        # Configuration server details
        self.config_server = "0495-5.exotel.in"
        self.config_user = "asterisk"  # Change to root if needed
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_command(self, command, check_return_code=True, timeout=300):
        """Execute shell command with proper error handling"""
        self.logger.info(f"Executing: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if check_return_code and result.returncode != 0:
                self.logger.error(f"Command failed: {command}")
                self.logger.error(f"Error output: {result.stderr}")
                return False, result.stderr
            
            self.logger.info(f"Command output: {result.stdout}")
            return True, result.stdout
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return False, "Command timed out"
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return False, str(e)

    def run_remote_command(self, command, server=None):
        """Execute command on remote server via SSH"""
        if not server:
            server = self.target_server
            
        if not server:
            self.logger.error("No target server specified")
            return False, "No target server specified"
            
        ssh_command = f"ssh -p {self.ssh_port} root@{server} '{command}'"
        return self.run_command(ssh_command)

    def backup_existing_binaries(self):
        """Backup existing HAProxy and Squid binaries"""
        self.logger.info("Backing up existing binaries...")
        
        # Backup HAProxy
        success, output = self.run_command("sudo cp /usr/sbin/haproxy /tmp/haproxy_backup")
        if not success:
            self.logger.error("Failed to backup HAProxy")
            return False
            
        # Backup Squid
        success, output = self.run_command("sudo cp /usr/sbin/squid /tmp/squid_backup")
        if not success:
            self.logger.error("Failed to backup Squid")
            return False
            
        self.logger.info("Binaries backed up successfully")
        return True

    def check_current_versions(self):
        """Check current versions of HAProxy and Squid"""
        self.logger.info("Checking current versions...")
        
        # Check HAProxy version
        success, haproxy_version = self.run_command("haproxy -v", check_return_code=False)
        if success:
            self.logger.info(f"Current HAProxy version: {haproxy_version}")
        
        # Check Squid version
        success, squid_version = self.run_command("squid -v", check_return_code=False)
        if success:
            self.logger.info(f"Current Squid version: {squid_version}")

    def upgrade_haproxy(self):
        """Upgrade HAProxy to version 2.4.2"""
        self.logger.info("Starting HAProxy upgrade...")
        
        try:
            # Switch to root user and change to /tmp
            commands = [
                "sudo su -",
                "cd /tmp",
                f"wget {self.haproxy_url}",
                f"tar -xzf haproxy-{self.haproxy_version}.tar.gz",
                f"cd haproxy-{self.haproxy_version}",
                'make TARGET=linux-glibc USE_NS= EXTRA_OBJS="addons/promex/service-prometheus.o"',
                "sudo service haproxy stop",
                "make install",
                "sudo service haproxy stop",
                "sleep 1",
                "sudo rm -rf /usr/sbin/haproxy",
                "sudo cp /usr/local/sbin/haproxy /usr/sbin/haproxy",
                f"rm -rf /tmp/haproxy-{self.haproxy_version}.tar.gz",
                f"rm -rf /tmp/haproxy-{self.haproxy_version}"
            ]
            
            # Execute upgrade commands
            upgrade_command = " && ".join(commands)
            success, output = self.run_command(upgrade_command, timeout=600)
            
            if not success:
                self.logger.error("HAProxy upgrade failed")
                return False
                
            # Verify installation
            success, version_output = self.run_command("haproxy -v")
            if success and self.expected_haproxy_version in version_output:
                self.logger.info(f"HAProxy upgraded successfully to {self.haproxy_version}")
                return True
            else:
                self.logger.error("HAProxy version verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"HAProxy upgrade failed: {e}")
            return False

    def upgrade_squid(self):
        """Upgrade Squid to version 3.5.28"""
        self.logger.info("Starting Squid upgrade...")
        
        try:
            # Install dependencies first
            dependency_commands = [
                "sudo yum install openldap-devel.x86_64 -y",
                "sudo yum install pam-devel.x86_64 -y"
            ]
            
            for cmd in dependency_commands:
                success, output = self.run_command(cmd, timeout=300)
                if not success:
                    self.logger.error(f"Failed to install dependency: {cmd}")
                    return False
            
            # Squid upgrade commands
            configure_options = [
                '"--build=x86_64-redhat-linux-gnu"',
                '"--host=x86_64-redhat-linux-gnu"',
                '"--target=x86_64-redhat-linux-gnu"',
                '"--program-prefix="',
                '"--prefix=/usr"',
                '"--exec-prefix=/usr"',
                '"--bindir=/usr/bin"',
                '"--sbindir=/usr/sbin"',
                '"--sysconfdir=/etc"',
                '"--datadir=/usr/share"',
                '"--includedir=/usr/include"',
                '"--libdir=/usr/lib64"',
                '"--libexecdir=/usr/libexec"',
                '"--sharedstatedir=/var/lib"',
                '"--mandir=/usr/share/man"',
                '"--infodir=/usr/share/info"',
                '"--enable-internal-dns"',
                '"--disable-strict-error-checking"',
                '"--exec_prefix=/usr"',
                '"--libexecdir=/usr/lib64/squid"',
                '"--localstatedir=/var"',
                '"--datadir=/usr/share/squid"',
                '"--sysconfdir=/etc/squid"',
                '"--with-logdir=/var/log/squid"',
                '"--with-pidfile=/var/run/squid.pid"',
                '"--disable-dependency-tracking"',
                '"--enable-arp-acl"',
                '"--enable-follow-x-forwarded-for"',
                '"--enable-auth"',
                '"--enable-auth-basic=LDAP,MSNT-multi-domain,NCSA,PAM,SMB,getpwnam,SASL,DB,POP3,RADIUS"',
                '"--enable-auth-ntlm=smb_lm,fake"',
                '"--enable-auth-digest=LDAP,eDirectory"',
                '"--enable-auth-negotiate=kerberos"',
                '"--enable-external-acl-helpers=LDAP_group,session,unix_group,wbinfo_group"',
                '"--enable-cache-digests"',
                '"--enable-cachemgr-hostname=localhost"',
                '"--enable-delay-pools"',
                '"--enable-epoll"',
                '"--enable-icap-client"',
                '"--enable-ident-lookups"',
                '"--enable-linux-netfilter"',
                '"--enable-referer-log"',
                '"--enable-removal-policies=heap,lru"',
                '"--enable-snmp"',
                '"--enable-ssl"',
                '"--with-included-ltdl"',
                '"--enable-storeio=aufs,diskd,ufs"',
                '"--enable-useragent-log"',
                '"--enable-wccpv2"',
                '"--enable-esi"',
                '"--enable-http-violations"',
                '"--with-aio"',
                '"--with-default-user=squid"',
                '"--with-filedescriptors=16384"',
                '"--with-dl"',
                '"--with-openssl"',
                '"--with-pthreads"',
                '"build_alias=x86_64-redhat-linux-gnu"',
                '"host_alias=x86_64-redhat-linux-gnu"',
                '"target_alias=x86_64-redhat-linux-gnu"',
                '"CFLAGS=-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -fpie"',
                '"LDFLAGS=-pie"',
                '"CXXFLAGS=-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -fpie"'
            ]
            
            commands = [
                "sudo su -",
                "cd /home/asterisk",
                "cd /tmp",
                f"wget {self.squid_url}",
                f"tar -xzf squid-{self.squid_version}.tar.gz",
                f"cd squid-{self.squid_version}",
                f"./configure {' '.join(configure_options)}",
                "make",
                "make install"
            ]
            
            # Execute upgrade commands
            upgrade_command = " && ".join(commands)
            success, output = self.run_command(upgrade_command, timeout=1800)  # 30 minutes timeout
            
            if not success:
                self.logger.error("Squid upgrade failed")
                return False
                
            # Verify installation
            success, version_output = self.run_command("squid -v")
            if success and self.squid_version in version_output:
                self.logger.info(f"Squid upgraded successfully to {self.squid_version}")
                return True
            else:
                self.logger.error("Squid version verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Squid upgrade failed: {e}")
            return False

    def copy_configurations_from_server(self):
        """Copy latest configuration files from 0495-5 server"""
        self.logger.info("Copying configuration files from 0495-5 server...")
        
        try:
            # Copy configuration files
            copy_command = f"scp -P {self.ssh_port} -r {self.config_user}@{self.config_server}:/tmp/netconf_new* ."
            success, output = self.run_command(copy_command)
            
            if not success:
                self.logger.error("Failed to copy configuration files")
                return False
                
            self.logger.info("Configuration files copied successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to copy configurations: {e}")
            return False

    def push_configurations_to_target(self):
        """Push configuration files to target server"""
        if not self.target_server:
            self.logger.error("No target server specified")
            return False
            
        self.logger.info(f"Pushing configuration files to {self.target_server}...")
        
        try:
            push_command = f"sudo scp -P {self.ssh_port} -r netconf_new* root@{self.target_server}:/tmp/"
            success, output = self.run_command(push_command)
            
            if not success:
                self.logger.error("Failed to push configuration files")
                return False
                
            self.logger.info("Configuration files pushed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to push configurations: {e}")
            return False

    def configure_haproxy(self):
        """Generate and configure HAProxy"""
        self.logger.info("Configuring HAProxy...")
        
        try:
            if self.target_server:
                # Remote configuration
                commands = [
                    "cd /tmp/netconf_new/haproxyTools",
                    "sudo php -f haproxyConfigGenerator.php",
                    "sudo cp haproxy.cfg /etc/haproxy/",
                    "sudo service haproxy restart"
                ]
                
                for cmd in commands:
                    success, output = self.run_remote_command(cmd)
                    if not success:
                        self.logger.error(f"Failed to execute: {cmd}")
                        return False
            else:
                # Local configuration
                commands = [
                    "cd /tmp/netconf_new/haproxyTools",
                    "sudo php -f haproxyConfigGenerator.php",
                    "sudo cp haproxy.cfg /etc/haproxy/",
                    "sudo service haproxy restart"
                ]
                
                for cmd in commands:
                    success, output = self.run_command(cmd)
                    if not success:
                        self.logger.error(f"Failed to execute: {cmd}")
                        return False
            
            # Check HAProxy status
            success, status = self.run_command("sudo service haproxy status")
            if success:
                self.logger.info("HAProxy configured and running successfully")
                return True
            else:
                self.logger.warning("HAProxy configuration completed but service status check failed")
                return self.fix_haproxy_issues()
                
        except Exception as e:
            self.logger.error(f"HAProxy configuration failed: {e}")
            return False

    def fix_haproxy_issues(self):
        """Fix common HAProxy issues"""
        self.logger.info("Attempting to fix HAProxy issues...")
        
        # Create missing PID file
        success, output = self.run_command("sudo touch /var/run/haproxy.pid")
        if success:
            self.logger.info("Created missing PID file")
        
        # Restart HAProxy
        success, output = self.run_command("sudo service haproxy restart")
        if success:
            success, status = self.run_command("sudo service haproxy status")
            if success:
                return True
        
        # Create admin socket directory and file
        commands = [
            "sudo mkdir -p /run/haproxy",
            "sudo touch /run/haproxy/admin.sock",
            "sudo chmod 666 /run/haproxy/admin.sock",
            "sudo service haproxy restart"
        ]
        
        for cmd in commands:
            success, output = self.run_command(cmd)
            if not success:
                self.logger.error(f"Failed to execute: {cmd}")
        
        # Final status check
        success, status = self.run_command("sudo service haproxy status")
        return success

    def configure_squid(self):
        """Generate and configure Squid"""
        self.logger.info("Configuring Squid...")
        
        try:
            if self.target_server:
                # Remote configuration
                commands = [
                    "cd /tmp/netconf_new/squidTools",
                    "sudo php -f squidConfigCreator.php",
                    "sudo cp squid.conf /etc/squid/",
                    "sudo service squid restart"
                ]
                
                for cmd in commands:
                    success, output = self.run_remote_command(cmd)
                    if not success:
                        self.logger.error(f"Failed to execute: {cmd}")
                        return False
            else:
                # Local configuration
                commands = [
                    "cd /tmp/netconf_new/squidTools",
                    "sudo php -f squidConfigCreator.php",
                    "sudo cp squid.conf /etc/squid/",
                    "sudo service squid restart"
                ]
                
                for cmd in commands:
                    success, output = self.run_command(cmd)
                    if not success:
                        self.logger.error(f"Failed to execute: {cmd}")
                        return False
            
            # Check Squid status
            success, status = self.run_command("sudo service squid status")
            if success:
                self.logger.info("Squid configured and running successfully")
                return True
            else:
                self.logger.warning("Squid configuration completed but service status check failed")
                return self.fix_squid_issues()
                
        except Exception as e:
            self.logger.error(f"Squid configuration failed: {e}")
            return False

    def fix_squid_issues(self):
        """Fix common Squid issues"""
        self.logger.info("Attempting to fix Squid issues...")
        
        # Copy ncsa_auth file from 0495-5 server
        commands = [
            f"scp -P {self.ssh_port} -r root@{self.config_server}:/usr/lib64/squid/ncsa_auth .",
            "sudo mv ncsa_auth /usr/lib64/squid/",
            "sudo service squid restart"
        ]
        
        for cmd in commands:
            success, output = self.run_command(cmd)
            if not success:
                self.logger.error(f"Failed to execute: {cmd}")
        
        # Final status check
        success, status = self.run_command("sudo service squid status")
        return success

    def test_squid_connectivity(self):
        """Test Squid connectivity using curl commands"""
        self.logger.info("Testing Squid connectivity...")
        
        test_commands = [
            "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23451' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
            "curl -H 'Proxy-Authorization: Basic aXAyXzB1dGMwbm4zY3QyOnNxdWxkdHcwM3gwdGUxX2lwMg==' --request GET --proxy 'http://127.0.0.1:23452' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
            "curl --request GET --proxy 'http://127.0.0.1:23432' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'",
            "curl --request GET --proxy 'http://127.0.0.1:23433' 'https://run.mocky.io/v3/f39c73f6-7ab3-4fa6-a3b6-84b929786d7c'"
        ]
        
        expected_response = '{"status": "Working"}'
        all_tests_passed = True
        
        for i, cmd in enumerate(test_commands, 1):
            self.logger.info(f"Running test {i}/4...")
            success, output = self.run_command(cmd, check_return_code=False)
            
            if success and expected_response in output:
                self.logger.info(f"Test {i} PASSED")
            else:
                self.logger.error(f"Test {i} FAILED: {output}")
                all_tests_passed = False
        
        if all_tests_passed:
            self.logger.info("All Squid connectivity tests PASSED")
            return True
        else:
            self.logger.error("Some Squid connectivity tests FAILED")
            return False

    def generate_upgrade_report(self):
        """Generate upgrade completion report"""
        self.logger.info("Generating upgrade report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "haproxy_version": None,
            "squid_version": None,
            "haproxy_status": None,
            "squid_status": None,
            "squid_tests": None
        }
        
        # Check HAProxy version and status
        success, version = self.run_command("haproxy -v", check_return_code=False)
        if success:
            report["haproxy_version"] = version.strip()
        
        success, status = self.run_command("sudo service haproxy status", check_return_code=False)
        report["haproxy_status"] = "running" if success else "stopped"
        
        # Check Squid version and status
        success, version = self.run_command("squid -v", check_return_code=False)
        if success:
            report["squid_version"] = version.strip()
        
        success, status = self.run_command("sudo service squid status", check_return_code=False)
        report["squid_status"] = "running" if success else "stopped"
        
        # Test Squid connectivity
        report["squid_tests"] = self.test_squid_connectivity()
        
        # Save report to file
        report_file = f"upgrade_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Upgrade report saved to: {report_file}")
        return report

    def run_full_upgrade(self, skip_config_copy=False):
        """Run the complete upgrade process"""
        self.logger.info("Starting HAProxy and Squid upgrade process...")
        
        try:
            # Pre-upgrade checks
            self.check_current_versions()
            
            # Backup existing binaries
            if not self.backup_existing_binaries():
                self.logger.error("Backup failed - aborting upgrade")
                return False
            
            # Upgrade HAProxy
            if not self.upgrade_haproxy():
                self.logger.error("HAProxy upgrade failed")
                return False
            
            # Upgrade Squid
            if not self.upgrade_squid():
                self.logger.error("Squid upgrade failed")
                return False
            
            # Handle configuration files
            if not skip_config_copy:
                if not self.copy_configurations_from_server():
                    self.logger.warning("Configuration copy failed - using existing configs")
                
                if self.target_server and not self.push_configurations_to_target():
                    self.logger.warning("Configuration push failed - using existing configs")
            
            # Configure services
            if not self.configure_haproxy():
                self.logger.error("HAProxy configuration failed")
                return False
            
            if not self.configure_squid():
                self.logger.error("Squid configuration failed")
                return False
            
            # Test connectivity
            if not self.test_squid_connectivity():
                self.logger.warning("Squid connectivity tests failed")
            
            # Generate report
            report = self.generate_upgrade_report()
            
            self.logger.info("Upgrade process completed successfully!")
            self.logger.info(f"Check the log file for details: {self.log_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Upgrade process failed: {e}")
            return False

def main():
    """Main function"""
    print("HAProxy and Squid Upgrade Automation")
    print("====================================")
    
    # Get user inputs
    target_server = input("Enter target server (leave empty for local upgrade): ").strip()
    if not target_server:
        target_server = None
    
    ssh_port = input("Enter SSH port (default 22000): ").strip()
    if not ssh_port:
        ssh_port = 22000
    else:
        ssh_port = int(ssh_port)
    
    skip_config = input("Skip configuration file copy? (y/N): ").strip().lower() == 'y'
    
    # Confirm before proceeding
    print(f"\nUpgrade Configuration:")
    print(f"Target Server: {target_server or 'Local'}")
    print(f"SSH Port: {ssh_port}")
    print(f"Skip Config Copy: {skip_config}")
    print(f"HAProxy Version: 2.4.2")
    print(f"Squid Version: 3.5.28")
    
    confirm = input("\nProceed with upgrade? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Upgrade cancelled.")
        return
    
    # Initialize and run upgrade
    upgrader = HAProxySquidUpgrade(target_server, ssh_port)
    success = upgrader.run_full_upgrade(skip_config_copy=skip_config)
    
    if success:
        print("\n✅ Upgrade completed successfully!")
    else:
        print("\n❌ Upgrade failed. Check the log file for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()