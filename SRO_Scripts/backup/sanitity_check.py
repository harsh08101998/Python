#!/usr/bin/env python3
import subprocess
import sys
import argparse
import time


# python3 sanitiy_check.py 0731-1.exotel.in asterisk --port 22000 --ssh-password asterisk --sudo-password asterisk --skip-failed --check-only


def run_command_on_server(server_ip, username, port, command, ssh_password=None, use_sudo_password=False, sudo_password=None):
    """Execute command on remote server via SSH"""
    
    if ssh_password:
        # Use sshpass for SSH password authentication
        if use_sudo_password and sudo_password:
            ssh_command = [
                'sshpass', '-p', ssh_password, 'ssh', '-p', str(port), 
                '-o', 'StrictHostKeyChecking=no', 
                '{0}@{1}'.format(username, server_ip), 
                'echo "{0}" | sudo -S {1}'.format(sudo_password, command)
            ]
        else:
            ssh_command = [
                'sshpass', '-p', ssh_password, 'ssh', '-p', str(port), 
                '-o', 'StrictHostKeyChecking=no', 
                '{0}@{1}'.format(username, server_ip), 
                command
            ]
    else:
        # Use SSH key authentication
        if use_sudo_password and sudo_password:
            ssh_command = [
                'ssh', '-p', str(port), '-o', 'StrictHostKeyChecking=no', 
                '{0}@{1}'.format(username, server_ip), 
                'echo "{0}" | sudo -S {1}'.format(sudo_password, command)
            ]
        else:
            ssh_command = [
                'ssh', '-p', str(port), '-o', 'StrictHostKeyChecking=no', 
                '{0}@{1}'.format(username, server_ip), 
                command
            ]
    
    print("\n" + "="*60)
    print("Executing {} ".format(command))
    
    try:
        # Use Popen for maximum compatibility with old Python versions
        process = subprocess.Popen(
            ssh_command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        # Convert bytes to string for Python 3 compatibility
        if hasattr(stdout, 'decode'):
            stdout = stdout.decode('utf-8')
            stderr = stderr.decode('utf-8')
        
        if stdout:
            print("STDOUT:\n{0}".format(stdout))
        
        if stderr:
            print("STDERR:\n{0}".format(stderr))
            
        print("Return Code: {0}".format(process.returncode))
        
        # Check for common "service not found" errors
        stderr_lower = stderr.lower()
        if any(phrase in stderr_lower for phrase in ['unrecognized service', 'not found', 'no such file']):
            print("⚠️  Service not available on this server - SKIPPING")
            return True  # Treat as success to continue
        
        if process.returncode == 0:
            print("✅ Command executed successfully \n")
            print("="*60 + "\n")
            return True
        else:
            print("❌ Command failed\n")
            print("="*60 + "\n")
            return False
            
    except OSError as e:
        if ssh_password and 'No such file' in str(e):
            print("❌ Error: 'sshpass' not found. Please install sshpass or use SSH key authentication")
        else:
            print("❌ Error: SSH command failed - {0}".format(e))
        return False
    except Exception as e:
        print("❌ Error executing command: {0}".format(e))
        return False

def main():
    parser = argparse.ArgumentParser(description='Restart services on remote servers')
    parser.add_argument('server_ip', help='Server IP address')
    parser.add_argument('username', help='SSH username')
    parser.add_argument('--port', '-p', type=int, default=22000, help='SSH port (default: 22000)')
    parser.add_argument('--ssh-password', help='SSH login password (if not using SSH keys)')
    parser.add_argument('--sudo-password', help='Sudo password if required')
    parser.add_argument('--skip-failed', action='store_true', help='Continue even if commands fail')
    parser.add_argument('--check-only', action='store_true', help='Only check service status, do not restart')
    parser.add_argument('--restart-only', action='store_true', help='Only restart services, do not check status')
    
    args = parser.parse_args()
    
    # List of commands to execute
    if args.check_only:
        commands = [
            "hostname",
            "sudo service beanstalkd status",
            "sudo service dnsmasq status", 
            "sudo service rsyslog status",
            "sudo service squid status",
            "sudo service vsftpd status",
            "sudo service fail2ban status",
            "sudo service asterisk status",
            "sudo service legolas-ts status",
            "sudo service beanstalkd status",
            "sudo service dnsmasq status", 
            "sudo service rsyslog status",
            "sudo service squid status",
            "sudo service vsftpd status",
            "sudo service fail2ban status",
            "sudo service asterisk status",
            "sudo service legolas-ts status",
            "sudo service amix status",
            "sudo service eventshipper status",
            "sudo service causix status",
            "sudo service causixenqueuer status",
            "sudo service voipmonitor status",
            "sudo service fangorn status",
            "sudo service firefoot-ts status",
            "sudo service ahn status",
            "sudo service haproxy status",
            "sudo service mysqld status",
            "/opt/jruby-1.7.1/bin/jruby --version",
            "sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status"
        ]
    elif args.restart_only:
        commands = [
            "sudo service beanstalkd restart",
            "sudo service dnsmasq restart", 
            "sudo service rsyslog restart",
            "sudo service squid restart",
            "sudo service vsftpd restart",
            "sudo service fail2ban restart",
            "sudo service asterisk restart",
            "sudo service legolas-ts restart",
            "sudo service amix restart",
            "sudo service eventshipper restart",
            "sudo service causix restart",
            "sudo service causixenqueuer restart",
            "sudo service voipmonitor restart",
            "sudo service fangorn restart",
            "sudo service firefoot-ts restart",
            "sudo service ahn restart",
            "sudo service amix restart",
            "sudo service eventshipper restart",
            "sudo service causix restart",
            "sudo service causixenqueuer restart",
            "sudo service voipmonitor restart",
            "sudo service fangorn restart",
            "sudo service firefoot-ts restart",
            "sudo service ahn restart",
            "sudo service haproxy restart",
            "sudo service mysqld restart",
            "sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh restart"
        ]
    
    action = "status check" if args.check_only else "restart"
    print("🚀 Starting service {0} automation on server: {1}:{2}".format(action, args.server_ip, args.port))
    print("👤 Username: {0}".format(args.username))
    print("📝 Total commands to execute: {0}".format(len(commands)))
    
    if args.ssh_password:
        print("🔑 Using SSH password authentication")
    else:
        print("🔑 Using SSH key authentication")
    
    failed_commands = []
    successful_commands = []
    
    for i, command in enumerate(commands, 1):
        print("\n📋 Step {0}/{1}".format(i, len(commands)))
        
        success = run_command_on_server(
            args.server_ip, 
            args.username, 
            args.port,
            command,
            ssh_password=args.ssh_password,
            use_sudo_password=(args.sudo_password is not None),
            sudo_password=args.sudo_password
        )
        
        if success:
            successful_commands.append(command)
        else:
            failed_commands.append(command)
            if not args.skip_failed:
                print("\n❌ Stopping execution due to failed command: {0}".format(command))
                break
        
        # Small delay between commands
        time.sleep(1)
    
    # Summary
    print("\n" + "="*80)
    print("📊 EXECUTION SUMMARY")
    print("="*80)
    print("✅ Successful commands: {0}".format(len(successful_commands)))
    print("❌ Failed commands: {0}".format(len(failed_commands)))
    
    if successful_commands:
        print("\n✅ SUCCESSFUL COMMANDS:")
        for cmd in successful_commands:
            print("   ✓ {0}".format(cmd))
    
    if failed_commands:
        print("\n❌ FAILED COMMANDS:")
        for cmd in failed_commands:
            print("   ✗ {0}".format(cmd))
        
        sys.exit(1)  # Exit with error code for Jenkins
    else:
        print("\n🎉 All commands completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()