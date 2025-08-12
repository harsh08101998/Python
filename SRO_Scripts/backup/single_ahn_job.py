import requests
import time,sys
from requests.auth import HTTPBasicAuth

from ast import arg
import paramiko
import sys, sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Global variables
JENKINS_URL = "https://build.corp.exotel.in:8080"
USERNAME = "harsh_kumar"
API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"


# Jenkins configuration
# JENKINS_URL = "https://build.corp.exotel.in:8080"
# JOB_NAME = "ts-ami-deploy"
# USERNAME = "harsh_kumar"
# API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"

# # List of parameter sets (each dict is one run)
# parameter_list = [
#     # {"PLAYBOOK": "ts_base_ami", "GIT_BRANCH": "feat/ts-centos-7-changes-updated","HOST": HOST,"SSH_USER_NAME":"root","SSH_PASSWORD":"Mytet@P*l8bza0","SILLYIO_CODE":HOST{"PLAYBOOK": "ts_environmental_setup", "GIT_BRANCH": "feat/ts-centos-7-changes-updated","HOST": HOST,"SSH_USER_NAME":"root","SSH_PASSWORD":"Mytet@P*l8bza0","SILLYIO_CODE":HOSTPLAYBOOK": "ts_services_setup", "GIT_BRANCH": "feat/ts-centos-7-changes-updated","HOST": HOST,"SSH_USER_NAME":"root","SSH_PASSWORD":"Mytet@P*l8bza0","SILLYIO_CODE":HOST"PLAYBOOK": "ts_telegraf_installtion", "GIT_BRANCH": "feat/ts-centos-7-changes-updated","HOST": HOST,"SSH_USER_NAME":"root","SSH_PASSWORD":"Mytet@P*l8bza0","SILLYIO_CODE":HOST######################################################################################################################


# JENKINS_URL = "https://build.corp.exotel.in:8080"
# JOB_NAME = "ts-code-push"
# USERNAME = "harsh_kumar"
# API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"rvim

# # List of parameter sets (each dict is one run)
# parameter_list = [
#     {"SERVICE": "asterisk","ANS_VERSION": "9-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch}
# ]


########################################################################################################################

# JENKINS_URL = "https://build.corp.exotel.in:8080"
# JOB_NAME = "legolas-ts/job/legolas-ts-deploy-prod1"
# USERNAME = "harsh_kumar"
# API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"

# # List of parameter sets (each dict is one run)
# parameter_list = [
#     {"ANS_VERSION": "5-C7","VERSION": "latest-stable","HOST": HOST,"GIT_BRANCH": ahn_git_branch}
# ]


################################################ AHN_INSTALLATION Jobs ########################################################################


# JOB_NAME = "ts-code-push-C7"
# HOST = "079-veeno-2.exotel.in"
# ahn_git_branch = "master"

# # List of parameter sets (each dict is one run)
# parameter_list = [
#     {"SERVICE": "adhearsion","ANS_VERSION": "29-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "firefoot-ts","ANS_VERSION": "7-C7","VERSION": "latest","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "amix","ANS_VERSION": "12-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "eventshipper","ANS_VERSION": "8-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch}

#     # betwewn this first run Rsyslog Jenkins job and commands
#     {"SERVICE": "causix","ANS_VERSION": "5-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "causixenqueuer","ANS_VERSION": "2-C7","VERSION": "latest","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "route-switcher","ANS_VERSION": "11-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},

#     {"SERVICE": "voipmonitor","ANS_VERSION": "21-C7","VERSION": "latest-stable","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "fangorn","ANS_VERSION": "14-C7","VERSION": "latest","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch},
#     {"SERVICE": "traffic-shaper","ANS_VERSION": "1-C7","VERSION": "6-C7","HOST": HOST,"EXTERNAL_VARS": "conftype=slave","GIT_BRANCH": ahn_git_branch}

# ]

######################################### Rsyslog Jenkins job ###############################################################################

