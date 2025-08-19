from math import ceil
import paramiko
import os
import time
import sys
from datetime import datetime
import argparse
import requests
import time,sys
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import socket


# Task definitions and global variables
# HOST = "080-33.exotel.in"
# global_username = "asterisk"
# global_password = "P*ot1l@rty123"
# port = 22000
JENKINS_URL = "https://build.corp.exotel.in:8080"
USERNAME = "harsh_kumar"
API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"
# SILLYIO_CODE = '080_33'
global_key_file = "/home/exotel/harsh/do_not_touch/centos.pem"  # Update with your actual key file path


  
  # python3 SRO_Scripts/whole_script_in_one.py \
# --task_1_branch_ts_ami_setup=feat/ts-centos-7-changes-updated-new \
# --task_2_branch_ts_base_ami=feat/ts-centos-7-changes-updated-new \
# --task_3_branch_ts_environmental_setup=feat/ts-centos-7-changes-updated-new \
# --task_4_branch_ts_services_setup=feat/ts-centos-7-changes-updated-new \
# --task_5_branch_ts_telegraf_installation=feat/ts-centos-7-changes-updated-new \
# --task_6_branch_monitoring_scripts_build=feat/ts-centos-7-changes-updated-new \
# --task_7_branch_monitoring_scripts_deploy_ts=feat/ts-centos-7-changes-updated-new \
# --task_8_branch_asterisk=master \
# --task_9_branch_legolas_ts_build=master \
# --task_10_branch_legolas_ts_deploy=master \
# --task_11_branch_ts_gracefulstartstop_deploy=master \
# --task_12_branch_adhearsion=master \
# --task_13_branch_firefoot_ts=master \
# --task_14_branch_amix=master \
# --task_15_branch_eventshipper=master \
# --task_16_branch_rsyslog=master \
# --task_17_branch_causix=master \
# --task_18_branch_causixenqueuer=master \
# --task_19_branch_route_switcher=master \
# --task_20_branch_voipmonitor=master \
# --task_21_branch_fangorn=master \
# --task_22_branch_traffic_shaper=master

######################################################### All Branch Names #########################################################

