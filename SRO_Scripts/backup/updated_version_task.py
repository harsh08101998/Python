import paramiko
import os
import time
import csv
import sys
from datetime import datetime
import linux_command_output
import ahn_installation

# Task definitions and global variables
HOST = "192.168.64.3"
global_username = "root"
global_password = "redhat"
port = 22
JENKINS_URL = "https://build.corp.exotel.in:8080"
USERNAME = "harsh_kumar"
API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"
SILLYIO_CODE = ''

# Initialize logging
log_file = f"task_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
csv_file = f"task_checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def log_output(message, task_name="", status="INFO"):
    """Log output to both file and terminal"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{status}] {task_name}: {message}"
    
    # Print to terminal (real-time)
    print(log_message)
    sys.stdout.flush()
    
    # Write to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def create_csv_checklist():
    """Create CSV file with task checklist"""
    tasks = [
        {"Task": "Task 1", "Description": "Check DNS entries", "Status": "Pending"},
        {"Task": "Task 2", "Description": "Jenkins Job - ts-ami-setup-build-prod", "Status": "Pending"},
        {"Task": "Task 3", "Description": "Jenkins Job - ts_base_ami playbook", "Status": "Pending"},
        {"Task": "Task 4", "Description": "Execute commands on remote server", "Status": "Pending"},
        {"Task": "Task 5", "Description": "Jenkins Job - ts_environmental_setup", "Status": "Pending"},
        {"Task": "Task 6", "Description": "Jenkins Job - ts_services_setup", "Status": "Pending"},
        {"Task": "Task 7", "Description": "Jenkins Job - ts_telegraf_installation", "Status": "Pending"},
        {"Task": "Task 8", "Description": "Jenkins Job - monitoring-scripts-build", "Status": "Pending"},
        {"Task": "Task 9", "Description": "Jenkins Job - monitoring-scripts-deploy-ts", "Status": "Pending"},
        {"Task": "Task 10", "Description": "Install Asterisk 9-C7", "Status": "Pending"},
        {"Task": "Task 11", "Description": "Jenkins Job - legolas-ts-build-prod", "Status": "Pending"},
        {"Task": "Task 12", "Description": "Jenkins Job - legolas-ts-deploy-prod1", "Status": "Pending"},
        {"Task": "Task 13", "Description": "Jenkins Job - ts_gracefulstartstop_deploy", "Status": "Pending"},
        {"Task": "Task 14", "Description": "Install Adhearsion 29-C7", "Status": "Pending"},
        {"Task": "Task 15", "Description": "Install Firefoot-ts 7-C7", "Status": "Pending"},
        {"Task": "Task 16", "Description": "Install Amix 12-C7", "Status": "Pending"},
        {"Task": "Task 17", "Description": "Install Eventshipper 8-C7", "Status": "Pending"},
        {"Task": "Task 18", "Description": "Install Causix 5-C7", "Status": "Pending"},
        {"Task": "Task 19", "Description": "Install Causixenqueuer 2-C7", "Status": "Pending"},
        {"Task": "Task 20", "Description": "Install Route-switcher 11-C7", "Status": "Pending"},
        {"Task": "Task 21", "Description": "Install Voipmonitor 21-C7", "Status": "Pending"},
        {"Task": "Task 22", "Description": "Install Fangorn 14-C7", "Status": "Pending"},
        {"Task": "Task 23", "Description": "Install Traffic-shaper 1-C7", "Status": "Pending"}
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Task", "Description", "Status", "Start_Time", "End_Time", "Duration", "Notes"])
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)
    
    log_output(f"Created CSV checklist: {csv_file}")

def update_task_status(task_number, status, start_time=None, end_time=None, duration=None, notes=""):
    """Update task status in CSV file"""
    import csv
    from datetime import datetime
    
    # Read existing data
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Task"] == f"Task {task_number}":
                row["Status"] = status
                if start_time:
                    row["Start_Time"] = start_time
                if end_time:
                    row["End_Time"] = end_time
                if duration:
                    row["Duration"] = duration
                if notes:
                    row["Notes"] = notes
            rows.append(row)
    
    # Write updated data
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Task", "Description", "Status", "Start_Time", "End_Time", "Duration", "Notes"])
        writer.writeheader()
        writer.writerows(rows)

def task_1():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Please let us know if you have checked for DNS entries in /etc/resolv.conf file \n And yum is working, if yum is not working, then update the BaseURL file in /etc/yum.repos.d")
    task_value = input("If completed, please enter 'yes': ")

    if task_value == "yes":
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        print("DNS entries are checked and yum is working")
        update_task_status(1, "SUCCESS", start_time, end_time, duration)
        return True
    else:
        print("DNS entries are not checked and yum is not working")
    return task_value

def task_2():
    """Execute Jenkins Job for ts-ami-setup-build"""
    task_name = "Task 2"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts-ami-setup-build-prod", task_name)
    update_task_status(2, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-setup-build-prod"
        parameter_list = {
            "PROD_GIT_BRANCH": "feat/ts-centos-7-changes-updated"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(2, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(2, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_3():
    """Execute Jenkins Job for ts_base_ami playbook"""
    task_name = "Task 3"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_base_ami playbook", task_name)
    update_task_status(3, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_base_ami",
            "GIT_BRANCH": "feat/ts-centos-7-changes-updated",
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(3, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(3, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_4():
    """Execute commands on remote server"""
    task_name = "Task 4"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting remote server commands execution", task_name)
    update_task_status(4, "Running", start_time)
    
    try:
        commands = [
            "sudo reboot now",
            "sudo service sshd status",
            "grep -E 'asterisk|exomon|recotrix' /etc/passwd",
            "grep \"exotel@prod-build-node\" /home/asterisk/.ssh/authorized_keys ; grep \"exotel@Cron-Machine2\" /home/asterisk/.ssh/authorized_keys",
            "ll /home/asterisk/.ssh ; ll /home/exomon/.ssh ; ll -a /home/asterisk/",
            "cat /home/asterisk/.aws/credentials && cat /root/.aws/credential",
            "sudo service fail2ban status",
            "grep -i \"22000\" /etc/ssh/sshd_config"
        ]
        
        for i, cmd in enumerate(commands, 1):
            log_output(f"Executing command {i}: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command {i} output: {executing_linux_command_output}", task_name)
            
            if cmd == 'sudo reboot now':
                log_output('Rebooting the server, it will take few seconds to complete', task_name)
                time.sleep(100)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(4, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(4, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_5():
    """Execute Jenkins Job for ts_environmental_setup"""
    task_name = "Task 5"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_environmental_setup", task_name)
    update_task_status(5, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_environmental_setup",
            "GIT_BRANCH": "feat/ts-centos-7-changes-updated",
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        # Execute additional commands
        commands = [
            "/opt/jruby-1.7.1/bin/jruby --version",
            "sudo service mysqld status"
        ]
        
        log_output("Executing additional commands", task_name)
        for i, cmd in enumerate(commands, 1):
            log_output(f"Executing command {i}: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command {i} output: {executing_linux_command_output}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(5, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(5, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_6():
    """Execute Jenkins Job for ts_services_setup"""
    task_name = "Task 6"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_services_setup", task_name)
    update_task_status(6, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_services_setup",
            "GIT_BRANCH": "feat/ts-centos-7-changes-updated",
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        # Execute service status commands
        commands = [
            "sudo status beanstalkd",
            "sudo service dnsmasq status",
            "sudo service rsyslog status",
            "sudo service squid status",
            "sudo service vsftpd status",
            "sudo service fail2ban status"
        ]
        
        log_output("Checking service status", task_name)
        for i, cmd in enumerate(commands, 1):
            log_output(f"Executing command {i}: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command {i} output: {executing_linux_command_output}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(6, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(6, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_7():
    """Execute Jenkins Job for ts_telegraf_installation"""
    task_name = "Task 7"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_telegraf_installation", task_name)
    update_task_status(7, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_telegraf_installtion",
            "GIT_BRANCH": "feat/ts-centos-7-changes-updated",
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(7, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(7, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_8():
    """Execute Jenkins Job for monitoring-scripts-build"""
    task_name = "Task 8"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-build", task_name)
    update_task_status(8, "Running", start_time)
    
    try:
        JOB_NAME = "monitoring-scripts-build"
        parameter_list = {
            "GIT_BRANCH": "master",
            "NAGIOS_DNS_NAME": "nagios.internal.exotel.in"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(8, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(8, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_9():
    """Execute Jenkins Job for monitoring-scripts-deploy-ts"""
    task_name = "Task 9"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-deploy-ts", task_name)
    update_task_status(9, "Running", start_time)
    
    try:
        JOB_NAME = "monitoring-scripts-deploy-ts"
        VERSION = input("Enter the version number: ")
        parameter_list = {
            "HOST": HOST,
            "BRANCH": "master",
            "VERSION": VERSION,
            "ENV": "prod"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(9, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(9, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_10():
    """Install Asterisk 9-C7"""
    task_name = "Task 10"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Asterisk 9-C7 installation", task_name)
    update_task_status(10, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push"
        parameter_list = {
            "SERVICE": "asterisk",
            "ANS_VERSION": "9-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": "master"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        # Check asterisk status
        commands = ["sudo service asterisk status"]
        for cmd in commands:
            log_output(f"Executing command: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command output: {executing_linux_command_output}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(10, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(10, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_11():
    """Execute Jenkins Job for legolas-ts-build-prod"""
    task_name = "Task 11"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-build-prod", task_name)
    update_task_status(11, "Running", start_time)
    
    try:
        JOB_NAME = "legolas-ts/legolas-ts-build-prod"
        parameter_list = {
            "ENV": "prod",
            "GIT_BRANCH": "master"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(11, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(11, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_12():
    """Execute Jenkins Job for legolas-ts-deploy-prod1"""
    task_name = "Task 12"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-deploy-prod1", task_name)
    update_task_status(12, "Running", start_time)
    
    try:
        JOB_NAME = "legolas-ts/legolas-ts/legolas-ts-deploy-prod1"
        parameter_list = {
            "ANS_VERSION": "5-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "GIT_BRANCH": "master"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        # Check legolas-ts status
        commands = ["sudo service legolas-ts status"]
        for cmd in commands:
            log_output(f"Executing command: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command output: {executing_linux_command_output}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(12, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(12, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_13():
    """Execute Jenkins Job for ts_gracefulstartstop_deploy"""
    task_name = "Task 13"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_gracefulstartstop_deploy", task_name)
    update_task_status(13, "Running", start_time)
    
    try:
        JOB_NAME = "ts_gracefulstartstop_deploy"
        parameter_list = {
            "HOSTS": HOST,
            "GIT_BRANCH": "master"
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        # Check gracefulrestart.sh script
        commands = ["ls /home/asterisk/"]
        for cmd in commands:
            log_output(f"Executing command: {cmd}", task_name)
            executing_linux_command_output = linux_command_output.run_remote_command(HOST, global_username, global_password, cmd, port)
            log_output(f"Command output: {executing_linux_command_output}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(13, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(13, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_14():
    """Install Adhearsion 29-C7"""
    task_name = "Task 14"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Adhearsion 29-C7 installation", task_name)
    update_task_status(14, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "adhearsion",
            "ANS_VERSION": "29-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(14, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(14, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_15():
    """Install Firefoot-ts 7-C7"""
    task_name = "Task 15"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Firefoot-ts 7-C7 installation", task_name)
    update_task_status(15, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "firefoot-ts",
            "ANS_VERSION": "7-C7",
            "VERSION": "latest",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(15, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(15, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_16():
    """Install Amix 12-C7"""
    task_name = "Task 16"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Amix 12-C7 installation", task_name)
    update_task_status(16, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "amix",
            "ANS_VERSION": "12-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(16, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(16, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_17():
    """Install Eventshipper 8-C7"""
    task_name = "Task 17"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Eventshipper 8-C7 installation", task_name)
    update_task_status(17, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "eventshipper",
            "ANS_VERSION": "8-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(17, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(17, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_18():
    """Install Causix 5-C7"""
    task_name = "Task 18"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causix 5-C7 installation", task_name)
    update_task_status(18, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "causix",
            "ANS_VERSION": "5-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(18, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(18, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_19():
    """Install Causixenqueuer 2-C7"""
    task_name = "Task 19"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causixenqueuer 2-C7 installation", task_name)
    update_task_status(19, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "causixenqueuer",
            "ANS_VERSION": "2-C7",
            "VERSION": "latest",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_20():
    """Install Route-switcher 11-C7"""
    task_name = "Task 20"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Route-switcher 11-C7 installation", task_name)
    update_task_status(20, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        ahn_git_branch = "master"
        
        parameter_list = {
            "SERVICE": "route-switcher",
            "ANS_VERSION": "11-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": ahn_git_branch
        }
        
        executing_jenkins_job = ahn_installation.main(parameter_list, JOB_NAME)
        log_output(f"Jenkins job result: {executing_jenkins_job}", task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output(f"Error: {e}", task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "FAILED", start_time, end_time, duration, str(e))
        return False

# Main execution function
def main():
    """Main function to execute tasks"""
    log_output("Starting task execution", "MAIN")
    create_csv_checklist()
    
    # Get task range from user
    task_start_number = int(input("Enter the Task start number: "))
    task_end_number = int(input("Enter the Task end number: "))
    
    log_output(f"Executing tasks from {task_start_number} to {task_end_number}", "MAIN")
    
    for i in range(task_start_number, task_end_number + 1):
        function_name = f"task_{i}"
        
        if function_name in globals():
            log_output(f"Preparing to execute {function_name}", "MAIN")
            print(f"\nGoing to execute {function_name}\nPlease press y to continue, n to skip, or c to cancel (y/n/c): ")
            choice = input().lower()
            
            if choice == 'y':
                try:
                    globals()[function_name]()
                    log_output(f"{function_name} completed", "MAIN")
                except Exception as e:
                    log_output(f"Error in {function_name}: {e}", "MAIN", "ERROR")
            elif choice == 'n':
                log_output(f"Skipping {function_name}", "MAIN")
                update_task_status(i, "SKIPPED")
            elif choice == 'c':
                log_output("Cancelling the script", "MAIN")
                break
            else:
                log_output("Invalid choice, cancelling", "MAIN")
                break
        else:
            log_output(f"Function {function_name} not found", "MAIN", "ERROR")
    
    log_output("Task execution completed", "MAIN")
    log_output(f"Log file: {log_file}", "MAIN")
    log_output(f"CSV checklist: {csv_file}", "MAIN")

if __name__ == "__main__":
    main()