#!/usr/bin/env python3

def fix_jenkins_job_trigger():
    """Fix the jenkins_job_trigger function to handle single parameter dictionaries"""
    
    with open('SRO_Scripts/whole_script_in_one.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the jenkins_job_trigger function
    old_function = '''def jenkins_job_trigger(params,JOB_NAME):
    # params=sys.argv[1]
    JOB_NAME = JOB_NAME
    params=params
    
    
    for params in params:
        queue_url = trigger_jenkins_job(params,JOB_NAME)
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
            break'''
    
    new_function = '''def jenkins_job_trigger(params,JOB_NAME):
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
            break'''
    
    # Replace the function
    new_content = content.replace(old_function, new_function)
    
    # Write back to file
    with open('SRO_Scripts/whole_script_in_one.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed jenkins_job_trigger function in whole_script_in_one.py")

if __name__ == "__main__":
    fix_jenkins_job_trigger() 