# JENKINS_URL = "https://build.corp.exotel.in:8080"
# JOB_NAME = "prod-rsyslog-deploy-C7 (centos 7 TS only)"
# USERNAME = "harsh_kumar"
# API_TOKEN = "11997f137d8f363dd8afaf9285a6fe88d2"

# # List of parameter sets (each dict is one run)
# parameter_list = [
#     {"HOSTS": HOST,"GIT_BRANCH": ahn_git_branch,"FORK": "5","USER": "asterisk","RSYSLOG_TYPE": "log","SERVICES": '"adhearsion","firefoot-ts","eventshipper","legolas-ts"'}

# ]

########## creating new pri table #########################################################################################


JOB_NAME = "Insert_into_new_Pri_table_15_july202335"
# List of parameter sets (each dict is one run)
params = [{
    "server_code": "079_veeno_02",
    "pilotNumber": "07971114545", 
    "plan": "138",
    "fcvPlan": "192",
    "range": "100",
    "pipeType": "trans",
    "isdStatus": "disabled",
    "operatorAccountNumber": "VODAFONE SIP ",
    "slot_number_for_card": "3",
    "spans": "vodafone.sip.com"
},
{
    "server_code": "079_veeno_02",
    "pilotNumber": "07935048061", 
    "plan": "139",
    "fcvPlan": "193",
    "range": "100",
    "pipeType": "trans",
    "isdStatus": "disabled",
    "operatorAccountNumber": "JIO SIP",
    "slot_number_for_card": "3",
    "spans": "jio.sip.com"
},
{
    "server_code": "079_veeno_02",
    "pilotNumber": "07971038770", 
    "plan": "260",
    "fcvPlan": "288",
    "range": "100",
    "pipeType": "trans",
    "isdStatus": "inactive",
    "operatorAccountNumber": "VODAFONE SIP",
    "slot_number_for_card": "3",
    "spans": "vi.sbc.sip.com"
}
]


def trigger_jenkins_job(params):
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/buildWithParameters"
    response = requests.post(
        build_url,
        params=params,
        auth=HTTPBasicAuth(USERNAME, API_TOKEN),
        verify=False
    )
    if response.status_code in [201, 200]:
        print(f"Job triggered with params: {params}")
        # Get queue item URL from headers
        queue_url = response.headers.get('Location')
        return queue_url
    else:
        print(f"Failed to trigger job: {response.status_code} {response.text}")
        return None

def get_build_number(queue_url):
    # Poll the queue item until it gets a build number
    while True:
        r = requests.get(f"{queue_url}api/json", auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'executable' in data and 'number' in data['executable']:
                return data['executable']['number']
            elif 'cancelled' in data and data['cancelled']:
                print("Job was cancelled in queue.")
                return None
        time.sleep(2)

def wait_for_build(jenkins_url, job_name, build_number):
    build_url = f"{jenkins_url}/job/{job_name}/{build_number}/api/json"
    while True:
        r = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        if r.status_code == 200:
            data = r.json()
            if data['building']:
                print(f"Build {build_number} is still running...")
            else:
                print(f"Build {build_number} finished with result: {data['result']}")
                return data['result']
        else:
            print(f"Error fetching build status: {r.status_code}")
        time.sleep(5)


def main(params,JOB_NAME):
    # params=sys.argv[1]
    JOB_NAME = JOB_NAME
    params=params
    
    
    for params in params:
        queue_url = trigger_jenkins_job(params)
        if not queue_url:
            print("Skipping to next parameter set due to trigger failure.")
            continue
        print(f"Waiting for job to start (queue URL: {queue_url})...")
        build_number = get_build_number(queue_url)
        if not build_number:
            print("No build number found, skipping to next.")
            continue
        print(f"Build started: {build_number}. Waiting for completion...")
        result = wait_for_build(JENKINS_URL, JOB_NAME, build_number)
        print(f"Build {build_number} result: {result}")
        if result != "SUCCESS":
            print("Stopping further runs due to failure.")
            break

if __name__ == "__main__":
    main(params,JOB_NAME)