def parse_args():
    parser = argparse.ArgumentParser(description="Script for running Jenkins and server tasks with branch overrides.")

    # Task 1: Jenkins Job - ts-ami-setup-build-prod
    parser.add_argument('--task_1_branch_ts_ami_setup', default="feat/ts-centos-7-changes-updated-new", help="Task 1: Jenkins Job - ts-ami-setup-build-prod")
    # Task 2: Jenkins Job - ts_base_ami playbook
    parser.add_argument('--task_2_branch_ts_base_ami', default="feat/ts-centos-7-changes-updated-new", help="Task 2: Jenkins Job - ts_base_ami playbook")
    # Task 3: Jenkins Job - ts_environmental_setup
    parser.add_argument('--task_3_branch_ts_environmental_setup', default="feat/ts-centos-7-changes-updated-new", help="Task 3: Jenkins Job - ts_environmental_setup")
    # Task 4: Jenkins Job - ts_services_setup
    parser.add_argument('--task_4_branch_ts_services_setup', default="feat/ts-centos-7-changes-updated-new", help="Task 4: Jenkins Job - ts_services_setup")
    # Task 5: Jenkins Job - ts_telegraf_installation
    parser.add_argument('--task_5_branch_ts_telegraf_installation', default="feat/ts-centos-7-changes-updated-new", help="Task 5: Jenkins Job - ts_telegraf_installation")
    # Task 6: Jenkins Job - monitoring-scripts-build
    parser.add_argument('--task_6_branch_monitoring_scripts_build', default="feat/ts-centos-7-changes-updated-new", help="Task 6: Jenkins Job - monitoring-scripts-build")
    # Task 7: Jenkins Job - monitoring-scripts-deploy-ts
    parser.add_argument('--task_7_branch_monitoring_scripts_deploy_ts', default="feat/ts-centos-7-changes-updated-new", help="Task 7: Jenkins Job - monitoring-scripts-deploy-ts")
    # Task 8: Install Asterisk 9-C7
    parser.add_argument('--task_8_branch_asterisk', default="master", help="Task 8: Install Asterisk 9-C7")
    # Task 9: Jenkins Job - legolas-ts-build-prod
    parser.add_argument('--task_9_branch_legolas_ts_build', default="master", help="Task 9: Jenkins Job - legolas-ts-build-prod")
    # Task 10: Jenkins Job - legolas-ts-deploy-prod1
    parser.add_argument('--task_10_branch_legolas_ts_deploy', default="master", help="Task 10: Jenkins Job - legolas-ts-deploy-prod1")
    # Task 11: Jenkins Job - ts_gracefulstartstop_deploy
    parser.add_argument('--task_11_branch_ts_gracefulstartstop_deploy', default="master", help="Task 11: Jenkins Job - ts_gracefulstartstop_deploy")
    # Task 12: Install Adhearsion 29-C7
    parser.add_argument('--task_12_branch_adhearsion', default="master", help="Task 12: Install Adhearsion 29-C7")
    # Task 13: Install Firefoot-ts 7-C7
    parser.add_argument('--task_13_branch_firefoot_ts', default="master", help="Task 13: Install Firefoot-ts 7-C7")
    # Task 14: Install Amix 12-C7
    parser.add_argument('--task_14_branch_amix', default="master", help="Task 14: Install Amix 12-C7")
    # Task 15: Install Eventshipper 8-C7
    parser.add_argument('--task_15_branch_eventshipper', default="master", help="Task 15: Install Eventshipper 8-C7")
    # Task 16: Install Rsyslog
    parser.add_argument('--task_16_branch_rsyslog', default="master", help="Task 16: Install Rsyslog")
    # Task 17: Install Causix 5-C7
    parser.add_argument('--task_17_branch_causix', default="master", help="Task 17: Install Causix 5-C7")
    # Task 18: Install Causixenqueuer 2-C7
    parser.add_argument('--task_18_branch_causixenqueuer', default="master", help="Task 18: Install Causixenqueuer 2-C7")
    # Task 19: Install Route-switcher 11-C7
    parser.add_argument('--task_19_branch_route_switcher', default="master", help="Task 19: Install Route-switcher 11-C7")
    # Task 20: Install Voipmonitor 21-C7
    parser.add_argument('--task_20_branch_voipmonitor', default="master", help="Task 20: Install Voipmonitor 21-C7")
    # Task 21: Install Fangorn 14-C7
    parser.add_argument('--task_21_branch_fangorn', default="master", help="Task 21: Install Fangorn 14-C7")
    # Task 22: Install Traffic-shaper 1-C7
    parser.add_argument('--task_22_branch_traffic_shaper', default="master", help="Task 22: Install Traffic-shaper 1-C7")
    # Task 23: Jenkins Job - prod-prometheus-process-exporter-deploy
    parser.add_argument('--task_23_branch_prometheus_process_exporter', default="master", help="Task 23: Jenkins Job - prod-prometheus-process-exporter-deploy")
    # Task 24: Jenkins Job - prod-prometheus-node-exporter-deploy
    parser.add_argument('--task_24_branch_prometheus_node_exporter', default="master", help="Task 24: Jenkins Job - prod-prometheus-node-exporter-deploy")
    # Task 25: Jenkins Job - prometheus-asterisk-exporter-deploy
    parser.add_argument('--task_25_branch_prometheus_asterisk_exporter', default="master", help="Task 25: Jenkins Job - prometheus-asterisk-exporter-deploy")
    # Task 26: Jenkins Job - ts_logs_uploader_deploy
    parser.add_argument('--task_26_branch_ts_logs_uploader', default="master", help="Task 26: Jenkins Job - ts_logs_uploader_deploy")

    

    # General/global arguments
    parser.add_argument('--host', help="Target host for SSH and Jenkins jobs")
    parser.add_argument('--ssh_user', default="asterisk", help="SSH username")
    parser.add_argument('--ssh_password', default="P*ot1l@rty123", help="SSH password (if needed)")
    parser.add_argument('--ssh_port', type=int, default=22000, help="SSH port")
    parser.add_argument('--sillyio_code', default="080_33", help="SILLYIO_CODE value")
    parser.add_argument('--task_start_number', type=int, default=1, help="Task number to start execution from (inclusive)")
    parser.add_argument('--task_end_number', type=int, default=26, help="Task number to end execution at (inclusive)")

    return parser.parse_args()


# branch_ts_ami_setup = args.branch_ts_ami_setup
# branch_ts_base_ami = args.branch_ts_base_ami
# branch_ts_environmental_setup = args.branch_ts_environmental_setup
# branch_ts_services_setup = args.branch_ts_services_setup
# branch_ts_telegraf_installation = args.branch_ts_telegraf_installation
# branch_monitoring_scripts_build = args.branch_monitoring_scripts_build
# branch_monitoring_scripts_deploy_ts = args.branch_monitoring_scripts_deploy_ts
# branch_asterisk = args.branch_asterisk
# branch_legolas_ts_build = args.branch_legolas_ts_build
# branch_legolas_ts_deploy = args.branch_legolas_ts_deploy
# branch_ts_gracefulstartstop_deploy = args.branch_ts_gracefulstartstop_deploy
# branch_firefoot_ts = args.branch_firefoot_ts
# branch_amix = args.branch_amix
# branch_eventshipper = args.branch_eventshipper
# branch_rsyslog = args.branch_rsyslog
# branch_causix = args.branch_causix
# branch_causixenqueuer = args.branch_causixenqueuer
# branch_route_switcher = args.branch_route_switcher
# branch_voipmonitor = args.branch_voipmonitor
# branch_fangorn = args.branch_fangorn
# branch_traffic_shaper = args.branch_traffic_shaper


