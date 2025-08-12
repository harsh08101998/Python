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


# Task definitions and global variables
HOST = "080-33.exotel.in"
global_username = "asterisk"
# global_password = "P*ot1l@rty123"
port = 22000
JENKINS_URL = "https://build.corp.exotel.in:8080"
USERNAME = "harsh_kumar"
API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"
SILLYIO_CODE = '080_33'
global_key_file = "centos.pem"  # Update with your actual key file path



######################################################### All Branch Names #########################################################

branch_ts_ami_setup = "feat/ts-centos-7-changes-updated-new"
branch_ts_base_ami = "feat/ts-centos-7-changes-updated-new"
branch_ts_environmental_setup = "feat/ts-centos-7-changes-updated-new"
branch_ts_services_setup = "feat/ts-centos-7-changes-updated-new"
branch_ts_telegraf_installation = "feat/ts-centos-7-changes-updated-new"
branch_monitoring_scripts_build = "feat/ts-centos-7-changes-updated-new"
branch_monitoring_scripts_deploy_ts = "feat/ts-centos-7-changes-updated-new"
branch_asterisk="master"
branch_legolas_ts_build="master"
branch_legolas_ts_deploy="master"
branch_ts_gracefulstartstop_deploy="master"
branch_firefoot_ts="master"
branch_amix="master"
branch_eventshipper="master"
branch_rsyslog="master"
branch_causix="master"
branch_causixenqueuer="master"
branch_route_switcher="master"
branch_voipmonitor="master"
branch_fangorn="master"
branch_traffic_shaper="master"


tasks_list = [
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
        {"Task": "Task 22", "Description": "Install Causixenqueuer 2-C7", "Status": "Pending"},
        {"Task": "Task 23", "Description": "Install Fangorn 14-C7", "Status": "Pending"},
        {"Task": "Task 24", "Description": "Install Voipmonitor 21-C7", "Status": "Pending"},
        {"Task": "Task 25", "Description": "Install Traffic-shaper 1-C7", "Status": "Pending"}


    ]


######################################################### Jenkins Job Definitions #########################################################

def trigger_jenkins_job(params,JOB_NAME):
    build_url = "{}/job/{}/buildWithParameters".format(JENKINS_URL, JOB_NAME)
    urll="{}/job/{}".format(JENKINS_URL, JOB_NAME)
    print("\n\n",urll,"\n\n")
    response = requests.post(
        build_url,
        params=params,
        auth=HTTPBasicAuth(USERNAME, API_TOKEN),
        verify=False
    )
    if response.status_code in [201, 200]:
        print("Job triggered with params: {}".format(params))
        # Get queue item URL from headers
        queue_url = response.headers.get('Location')
        return queue_url
    else:
        print("Failed to trigger job: {} {}".format(response.status_code, response.text))
        return None

