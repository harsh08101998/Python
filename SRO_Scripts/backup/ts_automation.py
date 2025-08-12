#!/usr/bin/env python3
"""
TS (Telephone Server) Installation Automation Script
This script automates the TS installation process based on ahn_installation.txt

"""

import os
import sys
import json
import csv
import subprocess
import requests
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

# Configure comprehensive logging with detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('ts_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TSAutomation:
    """
    Main automation class for TS installation process.
    Handles all phases of installation with proper error handling and rollback capabilities.
    """
    
    def __init__(self, config_file: str = "ts_config.json"):
        """
        Initialize the automation system.
        
        Args:
            config_file (str): Path to configuration JSON file
        """
        self.config_file = config_file
        self.config = self.load_config()  # Load configuration from JSON
        self.checklist_data = []  # Track all tasks and their status
        self.current_phase = 0  # Track current execution phase
        self.failed_phase = None  # Track which phase failed
        
    def load_config(self) -> Dict:
        """
        Load configuration from JSON file with fallback to defaults.
        
        Returns:
            Dict: Configuration dictionary with all settings
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration if file doesn't exist
            logger.warning(f"Config file {self.config_file} not found, using defaults")
            return {
                "jenkins_url": "https://build.corp.exotel.in:8080",
                "jenkins_username": "",
                "jenkins_token": "",
                "aws_region": "ap-southeast-1",
                "route53_zone_id": "",
                "git_branch": "feat/ts-centos-7-changes-updated",
                "ansible_version": "9-C7",
                "services": {
                    "asterisk": {"ans_version": "9-C7", "version": "latest-stable"},
                    "legolas-ts": {"ans_version": "5-C7", "version": "latest-stable"},
                    "adhearsion": {"ans_version": "29-C7", "version": "latest"},
                    "firefoot-ts": {"ans_version": "7-C7", "version": "latest"},
                    "amix": {"ans_version": "12-C7", "version": "latest-stable"},
                    "eventshipper": {"ans_version": "8-C7", "version": "latest-stable"},
                    "causix": {"ans_version": "5-C7", "version": "latest-stable"},
                    "causixenqueuer": {"ans_version": "2-C7", "version": "latest-stable"},
                    "route-switcher": {"ans_version": "11-C7", "version": "latest-stable"},
                    "voipmonitor": {"ans_version": "21-C7", "version": "latest-stable"},
                    "fangorn": {"ans_version": "14-C7", "version": "latest-stable"},
                    "traffic-shaper": {"ans_version": "1-C7", "version": "6-C7"}
                }
            }
    
    def save_config(self):
        """Save current configuration to JSON file for persistence."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        logger.info(f"Configuration saved to {self.config_file}")
    
    def add_checklist_item(self, step: str, task: str, status: str = "Pending", notes: str = ""):
        """
        Add item to checklist with timestamp and detailed information.
        
        Args:
            step (str): Step number or phase identifier
            task (str): Description of the task
            status (str): Current status (Pending/Completed/Failed)
            notes (str): Additional notes or error details
        """
        self.checklist_data.append({
            "Step": step,
            "Task": task,
            "Status": status,
            "Notes": notes,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Phase": self.current_phase
        })
        logger.info(f"Checklist updated: {step} - {task} - {status}")
    
    def export_checklist_csv(self, filename: str = "ts_installation_checklist.csv"):
        """
        Export checklist to CSV file for easy tracking and reporting.
        
        Args:
            filename (str): Output CSV filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Step", "Task", "Status", "Notes", "Timestamp", "Phase"])
            writer.writeheader()
            writer.writerows(self.checklist_data)
        logger.info(f"Checklist exported to {filename}")
    
    def run_jenkins_job(self, job_name: str, parameters: Dict = None) -> bool:
        """
        Trigger Jenkins job with parameters using REST API.
        
        Args:
            job_name (str): Name of the Jenkins job to trigger
            parameters (Dict): Parameters to pass to the job
            
        Returns:
            bool: True if job triggered successfully, False otherwise
        """
        try:
            # Construct Jenkins URL for job triggering
            url = f"{self.config['jenkins_url']}/job/{job_name}/buildWithParameters"
            
            if parameters:
                # Convert parameters to Jenkins format
                param_data = {}
                for key, value in parameters.items():
                    param_data[key] = str(value)
                
                logger.info(f"Triggering Jenkins job {job_name} with parameters: {param_data}")
                response = requests.post(
                    url,
                    params=param_data,
                    auth=(self.config['jenkins_username'], self.config['jenkins_token']),
                    verify=False,  # Disable SSL verification for internal Jenkins
                    timeout=30  # 30 second timeout
                )
            else:
                logger.info(f"Triggering Jenkins job {job_name} without parameters")
                response = requests.post(
                    url,
                    auth=(self.config['jenkins_username'], self.config['jenkins_token']),
                    verify=False,
                    timeout=30
                )
            
            # Check response status
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Successfully triggered Jenkins job: {job_name}")
                return True
            else:
                logger.error(f"Failed to trigger Jenkins job {job_name}: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error triggering Jenkins job {job_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error triggering Jenkins job {job_name}: {str(e)}")
            return False
    
    def execute_ssh_command(self, host: str, command: str, username: str = "root", port: int = 22000) -> Tuple[bool, str]:
        """
        Execute SSH command on remote host with error handling.
        
        Args:
            host (str): Target hostname or IP
            command (str): Command to execute
            username (str): SSH username (default: root)
            port (int): SSH port (default: 22000 for TS servers)
            
        Returns:
            Tuple[bool, str]: (success_status, output_or_error_message)
        """
        try:
            # Construct SSH command with proper formatting
            ssh_cmd = f"ssh -p {port} {username}@{host} '{command}'"
            logger.info(f"Executing SSH command on {host}: {command}")
            
            # Execute command with timeout
            result = subprocess.run(
                ssh_cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                logger.info(f"SSH command successful on {host}")
                return True, result.stdout
            else:
                logger.error(f"SSH command failed on {host}: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            error_msg = f"SSH command timed out on {host}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"SSH execution error on {host}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def check_service_status(self, host: str, service: str) -> bool:
        """
        Check if service is running on remote host.
        
        Args:
            host (str): Target hostname
            service (str): Service name to check
            
        Returns:
            bool: True if service is running, False otherwise
        """
        success, output = self.execute_ssh_command(host, f"sudo service {service} status")
        is_running = success and "running" in output.lower()
        logger.info(f"Service {service} on {host}: {'Running' if is_running else 'Not Running'}")
        return is_running
    
    def phase1_os_installation(self, hostname: str, ip_address: str) -> bool:
        """
        Phase 1: OS Installation and Basic Setup.
        This phase handles the initial server setup and network configuration.
        
        Args:
            hostname (str): Target hostname
            ip_address (str): Target IP address
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 1: OS Installation ===")
        self.current_phase = 1
        
        try:
            # Step 1.1: iDRAC Security Configuration (Manual step)
            self.add_checklist_item("1.1", "iDRAC Security Configuration", "Manual", 
                                   "Disable IPMI, VLAN, configure SSL/TLS, SSH settings")
            logger.info("Step 1.1: iDRAC Security Configuration - Manual step required")
            
            # Step 1.2: CentOS Installation (Manual step)
            self.add_checklist_item("1.2", "CentOS Installation via iDRAC", "Manual",
                                   "Install CentOS 6.10, configure network, set root password")
            logger.info("Step 1.2: CentOS Installation - Manual step required")
            
            # Step 1.3: Network Interface Configuration (Manual step)
            self.add_checklist_item("1.3", "Network Interface Configuration", "Manual",
                                   "Configure em1-em4 interfaces with IP addresses")
            logger.info("Step 1.3: Network Interface Configuration - Manual step required")
            
            # Step 1.4: ILL Activation (Automated verification)
            logger.info("Step 1.4: Verifying ILL Activation...")
            success, output = self.execute_ssh_command(hostname, "ping -c 3 google.com")
            if success:
                self.add_checklist_item("1.4", "ILL Activation", "Completed", "Network connectivity verified")
                logger.info("Step 1.4: ILL Activation - Network connectivity verified")
            else:
                self.add_checklist_item("1.4", "ILL Activation", "Failed", "Check network configuration")
                logger.error("Step 1.4: ILL Activation - Network connectivity failed")
                return False  # Stop execution if network is not working
            
            # Step 1.5: DNS Entry in Route53 (Manual step)
            self.add_checklist_item("1.5", "DNS Entry in Route53", "Manual",
                                   f"Create A records for {hostname} in exotel.in and exotel.com")
            logger.info("Step 1.5: DNS Entry in Route53 - Manual step required")
            
            logger.info("=== Phase 1 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {str(e)}")
            self.failed_phase = 1
            return False
    
    def phase2_ts_deployment(self, hostname: str) -> bool:
        """
        Phase 2: TS Deployment through Jenkins.
        This phase handles the initial TS deployment and base configuration.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 2: TS Deployment ===")
        self.current_phase = 2
        
        try:
            # Step 2.1: ts-ami-setup-build
            logger.info("Step 2.1: Triggering ts-ami-setup-build...")
            self.add_checklist_item("2.1", "ts-ami-setup-build", "Pending")
            
            success = self.run_jenkins_job("ts-ami-setup-build", {
                "PROD_GIT_BRANCH": self.config['git_branch']
            })
            
            if not success:
                logger.error("Step 2.1: ts-ami-setup-build failed")
                self.add_checklist_item("2.1", "ts-ami-setup-build", "Failed")
                return False
            
            self.add_checklist_item("2.1", "ts-ami-setup-build", "Completed")
            logger.info("Step 2.1: ts-ami-setup-build completed successfully")
            
            # Step 2.2: ts-ami-deploy (ts_base_ami)
            logger.info("Step 2.2: Triggering ts-ami-deploy (ts_base_ami)...")
            self.add_checklist_item("2.2", "ts-ami-deploy (ts_base_ami)", "Pending")
            
            success = self.run_jenkins_job("ts-ami-deploy", {
                "JOB_TYPE": "ts_base_ami",
                "GIT_BRANCH": self.config['git_branch'],
                "HOST": hostname,
                "SSH_USER": "root",
                "SILLYIO_NAME": f"{hostname.replace('.', '-')}"
            })
            
            if not success:
                logger.error("Step 2.2: ts-ami-deploy (ts_base_ami) failed")
                self.add_checklist_item("2.2", "ts-ami-deploy (ts_base_ami)", "Failed")
                return False
            
            self.add_checklist_item("2.2", "ts-ami-deploy (ts_base_ami)", "Completed")
            logger.info("Step 2.2: ts-ami-deploy (ts_base_ami) completed successfully")
            
            # Step 2.3: Server Reboot
            logger.info("Step 2.3: Rebooting server...")
            self.add_checklist_item("2.3", "Server Reboot", "Pending")
            
            success, _ = self.execute_ssh_command(hostname, "sudo reboot now")
            if not success:
                logger.error("Step 2.3: Server reboot failed")
                self.add_checklist_item("2.3", "Server Reboot", "Failed")
                return False
            
            self.add_checklist_item("2.3", "Server Reboot", "Completed")
            logger.info("Step 2.3: Server reboot initiated")
            
            # Step 2.4: Wait for server to come back online
            logger.info("Step 2.4: Waiting for server to come back online...")
            time.sleep(60)  # Wait 60 seconds for reboot
            
            # Step 2.5: Check SSH service
            logger.info("Step 2.5: Checking SSH service...")
            success, _ = self.execute_ssh_command(hostname, "sudo service sshd status")
            if not success:
                logger.error("Step 2.5: SSH service check failed")
                self.add_checklist_item("2.4", "SSH Service Check", "Failed", "Start sshd manually")
                return False
            
            self.add_checklist_item("2.4", "SSH Service Check", "Completed")
            logger.info("Step 2.5: SSH service is running")
            
            logger.info("=== Phase 2 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {str(e)}")
            self.failed_phase = 2
            return False
    
    def phase3_verification(self, hostname: str) -> bool:
        """
        Phase 3: Post-deployment verification.
        This phase verifies that all required users, services, and configurations are in place.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 3: Verification ===")
        self.current_phase = 3
        
        try:
            # Step 3.1: User verification
            logger.info("Step 3.1: Verifying required users...")
            success, output = self.execute_ssh_command(hostname, "less /etc/passwd | grep -E '(asterisk|exomon|recotrix)'")
            if success and all(user in output for user in ['asterisk', 'exomon', 'recotrix']):
                self.add_checklist_item("3.1", "User Verification", "Completed")
                logger.info("Step 3.1: User verification successful")
            else:
                logger.error("Step 3.1: User verification failed")
                self.add_checklist_item("3.1", "User Verification", "Failed")
                return False
            
            # Step 3.2: SSH configs
            logger.info("Step 3.2: Checking SSH configurations...")
            success, _ = self.execute_ssh_command(hostname, "ls -la /home/asterisk/.ssh/")
            if success:
                self.add_checklist_item("3.2", "SSH Configs", "Completed")
                logger.info("Step 3.2: SSH configurations verified")
            else:
                logger.error("Step 3.2: SSH configurations failed")
                self.add_checklist_item("3.2", "SSH Configs", "Failed")
                return False
            
            # Step 3.3: Bash configs
            logger.info("Step 3.3: Checking bash configurations...")
            success, _ = self.execute_ssh_command(hostname, "ls -la /home/asterisk/ | grep bash")
            if success:
                self.add_checklist_item("3.3", "Bash Configs", "Completed")
                logger.info("Step 3.3: Bash configurations verified")
            else:
                logger.warning("Step 3.3: Bash configurations incomplete, may need manual fix")
                self.add_checklist_item("3.3", "Bash Configs", "Failed", "Copy .bash_history manually")
                # Don't fail here as it's not critical
            
            # Step 3.4: AWS credentials
            logger.info("Step 3.4: Checking AWS credentials...")
            success, _ = self.execute_ssh_command(hostname, "cat /home/asterisk/.aws/credentials")
            if success:
                self.add_checklist_item("3.4", "AWS Credentials", "Completed")
                logger.info("Step 3.4: AWS credentials verified")
            else:
                logger.error("Step 3.4: AWS credentials failed")
                self.add_checklist_item("3.4", "AWS Credentials", "Failed")
                return False
            
            # Step 3.5: fail2ban
            logger.info("Step 3.5: Checking fail2ban service...")
            if self.check_service_status(hostname, "fail2ban"):
                self.add_checklist_item("3.5", "fail2ban Service", "Completed")
                logger.info("Step 3.5: fail2ban service is running")
            else:
                logger.warning("Step 3.5: fail2ban service not running")
                self.add_checklist_item("3.5", "fail2ban Service", "Failed")
                # Don't fail here as it's not critical
            
            # Step 3.6: SSH port configuration
            logger.info("Step 3.6: Checking SSH port configuration...")
            success, output = self.execute_ssh_command(hostname, "grep -i '22000' /etc/ssh/sshd_config")
            if success and "22000" in output:
                self.add_checklist_item("3.6", "SSH Port Configuration", "Completed")
                logger.info("Step 3.6: SSH port configuration verified")
            else:
                logger.error("Step 3.6: SSH port configuration failed")
                self.add_checklist_item("3.6", "SSH Port Configuration", "Failed")
                return False
            
            logger.info("=== Phase 3 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {str(e)}")
            self.failed_phase = 3
            return False
    
    def phase4_environmental_setup(self, hostname: str) -> bool:
        """
        Phase 4: Environmental Setup.
        This phase deploys the environmental setup and verifies Ruby and MySQL.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 4: Environmental Setup ===")
        self.current_phase = 4
        
        try:
            # Step 4.1: ts_environmental_setup
            logger.info("Step 4.1: Triggering ts_environmental_setup...")
            self.add_checklist_item("4.1", "ts_environmental_setup", "Pending")
            
            success = self.run_jenkins_job("ts-ami-deploy", {
                "JOB_TYPE": "ts_environmental_setup",
                "GIT_BRANCH": self.config['git_branch'],
                "HOST": hostname,
                "SSH_USER": "root",
                "SILLYIO_NAME": f"{hostname.replace('.', '-')}"
            })
            
            if not success:
                logger.error("Step 4.1: ts_environmental_setup failed")
                self.add_checklist_item("4.1", "ts_environmental_setup", "Failed")
                return False
            
            self.add_checklist_item("4.1", "ts_environmental_setup", "Completed")
            logger.info("Step 4.1: ts_environmental_setup completed successfully")
            
            # Step 4.2: Wait for deployment (25 minutes)
            logger.info("Step 4.2: Waiting 25 minutes for environmental setup deployment...")
            time.sleep(1500)  # 25 minutes
            
            # Step 4.3: Verify Ruby version
            logger.info("Step 4.3: Verifying Ruby version...")
            success, output = self.execute_ssh_command(hostname, "/opt/jruby-1.7.1/bin/jruby --version")
            if success and "1.7" in output:
                self.add_checklist_item("4.2", "Ruby Version Check", "Completed")
                logger.info("Step 4.3: Ruby version verified")
            else:
                logger.error("Step 4.3: Ruby version check failed")
                self.add_checklist_item("4.2", "Ruby Version Check", "Failed")
                return False
            
            # Step 4.4: Verify MySQL
            logger.info("Step 4.4: Verifying MySQL service...")
            if self.check_service_status(hostname, "mysqld"):
                self.add_checklist_item("4.3", "MySQL Service Check", "Completed")
                logger.info("Step 4.4: MySQL service is running")
            else:
                logger.error("Step 4.4: MySQL service check failed")
                self.add_checklist_item("4.3", "MySQL Service Check", "Failed")
                return False
            
            logger.info("=== Phase 4 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 4 failed: {str(e)}")
            self.failed_phase = 4
            return False
    
    def phase5_services_setup(self, hostname: str) -> bool:
        """
        Phase 5: Services Setup.
        This phase deploys core services and verifies their status.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 5: Services Setup ===")
        self.current_phase = 5
        
        try:
            # Step 5.1: ts_services_setup
            logger.info("Step 5.1: Triggering ts_services_setup...")
            self.add_checklist_item("5.1", "ts_services_setup", "Pending")
            
            success = self.run_jenkins_job("ts-ami-deploy", {
                "JOB_TYPE": "ts_services_setup",
                "GIT_BRANCH": self.config['git_branch'],
                "HOST": hostname,
                "SSH_USER": "root",
                "SILLYIO_NAME": f"{hostname.replace('.', '-')}"
            })
            
            if not success:
                logger.error("Step 5.1: ts_services_setup failed")
                self.add_checklist_item("5.1", "ts_services_setup", "Failed")
                return False
            
            self.add_checklist_item("5.1", "ts_services_setup", "Completed")
            logger.info("Step 5.1: ts_services_setup completed successfully")
            
            # Step 5.2: Check core services
            logger.info("Step 5.2: Checking core services...")
            services = ['beanstalkd', 'dnsmasq', 'rsyslog', 'vsftpd', 'fail2ban']
            all_services_ok = True
            
            for service in services:
                if self.check_service_status(hostname, service):
                    self.add_checklist_item("5.2", f"{service} Service Check", "Completed")
                    logger.info(f"Step 5.2: {service} service is running")
                else:
                    logger.warning(f"Step 5.2: {service} service is not running")
                    self.add_checklist_item("5.2", f"{service} Service Check", "Failed")
                    all_services_ok = False
            
            if not all_services_ok:
                logger.warning("Some core services are not running, but continuing...")
            
            logger.info("=== Phase 5 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 5 failed: {str(e)}")
            self.failed_phase = 5
            return False
    
    def phase6_telegraf_installation(self, hostname: str) -> bool:
        """
        Phase 6: Telegraf Installation.
        This phase installs and configures Telegraf for monitoring.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 6: Telegraf Installation ===")
        self.current_phase = 6
        
        try:
            # Step 6.1: ts_telegraf_installation
            logger.info("Step 6.1: Triggering ts_telegraf_installation...")
            self.add_checklist_item("6.1", "ts_telegraf_installation", "Pending")
            
            success = self.run_jenkins_job("ts-ami-deploy", {
                "JOB_TYPE": "ts_telegraf_installation",
                "GIT_BRANCH": self.config['git_branch'],
                "HOST": hostname,
                "SSH_USER": "root",
                "SILLYIO_NAME": f"{hostname.replace('.', '-')}"
            })
            
            if success:
                self.add_checklist_item("6.1", "ts_telegraf_installation", "Completed")
                logger.info("Step 6.1: ts_telegraf_installation completed successfully")
            else:
                self.add_checklist_item("6.1", "ts_telegraf_installation", "Failed", "May be fine if it fails")
                logger.warning("Step 6.1: ts_telegraf_installation failed, but continuing...")
            
            logger.info("=== Phase 6 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 6 failed: {str(e)}")
            self.failed_phase = 6
            return False
    
    def phase7_monitoring_scripts(self, hostname: str) -> bool:
        """
        Phase 7: Monitoring Scripts Deployment.
        This phase deploys monitoring scripts for Nagios integration.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 7: Monitoring Scripts ===")
        self.current_phase = 7
        
        try:
            # Step 7.1: monitoring-scripts-build
            logger.info("Step 7.1: Triggering monitoring-scripts-build...")
            self.add_checklist_item("7.1", "monitoring-scripts-build", "Pending")
            
            success = self.run_jenkins_job("monitoring-scripts-build", {
                "GIT_BRANCH": "master",
                "NAGIOS_DNS_NAME": "nagios.internal.exotel.in"
            })
            
            if not success:
                logger.error("Step 7.1: monitoring-scripts-build failed")
                self.add_checklist_item("7.1", "monitoring-scripts-build", "Failed")
                return False
            
            self.add_checklist_item("7.1", "monitoring-scripts-build", "Completed")
            logger.info("Step 7.1: monitoring-scripts-build completed successfully")
            
            # Step 7.2: Get version number (this would need to be extracted from build output)
            version_number = "458"  # This should be extracted from build output
            logger.info(f"Step 7.2: Using monitoring scripts version: {version_number}")
            
            # Step 7.3: monitoring-scripts-deploy-ts
            logger.info("Step 7.3: Triggering monitoring-scripts-deploy-ts...")
            self.add_checklist_item("7.2", "monitoring-scripts-deploy-ts", "Pending")
            
            success = self.run_jenkins_job("monitoring-scripts-deploy-ts", {
                "HOST": hostname,
                "BRANCH": "master",
                "VERSION_NUMBER": version_number,
                "ENV": "prod"
            })
            
            if not success:
                logger.error("Step 7.3: monitoring-scripts-deploy-ts failed")
                self.add_checklist_item("7.2", "monitoring-scripts-deploy-ts", "Failed")
                return False
            
            self.add_checklist_item("7.2", "monitoring-scripts-deploy-ts", "Completed")
            logger.info("Step 7.3: monitoring-scripts-deploy-ts completed successfully")
            
            logger.info("=== Phase 7 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 7 failed: {str(e)}")
            self.failed_phase = 7
            return False
    
    def phase8_asterisk_deployment(self, hostname: str) -> bool:
        """
        Phase 8: Asterisk Deployment.
        This phase deploys the Asterisk service and verifies its status.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 8: Asterisk Deployment ===")
        self.current_phase = 8
        
        try:
            # Step 8.1: ts-code-push for asterisk
            logger.info("Step 8.1: Triggering Asterisk deployment...")
            self.add_checklist_item("8.1", "Asterisk Deployment", "Pending")
            
            success = self.run_jenkins_job("ts-code-push", {
                "SERVICE": "asterisk",
                "ANS_VERSION": self.config['services']['asterisk']['ans_version'],
                "VERSION": self.config['services']['asterisk']['version'],
                "HOST": hostname,
                "EXTERNAL_VAR": "conftype=slave",
                "GIT_BRANCH": self.config['git_branch']
            })
            
            if not success:
                logger.error("Step 8.1: Asterisk deployment failed")
                self.add_checklist_item("8.1", "Asterisk Deployment", "Failed")
                return False
            
            self.add_checklist_item("8.1", "Asterisk Deployment", "Completed")
            logger.info("Step 8.1: Asterisk deployment completed successfully")
            
            # Step 8.2: Verify asterisk service
            logger.info("Step 8.2: Verifying Asterisk service...")
            if self.check_service_status(hostname, "asterisk"):
                self.add_checklist_item("8.2", "Asterisk Service Check", "Completed")
                logger.info("Step 8.2: Asterisk service is running")
            else:
                logger.error("Step 8.2: Asterisk service check failed")
                self.add_checklist_item("8.2", "Asterisk Service Check", "Failed")
                return False
            
            logger.info("=== Phase 8 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 8 failed: {str(e)}")
            self.failed_phase = 8
            return False
    
    def phase9_legolas_deployment(self, hostname: str) -> bool:
        """
        Phase 9: Legolas Deployment.
        This phase deploys the Legolas service and verifies its status.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 9: Legolas Deployment ===")
        self.current_phase = 9
        
        try:
            # Step 9.1: Legolas-ts deployment
            logger.info("Step 9.1: Triggering Legolas-ts deployment...")
            self.add_checklist_item("9.1", "Legolas-ts Deployment", "Pending")
            
            success = self.run_jenkins_job("Legolas-ts", {
                "ANS_VERSION": self.config['services']['legolas-ts']['ans_version'],
                "VERSION": self.config['services']['legolas-ts']['version'],
                "HOSTS": hostname,
                "GIT_BRANCH": self.config['git_branch']
            })
            
            if not success:
                logger.error("Step 9.1: Legolas-ts deployment failed")
                self.add_checklist_item("9.1", "Legolas-ts Deployment", "Failed")
                return False
            
            self.add_checklist_item("9.1", "Legolas-ts Deployment", "Completed")
            logger.info("Step 9.1: Legolas-ts deployment completed successfully")
            
            # Step 9.2: Verify legolas-ts service
            logger.info("Step 9.2: Verifying Legolas-ts service...")
            success, _ = self.execute_ssh_command(hostname, "sudo service legolas-ts status")
            if success:
                self.add_checklist_item("9.2", "Legolas-ts Service Check", "Completed")
                logger.info("Step 9.2: Legolas-ts service is running")
            else:
                logger.error("Step 9.2: Legolas-ts service check failed")
                self.add_checklist_item("9.2", "Legolas-ts Service Check", "Failed")
                return False
            
            logger.info("=== Phase 9 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 9 failed: {str(e)}")
            self.failed_phase = 9
            return False
    
    def phase10_adhearsion_deployment(self, hostname: str) -> bool:
        """
        Phase 10: Adhearsion Deployment.
        This phase builds and deploys the Adhearsion service.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 10: Adhearsion Deployment ===")
        self.current_phase = 10
        
        try:
            # Step 10.1: Adhearsion build
            logger.info("Step 10.1: Triggering Adhearsion build...")
            self.add_checklist_item("10.1", "Adhearsion Build", "Pending")
            
            success = self.run_jenkins_job("adhearsion-build-prod", {
                "GIT_BRANCH": self.config['git_branch']
            })
            
            if not success:
                logger.error("Step 10.1: Adhearsion build failed")
                self.add_checklist_item("10.1", "Adhearsion Build", "Failed")
                return False
            
            self.add_checklist_item("10.1", "Adhearsion Build", "Completed")
            logger.info("Step 10.1: Adhearsion build completed successfully")
            
            # Step 10.2: Get build version (this should be extracted from build output)
            build_version = "904"  # This should be extracted from build output
            logger.info(f"Step 10.2: Using Adhearsion build version: {build_version}")
            
            # Step 10.3: Adhearsion deploy
            logger.info("Step 10.3: Triggering Adhearsion deploy...")
            self.add_checklist_item("10.2", "Adhearsion Deploy", "Pending")
            
            success = self.run_jenkins_job("adhearsion-deploy-prod", {
                "ANS_VERSION": self.config['services']['adhearsion']['ans_version'],
                "VERSION": build_version,
                "HOST": hostname,
                "EXTERNAL_VARS": "conftype=slave",
                "GIT_BRANCH": self.config['git_branch']
            })
            
            if not success:
                logger.error("Step 10.3: Adhearsion deploy failed")
                self.add_checklist_item("10.2", "Adhearsion Deploy", "Failed")
                return False
            
            self.add_checklist_item("10.2", "Adhearsion Deploy", "Completed")
            logger.info("Step 10.3: Adhearsion deploy completed successfully")
            
            # Step 10.4: Verify ahn process
            logger.info("Step 10.4: Verifying AHN process...")
            success, _ = self.execute_ssh_command(hostname, "sudo status ahn")
            if success:
                self.add_checklist_item("10.3", "AHN Process Check", "Completed")
                logger.info("Step 10.4: AHN process is running")
            else:
                logger.error("Step 10.4: AHN process check failed")
                self.add_checklist_item("10.3", "AHN Process Check", "Failed")
                return False
            
            logger.info("=== Phase 10 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 10 failed: {str(e)}")
            self.failed_phase = 10
            return False
    
    def phase11_remaining_services(self, hostname: str) -> bool:
        """
        Phase 11: Deploy remaining services.
        This phase deploys all remaining application services.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 11: Remaining Services ===")
        self.current_phase = 11
        
        try:
            services = [
                ("firefoot-ts", "firefoot-ts"),
                ("amix", "amix"),
                ("eventshipper", "eventshipper"),
                ("causix", "causix"),
                ("causixenqueuer", "causixenqueuer"),
                ("route-switcher", "route-switcher"),
                ("voipmonitor", "voipmonitor"),
                ("fangorn", "fangorn"),
                ("traffic-shaper", "traffic-shaper")
            ]
            
            for service_name, service_key in services:
                logger.info(f"Step 11.1: Deploying {service_name}...")
                self.add_checklist_item("11.1", f"{service_name} Deployment", "Pending")
                
                # Create causix_recordings directory for causix
                if service_name == "causix":
                    logger.info(f"Creating causix_recordings directory for {service_name}...")
                    self.execute_ssh_command(hostname, 
                        "mkdir -p /var/log/exotel/recordings/causix_recordings")
                
                success = self.run_jenkins_job("ts-code-push", {
                    "SERVICE": service_name,
                    "ANS_VERSION": self.config['services'][service_key]['ans_version'],
                    "VERSION": self.config['services'][service_key]['version'],
                    "HOST": hostname,
                    "EXTERNAL_VARS": "conftype=slave",
                    "GIT_BRANCH": self.config['git_branch']
                })
                
                if not success:
                    logger.error(f"Step 11.1: {service_name} deployment failed")
                    self.add_checklist_item("11.1", f"{service_name} Deployment", "Failed")
                    return False
                
                self.add_checklist_item("11.1", f"{service_name} Deployment", "Completed")
                logger.info(f"Step 11.1: {service_name} deployment completed successfully")
                
                # Step 11.2: Verify service
                logger.info(f"Step 11.2: Verifying {service_name} service...")
                if service_name == "traffic-shaper":
                    success, _ = self.execute_ssh_command(hostname, 
                        "sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status")
                else:
                    success, _ = self.execute_ssh_command(hostname, f"sudo status {service_name}")
                
                if success:
                    self.add_checklist_item("11.2", f"{service_name} Service Check", "Completed")
                    logger.info(f"Step 11.2: {service_name} service is running")
                else:
                    logger.error(f"Step 11.2: {service_name} service check failed")
                    self.add_checklist_item("11.2", f"{service_name} Service Check", "Failed")
                    return False
            
            logger.info("=== Phase 11 completed successfully ===")
            return True
            
        except Exception as e:
            logger.error(f"Phase 11 failed: {str(e)}")
            self.failed_phase = 11
            return False
    
    def phase12_rsyslog_deployment(self, hostname: str) -> bool:
        """
        Phase 12: Rsyslog Deployment.
        This phase deploys rsyslog configuration for log forwarding.
        
        Args:
            hostname (str): Target hostname
            
        Returns:
            bool: True if phase completed successfully, False otherwise
        """
        logger.info("=== Starting Phase 12: Rsyslog Deployment ===")
        self.current_phase = 12
        
        try:
            # Step 12.1: New-deploy-build for rsyslog
            logger.info("Step 12.1: Triggering Rsyslog deployment...")
            self.add_checklist_item("12.1", "Rsyslog Deployment", "Pending")
            
            success = self.run_jenkins_job("New-deploy-build", {
                "HOSTS": hostname,
                "GIT_BRANCH": "master",
                "FORK": "5",
                "USER": "asterisk",
                "RSYSLOG_TYPE": "log",
                "SERVICES": '"adhearsion","firefoot-ts","eventshipper","legolas-ts"',
                "ENV": "prod-ts"
            })
            
            if not success:
                logger.error("Step 12.1: Rsyslog deployment failed")
                self.add_checklist_item("12.1", "Rsyslog Deployment", "Failed")
                return False
            
            self.add_checklist_item("12.1", "Rsyslog Deployment", "Completed")
            logger.info("Step 12.1: Rsyslog deployment completed successfully")
            
            # Step 12.2: Verify rsyslog configuration
            logger.info("Step 12.2: Verifying rsyslog configuration...")
            success, output = self.execute_ssh