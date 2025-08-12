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

i=2

print(tasks_list[i-1]["Description"])