def get_build_number(queue_url):
    # Poll the queue item until it gets a build number
    while True:
        r = requests.get("{}api/json".format(queue_url), auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'executable' in data and 'number' in data['executable']:
                return data['executable']['number']
            elif 'cancelled' in data and data['cancelled']:
                print("Job was cancelled in queue.")
                return None
        time.sleep(2)

def wait_for_build(jenkins_url, job_name, build_number):
    build_url = "{}/job/{}/{}/api/json".format(jenkins_url, job_name, build_number)
    while True:
        r = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        if r.status_code == 200:
            data = r.json()
            if data['building']:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Build {} is still running... {}".format(build_number, timestamp))
                
                
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Build {} finished with result: {} {}".format(build_number, data['result'], timestamp))
                log_url = "{}/job/{}/{}/consoleText".format(jenkins_url,job_name,build_number)
                print("\nFetching Jenkins console log from: {}\n".format(log_url))
                response = requests.get(log_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
                if response.status_code == 200:
                    print("=== Jenkins Console Log Start ===")
                    print(response.text)
                    print("=== Jenkins Console Log End ===\n\n\n\n\n")
                else:
                    print("Failed to fetch console log: {} {}".format(response.status_code, response.text))

                return data['result']
        else:
            print("Error fetching build status: {}".format(r.status_code))
        time.sleep(15)


def jenkins_job_trigger(params,JOB_NAME):
    # params=sys.argv[1]
    JOB_NAME = JOB_NAME
    params=params
    
    # Handle single parameter dictionary or list of parameter dictionaries
    if isinstance(params, dict):
        params_list = [params]
    else:
        params_list = params
    
    for param_set in params_list:
        queue_url = trigger_jenkins_job(param_set,JOB_NAME)
        if not queue_url:
            print("Skipping to next parameter set due to trigger failure.")
            continue
        print("Waiting for job to start (queue URL: {})...".format(queue_url))
        build_number = get_build_number(queue_url)
        if not build_number:
            print("No build number found, skipping to next.")
            continue
        print("Build started: {}. Waiting for completion...".format(build_number))
        result = wait_for_build(JENKINS_URL, JOB_NAME, build_number)
        print("Build {} result: {}".format(build_number, result))
        if result != "SUCCESS":
            print("Stopping further runs due to failure.")
            break

######################################################### Jenkins Job Definitions END #########################################################


######################################################### Linux Command Definitions #########################################################

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
        
        print("🔐 Connecting to {}@{} using SSH key...".format(username, host))
        
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
        print("--------- Executing: {} ---------".format(command))
        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
        
        # Get output
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        exit_status = stdout.channel.recv_exit_status()
        
        # Close connection
        ssh.close()
        
        if exit_status == 0:
            print("✓ Command executed successfully \n\n")
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

######################################################### Linux Command Definitions END #########################################################




# Initialize logging
log_file = "task_execution_{}.log".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
csv_file = "task_checklist_{}.csv".format(datetime.now().strftime('%Y%m%d_%H%M%S'))

def log_output(message, task_name="", status="INFO"):
    """Log output to both file and terminal"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = "[{}] [{}] {}: {}".format(timestamp, status, task_name, message)
    
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
        {"Task": "Task 22", "Description": "Install Causixenqueuer 2-C7", "Status": "Pending"},
        {"Task": "Task 23", "Description": "Install Fangorn 14-C7", "Status": "Pending"},
        {"Task": "Task 24", "Description": "Install Voipmonitor 21-C7", "Status": "Pending"},
        {"Task": "Task 25", "Description": "Install Traffic-shaper 1-C7", "Status": "Pending"}


    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Task", "Description", "Status", "Start_Time", "End_Time", "Duration", "Notes"])
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)
    
    log_output("Created CSV checklist: {}".format(csv_file))

def update_task_status(task_number, status, start_time=None, end_time=None, duration=None, notes=""):
    """Update task status in CSV file"""
    
    
    # Read existing data
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Task"] == "Task {}".format(task_number):
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
    print("============================ Task 1 ============================\n\n")
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
    print("============================ Task 2 ============================\n\n")
    """Execute Jenkins Job for ts-ami-setup-build"""
    task_name = "Task 2"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts-ami-setup-build-prod", task_name)
    update_task_status(2, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-setup-build-prod"
        parameter_list = {
            "PROD_GIT_BRANCH": branch_ts_ami_setup
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(2, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(2, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_3():
    print("============================ Task 3 ============================\n\n")
    """Execute Jenkins Job for ts_base_ami playbook"""
    task_name = "Task 3"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_base_ami playbook", task_name)
    update_task_status(3, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_base_ami",
            "GIT_BRANCH": branch_ts_base_ami,
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }

        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(3, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(3, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_4():
    print("============================ Task 4 ============================\n\n")
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
            log_output("Executing command {}: {}".format(i, cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
            
        
            if cmd == 'sudo reboot now':
                log_output('Rebooting the server, it will take few seconds to complete', task_name)
                time.sleep(100)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(4, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(4, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_5():
    print("============================ Task 5 ============================\n\n")
    """Execute Jenkins Job for ts_environmental_setup"""
    task_name = "Task 5"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_environmental_setup", task_name)
    update_task_status(5, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_environmental_setup",
            "GIT_BRANCH": branch_ts_environmental_setup,
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        # Execute additional commands
        commands = [
            "/opt/jruby-1.7.1/bin/jruby --version",
            "sudo service mysqld status"
        ]
        
        print('\n\nExpected output: The version should be 1.7 for jruby and mysqld should be running\n\n')
        log_output("Executing additional commands", task_name)
        for i, cmd in enumerate(commands, 1):
            log_output("Executing command {}: {}".format(i, cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(5, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(5, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_6():
    print("\n\n============================ Task 6 ============================\n\n")
    """Execute Jenkins Job for ts_services_setup"""
    task_name = "Task 6"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_services_setup", task_name)
    update_task_status(6, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_services_setup",
            "GIT_BRANCH": branch_ts_services_setup,
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        # Execute service status commands
        commands = [
            "sudo status beanstalkd",
            "sudo service dnsmasq status",
            "sudo service rsyslog status",
            "sudo service squid status",
            "sudo service vsftpd status",
            "sudo service fail2ban status"
        ]

        print('Expect squid - (Ignore if it stopped - It will be fine after squid upgrade) and \n fail2ban -(Ignore if it stopped - It will be fine after asterisk deployment) \n all services should be running \n')
        
        log_output("Checking service status", task_name)
        for i, cmd in enumerate(commands, 1):
            log_output("Executing command {}: {}".format(i, cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(6, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(6, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_7():
    print("\n\n============================ Task 7 ============================\n\n")
    """Execute Jenkins Job for ts_telegraf_installation"""
    task_name = "Task 7"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_telegraf_installation", task_name)
    update_task_status(7, "Running", start_time)
    
    try:
        JOB_NAME = "ts-ami-deploy"
        parameter_list = {
            "PLAYBOOK": "ts_telegraf_installtion",
            "GIT_BRANCH": branch_ts_telegraf_installation,
            "HOST": HOST,
            "SSH_USER_NAME": global_username,
            "SSH_PASSWORD": global_password,
            "SILLYIO_CODE": SILLYIO_CODE
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(7, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(7, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_8():
    print("\n\n============================ Task 8 ============================\n\n")
    """Execute Jenkins Job for monitoring-scripts-build"""
    task_name = "Task 8"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-build", task_name)
    update_task_status(8, "Running", start_time)
    
    try:
        JOB_NAME = "monitoring-scripts-build"
        parameter_list = {
            "GIT_BRANCH": branch_monitoring_scripts_build,
            "NAGIOS_DNS_NAME": "nagios.internal.exotel.in"
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(8, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(8, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_9():
    print("============================ Task 9 ============================\n\n")
    """Execute Jenkins Job for monitoring-scripts-deploy-ts"""
    task_name = "Task 9"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-deploy-ts", task_name)
    update_task_status(9, "Running", start_time)
    
    try:
        JOB_NAME = "monitoring-scripts-deploy-ts"
        print("Get it from monitoring-scripts-build , click the last build , scroll down and take the version number. Look for something like monitoring-scripts/prod/monitoring-scripts-458.tar.gz . So the version number is 458 \n")

        VERSION = input("Enter the version number: ")
        parameter_list = {
            "HOST": HOST,
            "BRANCH": branch_monitoring_scripts_deploy_ts,
            "VERSION": VERSION,
            "ENV": "prod"
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(9, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(9, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_10():
    print("\n\n============================ Task 10 ============================\n\n")
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
            "GIT_BRANCH": branch_asterisk
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        # Check asterisk status
        commands = ["sudo service asterisk status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(10, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(10, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_11():
    print("\n\n============================ Task 11 ============================\n\n")
    """Execute Jenkins Job for legolas-ts-build-prod"""
    task_name = "Task 11"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-build-prod", task_name)
    update_task_status(11, "Running", start_time)
    
    try:
        JOB_NAME = "legolas-ts/job/legolas-ts-build-prod"
        parameter_list = {
            "ENV": "prod",
            "GIT_BRANCH": branch_legolas_ts_build
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(11, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(11, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_12():
    print("\n\n============================ Task 12 ============================\n\n")
    """Execute Jenkins Job for legolas-ts-deploy-prod1"""
    task_name = "Task 12"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-deploy-prod1", task_name)
    update_task_status(12, "Running", start_time)
    
    try:
        JOB_NAME = "legolas-ts/job/legolas-ts-deploy-prod1"
        parameter_list = {
            "ANS_VERSION": "5-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "GIT_BRANCH": branch_legolas_ts_deploy
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        # Check legolas-ts status
        commands = ["sudo service legolas-ts status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(12, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(12, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_13():
    print("\n\n============================ Task 13 ============================\n\n")
    """Execute Jenkins Job for ts_gracefulstartstop_deploy"""
    task_name = "Task 13"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_gracefulstartstop_deploy", task_name)
    update_task_status(13, "Running", start_time)
    
    try:
        JOB_NAME = "ts_gracefulstartstop_deploy"
        parameter_list = {
            "HOSTS": HOST,
            "GIT_BRANCH": branch_ts_gracefulstartstop_deploy
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        # Check gracefulrestart.sh script
        commands = ["ls /home/asterisk/"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(13, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(13, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_14():
    print("\n\n============================ Task 14 ============================\n\n")
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
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        commands = ["sudo service adhearsion status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(14, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(14, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_15():
    print("\n\n============================ Task 15 ============================\n\n")
    """Install Firefoot-ts 7-C7"""
    task_name = "Task 15"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Firefoot-ts 7-C7 installation", task_name)
    update_task_status(15, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "firefoot-ts",
            "ANS_VERSION": "7-C7",
            "VERSION": "latest",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_firefoot_ts
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        commands = ["sudo service firefoot-ts status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(15, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(15, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_16():
    print("\n\n============================ Task 16 ============================\n\n")
    """Install Amix 12-C7"""
    task_name = "Task 16"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Amix 12-C7 installation", task_name)
    update_task_status(16, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "amix",
            "ANS_VERSION": "12-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_amix
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)

        commands = ["sudo service amix status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(16, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(16, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_17():
    print("\n\n============================ Task 17 ============================\n\n")
    """Install Eventshipper 8-C7"""
    task_name = "Task 17"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Eventshipper 8-C7 installation", task_name)
    update_task_status(17, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "eventshipper",
            "ANS_VERSION": "8-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_eventshipper
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(17, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(17, "FAILED", start_time, end_time, duration, str(e))
        return False


def task_18():
    print("\n\n============================ Task 18 ============================\n\n")
    """Install Rsyslog"""
    task_name = "Task 18"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Rsyslog  installation", task_name)
    update_task_status(18, "Running", start_time)
    
    try:
        JOB_NAME = "prod-rsyslog-deploy-C7 (centos 7 TS only)"
        
        parameter_list = {
            "HOSTS": HOST,
            "GIT_BRANCH": branch_rsyslog,
            "FORK": "5",
            "USER": "asterisk",
            "RSYSLOG_TYPE": "log",
            "SERVICES": '"adhearsion","firefoot-ts","eventshipper","legolas-ts"'
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        commands = [
        "grep mum1 /etc/rsyslog.d/logs.con",
        ".format()sudo sed -r 's/(.*) : false/echo \"\1\n false\"/ge' /opt/jruby-1.7.1/lib/ruby/gems/shared/gems/mongrel-1.1.5-java/lib/mongrel/handlers.rb > /opt/jruby-1.7.1/lib/ruby/gems/shared/gems/mongrel-1.1.5-java/lib/mongrel/handlers.rb_",
        "sudo mv /opt/jruby-1.7.1/lib/ruby/gems/shared/gems/mongrel-1.1.5-java/lib/mongrel/handlers.rb_ /opt/jruby-1.7.1/lib/ruby/gems/shared/gems/mongrel-1.1.5-java/lib/mongrel/handlers.rb"]

        #print("Expected output: It should show mumbai stamp rsyslog servers host entry  Target=".format()rsyslog.mum1.exotel.in"  Target="rsyslog.mum1.exotel.in" Target="rsyslog.mum1.exotel.in"  Target="rsyslog.mum1.exotel.in"\n')
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)

            
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(18, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(18, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_19():
    print("============================ Task 19 ============================\n\n")
    """Execute commands on remote server"""
    task_name = "Task 19"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting remote server commands execution", task_name)
    update_task_status(19, "Running", start_time)
    
    try:
        print("Executing Task 19_1  ( executing commands on remote server(python,pip,event,fail2ban,beanstalkd,dnsmasq,rsyslog,squid,vsftpd) ) ---------------------------------------------------\n\n")
        commands = [
        "python --version",
        "pip3.6 --version",
        "pip3.6 list",
        "uname -r",
        "ldconfig -p | grep event",
        "sudo service fail2ban status",
        "sudo status beanstalkd",
        "sudo service dnsmasq status",
        "sudo service rsyslog status",
        "sudo service squid status",
        "sudo service vsftpd status",
        "sudo service fail2ban status",
        "mkdir /var/log/exotel/recordings/causix_recordings"]

        print("Expected Output: Python 2.7.5 \n\n Expected Output: pip 20.3.4 from /usr/lib/python3.6/site-packages/pip (python 3.6) \n\n  Expected Output: The list should contain all the three modules  aws-cli, python-yaml, boto, botocore3: \n\n Expected Output: 3.10.0-1160.53.1.el7.x86_64\n\n Expected Output : Should list the version of event \n libevent_pthreads-2.0.so.5 (libc6,x86-64) => /lib64/libevent_pthreads-2.0.so.5 \n libevent_openssl-2.0.so.5 (libc6,x86-64) => /lib64/libevent_openssl-2.0.so.5 \n libevent_extra-2.0.so.5 (libc6,x86-64) => /lib64/libevent_extra-2.0.so.5 \n libevent_core-2.0.so.5 (libc6,x86-64) => /lib64/libevent_core-2.0.so.5 \n libevent-2.0.so.5 (libc6,x86-64) => /lib64/libevent-2.0.so.5 \n\n Expected Output: fail2ban should be running . If it is not running , start fail2ban \n\n [Ignore if it stopped - It will be fine after squid upgrade]")
        
        for i, cmd in enumerate(commands, 1):
            log_output("Executing command {}: {}".format(i, cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
            
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(19, "FAILED", start_time, end_time, duration, str(e))
        return False



def task_20():
    print("============================ Task 20 ============================\n\n")
    """Install Causix 5-C7"""
    task_name = "Task 20"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causix 5-C7 installation", task_name)
    update_task_status(20, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "causix",
            "ANS_VERSION": "5-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_causix
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(20, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(20, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_21():
    print("============================ Task 21 ============================\n\n")
    """Install Causixenqueuer 2-C7"""
    task_name = "Task 21"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causixenqueuer 2-C7 installation", task_name)
    update_task_status(21, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "causixenqueuer",
            "ANS_VERSION": "2-C7",
            "VERSION": "latest",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_causixenqueuer
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)

        commands = ["sudo service causix status","sudo status causixenqueuer"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(21, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(21, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_22():
    print("============================ Task 22 ============================\n\n")
    """Install Route-switcher 11-C7"""
    task_name = "Task 22"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Route-switcher 11-C7 installation", task_name)
    update_task_status(22, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "route-switcher",
            "ANS_VERSION": "11-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_route_switcher
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(22, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(22, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_23():
    print("============================ Task 23 ============================\n\n")
    """Install Voipmonitor 21-C7"""
    task_name = "Task 23"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Voipmonitor 21-C7 installation", task_name)
    update_task_status(23, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "voipmonitor",
            "ANS_VERSION": "21-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_voipmonitor
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)

        commands = ["sudo service voipmonitor status"]
        print("\nIt may fail at restart voipmonitor - that should be fine . Restart it manually if not running\n")
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(23, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(23, "FAILED", start_time, end_time, duration, str(e))
        return False

def task_24():
    print("============================ Task 24 ============================\n\n")
    """Install Fangorn 14-C7"""
    task_name = "Task 24"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Fangorn 14-C7 installation", task_name)
    update_task_status(24, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "fangorn",
            "ANS_VERSION": "14-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_fangorn
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)

        commands = ["sudo service fangorn status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(24, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(24, "FAILED", start_time, end_time, duration, str(e))
        return False


def task_25():
    print("============================ Task 25 ============================\n\n")
    """Install Traffic-shaper 1-C7"""
    task_name = "Task 25"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Traffic-shaper 1-C7 installation", task_name)
    update_task_status(25, "Running", start_time)
    
    try:
        JOB_NAME = "ts-code-push-C7"
        
        parameter_list = {
            "SERVICE": "traffic-shaper",
            "ANS_VERSION": "1-C7",
            "VERSION": "6-C7",
            "HOST": HOST,
            "EXTERNAL_VARS": "conftype=slave",
            "GIT_BRANCH": branch_traffic_shaper
        }
        
        executing_jenkins_job = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(executing_jenkins_job), task_name)

        commands = ["sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status"]
        for cmd in commands:
            log_output("Executing command: {}".format(cmd), task_name)
            executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
            log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(25, "SUCCESS", start_time, end_time, duration)
        return True
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        update_task_status(25, "FAILED", start_time, end_time, duration, str(e))
        return False

# Main execution function
def main():
    """Main function to execute tasks"""
    log_output("Starting task execution", "MAIN")
    create_csv_checklist()
    
    # Get task range from user
    task_start_number = int(input("Enter the Task start number: "))
    task_end_number = int(input("Enter the Task end number: "))
    
    log_output("Executing tasks from {} to {}".format(task_start_number, task_end_number), "MAIN")
    
    promptt=input("Do you want Prompt? (y/n): ")
    if promptt == 'y':
        for i in range(task_start_number, task_end_number + 1):
            function_name = "task_{}".format(i)
            function_name2 = tasks_list[i-1]["Description"]

            if function_name in globals():
                log_output("Preparing to execute {}".format(function_name), "MAIN")
                print("\nGoing to execute {} - {}\nPlease press y to continue, n to skip, or c to cancel (y/n/c): ".format(function_name,function_name2))
                choice = input().lower()

                if choice == 'y':
                    try:
                        globals()[function_name]()
                        log_output("{} completed".format(function_name), "MAIN")
                    except Exception as e:
                        log_output("Error in {}: {}".format(function_name, e), "MAIN", "ERROR")
                elif choice == 'n':
                    log_output("Skipping {}".format(function_name), "MAIN")
                    update_task_status(i, "SKIPPED")
                elif choice == 'c':
                    log_output("Cancelling the script", "MAIN")
                    break
                else:
                    log_output("Invalid choice, cancelling", "MAIN")
                    break
            else:
                log_output("Function {} not found".format(function_name), "MAIN", "ERROR")
    
    else:
        for i in range(task_start_number, task_end_number + 1):
            function_name = "task_{}".format(i)
            function_name2 = tasks_list[i-1]["Description"]
            if function_name in globals():
                log_output("Preparing to execute {}".format(function_name), "MAIN")
                globals()[function_name]()
                log_output("{} completed".format(function_name), "MAIN")
            else:
                log_output("Function {} not found".format(function_name), "MAIN", "ERROR")



    log_output("Task execution completed", "MAIN")
    log_output("Log file: {}".format(log_file), "MAIN")
    log_output("CSV checklist: {}".format(csv_file), "MAIN")

if __name__ == "__main__":
    main()