tasks_list = [
    {"Task": "Task 1", "Description": "Jenkins Job - ts-ami-setup-build-prod", "Status": "Pending"},
    {"Task": "Task 2", "Description": "Jenkins Job - ts_base_ami playbook", "Status": "Pending"},
    {"Task": "Task 3", "Description": "Jenkins Job - ts_environmental_setup", "Status": "Pending"},
    {"Task": "Task 4", "Description": "Jenkins Job - ts_services_setup", "Status": "Pending"},
    {"Task": "Task 5", "Description": "Jenkins Job - ts_telegraf_installation", "Status": "Pending"},
    {"Task": "Task 6", "Description": "Jenkins Job - monitoring-scripts-build", "Status": "Pending"},
    {"Task": "Task 7", "Description": "Jenkins Job - monitoring-scripts-deploy-ts", "Status": "Pending"},
    {"Task": "Task 8", "Description": "Install Asterisk 9-C7", "Status": "Pending"},
    {"Task": "Task 9", "Description": "Jenkins Job - legolas-ts-build-prod", "Status": "Pending"},
    {"Task": "Task 10", "Description": "Jenkins Job - legolas-ts-deploy-prod1", "Status": "Pending"},
    {"Task": "Task 11", "Description": "Jenkins Job - ts_gracefulstartstop_deploy", "Status": "Pending"},
    {"Task": "Task 12", "Description": "Install Adhearsion 29-C7", "Status": "Pending"},
    {"Task": "Task 13", "Description": "Install Firefoot-ts 7-C7", "Status": "Pending"},
    {"Task": "Task 14", "Description": "Install Amix 12-C7", "Status": "Pending"},
    {"Task": "Task 15", "Description": "Install Eventshipper 8-C7", "Status": "Pending"},
    {"Task": "Task 16", "Description": "Install Rsyslog", "Status": "Pending"},
    {"Task": "Task 17", "Description": "Install Causix 5-C7", "Status": "Pending"},
    {"Task": "Task 18", "Description": "Install Causixenqueuer 2-C7", "Status": "Pending"},
    {"Task": "Task 19", "Description": "Install Route-switcher 11-C7", "Status": "Pending"},
    {"Task": "Task 20", "Description": "Install Voipmonitor 21-C7", "Status": "Pending"},
    {"Task": "Task 21", "Description": "Install Fangorn 14-C7", "Status": "Pending"},
    {"Task": "Task 22", "Description": "Install Traffic-shaper 1-C7", "Status": "Pending"},
    {"Task": "Task 23", "Description": "Jenkins Job - prod-prometheus-process-exporter-deploy", "Status": "Pending"},
    {"Task": "Task 24", "Description": "Jenkins Job - prod-prometheus-node-exporter-deploy", "Status": "Pending"},
    {"Task": "Task 25", "Description": "Jenkins Job - prometheus-asterisk-exporter-deploy", "Status": "Pending"},
    {"Task": "Task 26", "Description": "Jenkins Job - ts_logs_uploader_deploy", "Status": "Pending"}
]


######################################################### Jenkins Job Definitions #########################################################

def trigger_jenkins_job(params, JOB_NAME, build_number=None):
    build_url = "{}/job/{}/buildWithParameters".format(JENKINS_URL, JOB_NAME)
    
    # If build_number is provided, construct URL with build number
    if build_number:
        urll = "{}/job/{}/{}".format(JENKINS_URL, JOB_NAME, build_number)
        print("\n\nJob URL with Build Number: {}\n\n".format(urll))
    else:
        urll = "{}/job/{}".format(JENKINS_URL, JOB_NAME)
        print("\n\nJob URL: {}\n\n".format(urll))
    
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
    console_logs = ""
    # Store the actual build URL (not the API URL)
    actual_build_url = "{}/job/{}/{}".format(jenkins_url, job_name, build_number)
    
    while True:
        r = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        if r.status_code == 200:
            data = r.json()
            if data['building']:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_output("Build {} is still running... {}".format(build_number, timestamp), "JENKINS", "INFO")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Build {} finished with result: {} {}".format(build_number, data['result'], timestamp))
                log_url = "{}/job/{}/{}/consoleText".format(jenkins_url,job_name,build_number)
                print("\nFetching Jenkins console log from: {}\n".format(log_url))
                response = requests.get(log_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
                if response.status_code == 200:
                    print("\n\n=== Jenkins Console Log Start ===\n")
                    print(response.text)
                    console_logs=response.text
                    print("=== Jenkins Console Log End ===\n\n\n\n\n")
                else:
                    print("Failed to fetch console log: {} {}".format(response.status_code, response.text))

                return data['result'], console_logs, actual_build_url
        else:
            print("Error fetching build status: {}".format(r.status_code))
        time.sleep(15)


def jenkins_job_trigger(params, JOB_NAME, build_number=None):
    # params=sys.argv[1]
    JOB_NAME = JOB_NAME
    params=params
    
    # Handle single parameter dictionary or list of parameter dictionaries
    if isinstance(params, dict):
        params_list = [params]
    else:
        params_list = params
    
    console_logs = ""
    build_url = ""
    any_started = False
    for param_set in params_list:
        queue_url = trigger_jenkins_job(param_set, JOB_NAME, build_number)
        if not queue_url:
            print("Skipping to next parameter set due to trigger failure.")
            continue
        print("Waiting for job to start (queue URL: {})...".format(queue_url))
        build_number = get_build_number(queue_url)
        if not build_number:
            print("No build number found, skipping to next.")
            continue
        any_started = True
        # Store the build URL
        build_url = "{}/job/{}/{}".format(JENKINS_URL, JOB_NAME, build_number)
        print("Build started: {}. Waiting for completion...".format(build_number))
        print("Build URL: {}".format(build_url))
        result, console_logs, build_url = wait_for_build(JENKINS_URL, JOB_NAME, build_number)
        print("Build {} result: {}".format(build_number, result))
        if result != "SUCCESS":
            print("Stopping further runs due to failure.")
            return result, console_logs, build_url
    
    if not any_started:
        return "FAILED", console_logs, ""
    return "SUCCESS", console_logs, build_url

######################################################### Jenkins Job Definitions END #########################################################


######################################################### Linux Command Definitions #########################################################

def run_remote_cmd(host, username, key_file_path, command, port=22):
    print("\n$ {}".format(command))
    if not os.path.exists(key_file_path):
        print("❌ ERROR: SSH key file not found: {}".format(key_file_path))
        return False, "", "SSH key file not found", 1
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_file_path)
        ssh.connect(hostname=host, username=username, pkey=private_key, port=port, timeout=60)
        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        rc = stdout.channel.recv_exit_status()
        ssh.close()
        success = rc == 0
        return success, out.strip(), err.strip(), rc
    except Exception as e:
        print("Exception: {}".format(e))
        return False, "", str(e), 1

