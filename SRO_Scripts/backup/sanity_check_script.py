import paramiko
import os
import time
import csv
import sys
from datetime import datetime


import requests
import time,sys
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = "080-33.exotel.in"
global_username = "asterisk"
# global_password = "P*ot1l@rty123"
port = 22000
global_key_file = "centos.pem"  # Update with your actual key file path




def run_remote_command(host, username, key_file_path, command, port):
    """Run command on remote server using SSH key authentication"""
    try:
        # Validate key file exists
        if not os.path.exists(key_file_path):
            print("❌ ERROR: SSH key file not found: {}".format(key_file_path))
            return False, "SSH key file not found"
        
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        
        # Load private key
        try:
            private_key = paramiko.RSAKey.from_private_key_file(key_file_path)
        except paramiko.PasswordRequiredException:
            print("❌ ERROR: SSH key requires a passphrase")
            return False, "SSH key requires passphrase"
        except Exception as e:
            print("❌ ERROR: Failed to load SSH key: {}".format(e))
            return False, "Failed to load SSH key"
        
        # Connect to server using key authentication
        ssh.connect(
            hostname=host,
            username=username,
            pkey=private_key,
            timeout=60,
            port=port
        )
        
        # Execute command
        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
        
        # Get output
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        exit_status = stdout.channel.recv_exit_status()
        
        # Close connection
        ssh.close()
        
        if exit_status == 0:
            print("✓ Command executed successfully ")
            return True, output
        else:
            print("✗ Command failed with exit status {} \n\n".format(exit_status))
            return False, error if error else output
            
    except paramiko.AuthenticationException:
        print("❌ SSH Authentication failed\n\n")
        ssh.close()
        return False, "SSH Authentication failed"
    except Exception as e:
        print("❌ Connection failed: {} \n\n".format(e))
        ssh.close()
        return False, str(e)


def task_4():
    """Execute commands on remote server"""
    
    print("Starting remote server commands execution")

    try:
        commands = [
            "sudo service sshd status",
            "grep -E 'asterisk|exomon|recotrix' /etc/passwd",
            "grep \"exotel@prod-build-node\" /home/asterisk/.ssh/authorized_keys ; grep \"exotel@Cron-Machine2\" /home/asterisk/.ssh/authorized_keys",
            "ll /home/asterisk/.ssh ; ll /home/exomon/.ssh ; ll -a /home/asterisk/",
            "cat /home/asterisk/.aws/credentials && cat /root/.aws/credential",
            "sudo service fail2ban status",
            "grep -i \"22000\" /etc/ssh/sshd_config",
            "sudo service beanstalkd status",
            "systemctl status beanstalkd",
            "sudo service dnsmasq status",
            "sudo service rsyslog status",
            "sudo service squid status",
            "sudo service vsftpd status",
            "sudo service fail2ban status",
            "sudo service asterisk status",
            "sudo service legolas-ts status",
            "sudo service amix status",
            "sudo service causix status",
            "sudo service causixenqueuer status",
            "sudo service ahn status",
            "sudo service eventshipper status",
            "sudo service voipmonitor status",
            "sudo service fangorn status",
            "sudo service firefoot-ts status",
            "sudo service haproxy status",
            "sudo service mysqld status",
            "sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status",
        ]
        
        for i, cmd in enumerate(commands, 1):
            print("\n\n --------------- Executing command {} :- {} --------------------------------- \n".format(i, cmd))
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            print("Command {} output: {}\n\n".format(i, executing_linux_command_output))
            
        
        return True
        
    except Exception as e:
        return False

task_4()