######################################################### Linux Command Definitions END #########################################################




# Initialize logging
log_file = "task_execution_{}.log".format(datetime.now().strftime('%Y%m%d_%H%M%S'))

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

def print_task_summary(tasks_list):
    print("\n" + "="*40)
    print("TASK EXECUTION SUMMARY")
    print("="*40)
    for task in tasks_list:
        print(f"{task['Task']}: {task['Description']}")
        print(f"  Status: {task['Status']}")
        if task.get('Notes'):
            print(f"  Notes: {task['Notes']}")
        if task.get('BuildURL'):
            print(f"  Build URL: {task['BuildURL']}")
        print("-"*40)



def task_1():
    print("============================ Task 1 ============================\n\n")
    """Execute Jenkins Job for ts-ami-setup-build"""
    task_name = "Task 1"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts-ami-setup-build-prod", task_name)
    tasks_list[0]["Status"] = "Running"
    

    try:
        JOB_NAME = "ts-ami-setup-build-prod"
        parameter_list = {
            "PROD_GIT_BRANCH": branch_ts_ami_setup
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[0]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[0]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[0]["Status"] = "ABORTED"
        else:
            tasks_list[0]["Status"] = "FAILED"
        return result == "SUCCESS"
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[0]["Status"] = "FAILED"
        return False

def wait_for_ssh(host, port, timeout=300, interval=10):
    """Wait for SSH port to be open on the host."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"SSH is up on {host}:{port}")
                return True
        except Exception:
            print(f"Waiting for SSH on {host}:{port}...")
            time.sleep(interval)
    print(f"Timeout waiting for SSH on {host}:{port}")
    return False

def task_2():
    print("============================ Task 2 ============================\n\n")
    """Execute Jenkins Job for ts_base_ami playbook"""
    task_name = "Task 2"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_base_ami playbook", task_name)
    tasks_list[1]["Status"] = "Running"
    
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

        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[1]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
   
        if result == "SUCCESS":
            tasks_list[1]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[1]["Status"] = "ABORTED"
        else:
            tasks_list[1]["Status"] = "FAILED"
        return result == "SUCCESS"
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[1]["Status"] = "FAILED"
        return False



def task_3():
    print("============================ Task 3 ============================\n\n")
    """Execute Jenkins Job for ts_environmental_setup"""
    task_name = "Task 3"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_environmental_setup", task_name)
    tasks_list[2]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[2]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Execute additional commands
        # commands = [
        #     "/opt/jruby-1.7.1/bin/jruby --version",
        #     "sudo service mysqld status"
        # ]
        
        # print('\n\nExpected output: The version should be 1.7 for jruby and mysqld should be running\n\n')
        # log_output("Executing additional commands", task_name)
        # for i, cmd in enumerate(commands, 1):
        #     log_output("Executing command {}: {}".format(i, cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[2]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[2]["Status"] = "ABORTED"
        else:
            tasks_list[2]["Status"] = "FAILED"
        return result == "SUCCESS"
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[2]["Status"] = "FAILED"
        return False

def task_4():
    print("\n\n============================ Task 4 ============================\n\n")
    """Execute Jenkins Job for ts_services_setup"""
    task_name = "Task 4"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_services_setup", task_name)
    tasks_list[3]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[3]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Execute service status commands
        # commands = [
        #     "sudo status beanstalkd",
        #     "sudo service dnsmasq status",
        #     "sudo service rsyslog status",
        #     "sudo service squid status",
        #     "sudo service vsftpd status",
        #     "sudo service fail2ban status"
        # ]

        # print('Expect squid - (Ignore if it stopped - It will be fine after squid upgrade) and \n fail2ban -(Ignore if it stopped - It will be fine after asterisk deployment) \n all services should be running \n')
        
        # log_output("Checking service status", task_name)
        # for i, cmd in enumerate(commands, 1):
        #     log_output("Executing command {}: {}".format(i, cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command {} output: {}".format(i, executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[3]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[3]["Status"] = "ABORTED"
        else:
            tasks_list[3]["Status"] = "FAILED"
        return result == "SUCCESS"
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[3]["Status"] = "FAILED"
        return False

def task_5():
    print("\n\n============================ Task 5 ============================\n\n")
    """Execute Jenkins Job for ts_telegraf_installation"""
    task_name = "Task 5"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_telegraf_installation", task_name)
    tasks_list[4]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[4]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[4]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[4]["Status"] = "ABORTED"
        else:
            tasks_list[4]["Status"] = "FAILED"
        return result == "SUCCESS"
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[4]["Status"] = "FAILED"
        return False

def task_6():
    print("\n\n============================ Task 6 ============================\n\n")
    """Execute Jenkins Job for monitoring-scripts-build"""
    task_name = "Task 6"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-build", task_name)
    tasks_list[5]["Status"] = "Running"
    
    try:
        JOB_NAME = "monitoring-scripts-build"
        parameter_list = {
            "GIT_BRANCH": branch_monitoring_scripts_build,
            "NAGIOS_DNS_NAME": "nagios.internal.exotel.in"
        }
        result, console_logs, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[5]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        import re
        matches = re.findall(r"monitoring-scripts-(\d+)\.tar\.gz", console_logs)
        version = matches[-1] if matches else None
        if version:
            log_output(f"Extracted version for Task 7: {version}", task_name)
        else:
            log_output("Could not extract version for Task 7!", task_name, "ERROR")

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))

        if result == "SUCCESS":
            tasks_list[5]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[5]["Status"] = "ABORTED"
        else:
            tasks_list[5]["Status"] = "FAILED"
        return result == "SUCCESS", version, build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[5]["Status"] = "FAILED"
        return False, None, None

def task_7(version=None):
    print("============================ Task 7 ============================\n\n")
    """Execute Jenkins Job for monitoring-scripts-deploy-ts"""
    task_name = "Task 7"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - monitoring-scripts-deploy-ts", task_name)
    tasks_list[6]["Status"] = "Running"
    
    try:
        JOB_NAME = "monitoring-scripts-deploy-ts"
        if not version:
            # fallback to prompt if not provided
            version = input("Enter the version number: ")
        parameter_list = {
            "HOST": HOST,
            "BRANCH": branch_monitoring_scripts_deploy_ts,
            "VERSION": version,
            "ENV": "prod"
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[6]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[6]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[6]["Status"] = "ABORTED"
        else:
            tasks_list[6]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[6]["Status"] = "FAILED"
        return False, None

def task_8():
    print("\n\n============================ Task 8 ============================\n\n")
    """Install Asterisk 9-C7"""
    task_name = "Task 8"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Asterisk 9-C7 installation", task_name)
    tasks_list[7]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[7]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Check asterisk status
        # commands = ["sudo service asterisk status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[7]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[7]["Status"] = "ABORTED"
        else:
            tasks_list[7]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[7]["Status"] = "FAILED"
        return False, None

def task_9():
    print("\n\n============================ Task 9 ============================\n\n")
    """Execute Jenkins Job for legolas-ts-build-prod"""
    task_name = "Task 9"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-build-prod", task_name)
    tasks_list[8]["Status"] = "Running"
    
    try:
        JOB_NAME = "legolas-ts/job/legolas-ts-build-prod"
        parameter_list = {
            "ENV": "prod",
            "GIT_BRANCH": branch_legolas_ts_build
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[8]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[8]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[8]["Status"] = "ABORTED"
        else:
            tasks_list[8]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[8]["Status"] = "FAILED"
        return False, None

def task_10():
    print("\n\n============================ Task 10 ============================\n\n")
    """Execute Jenkins Job for legolas-ts-deploy-prod1"""
    task_name = "Task 10"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - legolas-ts-deploy-prod1", task_name)
    tasks_list[9]["Status"] = "Running"
    
    try:
        JOB_NAME = "legolas-ts/job/legolas-ts-deploy-prod1"
        parameter_list = {
            "ANS_VERSION": "5-C7",
            "VERSION": "latest-stable",
            "HOST": HOST,
            "GIT_BRANCH": branch_legolas_ts_deploy
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[9]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Check legolas-ts status
        # commands = ["sudo service legolas-ts status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[9]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[9]["Status"] = "ABORTED"
        else:
            tasks_list[9]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[9]["Status"] = "FAILED"
        return False, None

def task_11():
    print("\n\n============================ Task 11 ============================\n\n")
    """Execute Jenkins Job for ts_gracefulstartstop_deploy"""
    task_name = "Task 11"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_gracefulstartstop_deploy", task_name)
    tasks_list[10]["Status"] = "Running"
    
    try:
        JOB_NAME = "ts_gracefulstartstop_deploy"
        parameter_list = {
            "HOSTS": HOST,
            "GIT_BRANCH": branch_ts_gracefulstartstop_deploy
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[10]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Check gracefulrestart.sh script
        # commands = ["ls /home/asterisk/"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[10]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[10]["Status"] = "ABORTED"
        else:
            tasks_list[10]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[10]["Status"] = "FAILED"
        return False, None

def task_12():
    print("\n\n============================ Task 12 ============================\n\n")
    """Install Adhearsion 29-C7"""
    task_name = "Task 12"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Adhearsion 29-C7 installation", task_name)
    tasks_list[11]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[11]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # commands = ["sudo service adhearsion status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[11]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[11]["Status"] = "ABORTED"
        else:
            tasks_list[11]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[11]["Status"] = "FAILED"
        return False, None

def task_13():
    print("\n\n============================ Task 13 ============================\n\n")
    """Install Firefoot-ts 7-C7"""
    task_name = "Task 13"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Firefoot-ts 7-C7 installation", task_name)
    tasks_list[12]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[12]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # commands = ["sudo service firefoot-ts status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[12]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[12]["Status"] = "ABORTED"
        else:
            tasks_list[12]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[12]["Status"] = "FAILED"
        return False, None

def task_14():
    print("\n\n============================ Task 14 ============================\n\n")
    """Install Amix 12-C7"""
    task_name = "Task 14"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Amix 12-C7 installation", task_name)
    tasks_list[13]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[13]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)

        # commands = ["sudo service amix status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[13]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[13]["Status"] = "ABORTED"
        else:
            tasks_list[13]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[13]["Status"] = "FAILED"
        return False, None

def task_15():
    print("\n\n============================ Task 15 ============================\n\n")
    """Install Eventshipper 8-C7"""
    task_name = "Task 15"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Eventshipper 8-C7 installation", task_name)
    tasks_list[14]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[14]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[14]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[14]["Status"] = "ABORTED"
        else:
            tasks_list[14]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[14]["Status"] = "FAILED"
        return False, None


def task_16():
    print("\n\n============================ Task 16 ============================\n\n")
    """Install Rsyslog"""
    task_name = "Task 16"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Rsyslog  installation", task_name)
    tasks_list[15]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[15]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        # Create causix recordings directory after successful Jenkins job
        if result == "SUCCESS":
            log_output("Creating causix recordings directory...", task_name)
            mkdir_cmd = "sudo mkdir -p /var/log/exotel/recordings/causix_recordings"
            success, out, err, rc = run_remote_cmd(HOST, global_username, global_key_file, mkdir_cmd, port)
            
            if success:
                log_output("Directory created successfully: /var/log/exotel/recordings/causix_recordings", task_name)
            else:
                log_output("Failed to create directory: {}".format(err), task_name, "WARNING")
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[15]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[15]["Status"] = "ABORTED"
        else:
            tasks_list[15]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[15]["Status"] = "FAILED"
        return False, None

def task_17():
    print("============================ Task 17 ============================\n\n")
    """Install Causix 5-C7"""
    task_name = "Task 17"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causix 5-C7 installation", task_name)
    tasks_list[16]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[16]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[16]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[16]["Status"] = "ABORTED"
        else:
            tasks_list[16]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[16]["Status"] = "FAILED"
        return False, None

def task_18():
    print("============================ Task 18 ============================\n\n")
    """Install Causixenqueuer 2-C7"""
    task_name = "Task 18"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Causixenqueuer 2-C7 installation", task_name)
    tasks_list[17]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[17]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)

        # commands = ["sudo service causix status","sudo status causixenqueuer"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[17]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[17]["Status"] = "ABORTED"
        else:
            tasks_list[17]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[17]["Status"] = "FAILED"
        return False, None

def task_19():
    print("============================ Task 19 ============================\n\n")
    """Install Route-switcher 11-C7"""
    task_name = "Task 19"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Route-switcher 11-C7 installation", task_name)
    tasks_list[18]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[18]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[18]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[18]["Status"] = "ABORTED"
        else:
            tasks_list[18]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[18]["Status"] = "FAILED"
        return False, None

def task_20():
    print("============================ Task 20 ============================\n\n")
    """Install Voipmonitor 21-C7"""
    task_name = "Task 20"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Voipmonitor 21-C7 installation", task_name)
    tasks_list[19]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[19]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)

        # commands = ["sudo service voipmonitor status"]
        # print("\nIt may fail at restart voipmonitor - that should be fine . Restart it manually if not running\n")
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[19]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[19]["Status"] = "ABORTED"
        else:
            tasks_list[19]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[19]["Status"] = "FAILED"
        return False, None

def task_21():
    print("============================ Task 21 ============================\n\n")
    """Install Fangorn 14-C7"""
    task_name = "Task 21"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Fangorn 14-C7 installation", task_name)
    tasks_list[20]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[20]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)

        # commands = ["sudo service fangorn status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[20]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[20]["Status"] = "ABORTED"
        else:
            tasks_list[20]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[20]["Status"] = "FAILED"
        return False, None

def task_22():
    print("============================ Task 22 ============================\n\n")
    """Install Traffic-shaper 1-C7"""
    task_name = "Task 22"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Traffic-shaper 1-C7 installation", task_name)
    tasks_list[21]["Status"] = "Running"
    
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
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[21]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)

        # commands = ["sudo bash /home/asterisk/traffic-shaper/trafficShaper.sh status"]
        # for cmd in commands:
        #     log_output("Executing command: {}".format(cmd), task_name)
        #     executing_linux_command_output = run_remote_command(HOST, global_username, global_key_file, cmd, port)
        #     log_output("Command output: {}".format(executing_linux_command_output), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[21]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[21]["Status"] = "ABORTED"
        else:
            tasks_list[21]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[21]["Status"] = "FAILED"
        return False, None

def task_23():
    print("\n\n============================ Task 23 ============================\n\n")
    """Execute Jenkins Job - prod-prometheus-process-exporter-deploy"""
    task_name = "Task 23"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - prod-prometheus-process-exporter-deploy", task_name)
    tasks_list[22]["Status"] = "Running"
    
    try:
        JOB_NAME = "prod-prometheus-process-exporter-deploy"
        
        parameter_list = {
            "GIT_BRANCH": branch_prometheus_process_exporter,
            "USER": "asterisk",
            "HOSTS": "{}:{}".format(HOST, port)  # Fixed
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[22]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[22]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[22]["Status"] = "ABORTED"
        else:
            tasks_list[22]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[22]["Status"] = "FAILED"
        return False, None

def task_24():
    print("\n\n============================ Task 24 ============================\n\n")
    """Execute Jenkins Job - prod-prometheus-node-exporter-deploy"""
    task_name = "Task 24"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - prod-prometheus-node-exporter-deploy", task_name)
    tasks_list[23]["Status"] = "Running"
    
    try:
        JOB_NAME = "prod-prometheus-node-exporter-deploy"
        
        parameter_list = {
            "GIT_BRANCH": branch_prometheus_node_exporter,
            "USER": "asterisk",
            "HOSTS": "{}:{}".format(HOST, port)
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[23]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[23]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[23]["Status"] = "ABORTED"
        else:
            tasks_list[23]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[23]["Status"] = "FAILED"
        return False, None

def task_25():
    print("\n\n============================ Task 25 ============================\n\n")
    """Execute Jenkins Job - prometheus-asterisk-exporter-deploy"""
    task_name = "Task 25"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - prometheus-asterisk-exporter-deploy", task_name)
    tasks_list[24]["Status"] = "Running"
    
    try:
        JOB_NAME = "prometheus-asterisk-exporter-deploy"
        
        parameter_list = {
            "GIT_BRANCH": branch_prometheus_asterisk_exporter,
            "USER": "asterisk",
            "HOSTS": "{}:{}".format(HOST, port)
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[24]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[24]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[24]["Status"] = "ABORTED"
        else:
            tasks_list[24]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[24]["Status"] = "FAILED"
        return False, None

def task_26():
    print("\n\n============================ Task 26 ============================\n\n")
    """Execute Jenkins Job - ts_logs_uploader_deploy"""
    task_name = "Task 26"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_output("Starting Jenkins Job - ts_logs_uploader_deploy", task_name)
    tasks_list[25]["Status"] = "Running"
    
    try:
        JOB_NAME = "ts_logs_uploader_deploy"
        
        parameter_list = {
            "GIT_BRANCH": branch_ts_logs_uploader,
            "HOSTS": HOST
        }
        
        result, _, build_url = jenkins_job_trigger(parameter_list, JOB_NAME)
        log_output("Jenkins job result: {}".format(result), task_name)
        
        # Store build URL in tasks_list
        if build_url:
            tasks_list[25]["BuildURL"] = build_url
            log_output("Build URL: {}".format(build_url), task_name)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        if result == "SUCCESS":
            tasks_list[25]["Status"] = "SUCCESS"
        elif result == "ABORTED":
            tasks_list[25]["Status"] = "ABORTED"
        else:
            tasks_list[25]["Status"] = "FAILED"
        return result == "SUCCESS", build_url
        
    except Exception as e:
        log_output("Error: {}".format(e), task_name, "ERROR")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = str(datetime.now() - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        tasks_list[25]["Status"] = "FAILED"
        return False, None

# Main execution function
def main():
    """Main function to execute tasks"""
    args = parse_args()
    # Set global branch variables
    global branch_ts_ami_setup, branch_ts_base_ami, branch_ts_environmental_setup, branch_ts_services_setup
    global branch_ts_telegraf_installation, branch_monitoring_scripts_build, branch_monitoring_scripts_deploy_ts
    global branch_asterisk, branch_legolas_ts_build, branch_legolas_ts_deploy, branch_ts_gracefulstartstop_deploy
    global branch_adhearsion, branch_firefoot_ts, branch_amix, branch_eventshipper, branch_rsyslog, branch_causix, branch_causixenqueuer
    global branch_route_switcher, branch_voipmonitor, branch_fangorn, branch_traffic_shaper
    global branch_prometheus_process_exporter, branch_prometheus_node_exporter, branch_prometheus_asterisk_exporter
    global branch_ts_logs_uploader  # Add this line

    global HOST, global_username, global_password, port, JENKINS_URL, USERNAME, API_TOKEN, SILLYIO_CODE, global_key_file

    HOST = args.host
    global_username = args.ssh_user
    global_password = args.ssh_password
    port = args.ssh_port
    SILLYIO_CODE = args.sillyio_code

    branch_ts_ami_setup = args.task_1_branch_ts_ami_setup
    branch_ts_base_ami = args.task_2_branch_ts_base_ami
    branch_ts_environmental_setup = args.task_3_branch_ts_environmental_setup
    branch_ts_services_setup = args.task_4_branch_ts_services_setup
    branch_ts_telegraf_installation = args.task_5_branch_ts_telegraf_installation
    branch_monitoring_scripts_build = args.task_6_branch_monitoring_scripts_build
    branch_monitoring_scripts_deploy_ts = args.task_7_branch_monitoring_scripts_deploy_ts
    branch_asterisk = args.task_8_branch_asterisk
    branch_legolas_ts_build = args.task_9_branch_legolas_ts_build
    branch_legolas_ts_deploy = args.task_10_branch_legolas_ts_deploy
    branch_ts_gracefulstartstop_deploy = args.task_11_branch_ts_gracefulstartstop_deploy
    branch_adhearsion = args.task_12_branch_adhearsion   
    branch_firefoot_ts = args.task_13_branch_firefoot_ts      
    branch_amix = args.task_14_branch_amix
    branch_eventshipper = args.task_15_branch_eventshipper
    branch_rsyslog = args.task_16_branch_rsyslog
    branch_causix = args.task_17_branch_causix
    branch_causixenqueuer = args.task_18_branch_causixenqueuer
    branch_route_switcher = args.task_19_branch_route_switcher
    branch_voipmonitor = args.task_20_branch_voipmonitor
    branch_fangorn = args.task_21_branch_fangorn
    branch_traffic_shaper = args.task_22_branch_traffic_shaper  

    branch_prometheus_process_exporter = args.task_23_branch_prometheus_process_exporter
    branch_prometheus_node_exporter = args.task_24_branch_prometheus_node_exporter
    branch_prometheus_asterisk_exporter = args.task_25_branch_prometheus_asterisk_exporter
    branch_ts_logs_uploader = args.task_26_branch_ts_logs_uploader

    log_output("Starting task execution", "MAIN")
    
    # Get task range from user
    task_start_number = args.task_start_number
    task_end_number = args.task_end_number
    
    log_output("Executing tasks from {} to {}".format(task_start_number, task_end_number), "MAIN")
    
    promptt='n'
    if promptt == 'y':
        last_version = None
        for i in range(task_start_number, task_end_number + 1):
            function_name = "task_{}".format(i)
            function_name2 = tasks_list[i-1]["Description"]

            if function_name in globals():
                log_output("Preparing to execute {}".format(function_name), "MAIN")
                print("\nGoing to execute {} - {}\nPlease press y to continue, n to skip, or c to cancel (y/n/c): ".format(function_name,function_name2))
                choice = input().lower()

                if choice == 'y':
                    try:
                        if function_name == "task_6":
                            success, last_version, build_url = globals()[function_name]()
                            log_output("{} completed".format(function_name), "MAIN")
                        elif function_name == "task_7":
                            globals()[function_name](version=last_version)
                            log_output("{} completed".format(function_name), "MAIN")
                        else:
                            globals()[function_name]()
                            log_output("{} completed".format(function_name), "MAIN")
                    except Exception as e:
                        log_output("Error in {}: {}".format(function_name, e), "MAIN", "ERROR")
                elif choice == 'n':
                    log_output("Skipping {}".format(function_name), "MAIN")
                    tasks_list[i-1]["Status"] = "SKIPPED"
                elif choice == 'c':
                    log_output("Cancelling the script", "MAIN")
                    break
                else:
                    log_output("Invalid choice, cancelling", "MAIN")
                    break
            else:
                log_output("Function {} not found".format(function_name), "MAIN", "ERROR")
    
    else:
        last_version = None
        for i in range(task_start_number, task_end_number + 1):
            function_name = "task_{}".format(i)
            function_name2 = tasks_list[i-1]["Description"]
            if function_name in globals():
                log_output("Preparing to execute {}".format(function_name), "MAIN")
                if function_name == "task_6":
                    success, last_version, build_url = globals()[function_name]()
                    log_output("{} completed".format(function_name), "MAIN")
                elif function_name == "task_7":
                    globals()[function_name](version=last_version)
                    log_output("{} completed".format(function_name), "MAIN")
                else:
                    globals()[function_name]()
                    log_output("{} completed".format(function_name), "MAIN")
            else:
                log_output("Function {} not found".format(function_name), "MAIN", "ERROR")



    log_output("Task execution completed", "MAIN")
    log_output("Log file: {}".format(log_file), "MAIN")
    print_task_summary(tasks_list)

if __name__ == "__main__":
    main()