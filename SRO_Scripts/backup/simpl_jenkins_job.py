#!/usr/bin/env python3
"""
Simple Jenkins Job Runner Script
This script triggers Jenkins jobs with parameters using the Jenkins REST API
"""

import requests
import json
import sys
import argparse
from urllib.parse import urljoin

class JenkinsJobRunner:
    def __init__(self, jenkins_url, username, token):
        """
        Initialize Jenkins job runner.
        
        Args:
            jenkins_url (str): Jenkins server URL (e.g., https://jenkins.example.com)
            username (str): Jenkins username
            token (str): Jenkins API token
        """
        self.jenkins_url = jenkins_url.rstrip('/')
        self.username = username
        self.token = token
        self.auth = (username, token)
    
    def trigger_job(self, job_name, parameters=None):
        """
        Trigger a Jenkins job with optional parameters.
        
        Args:
            job_name (str): Name of the Jenkins job
            parameters (dict): Dictionary of parameters to pass to the job
            
        Returns:
            bool: True if job triggered successfully, False otherwise
        """
        try:
            # Construct the job URL
            job_url = urljoin(self.jenkins_url, f"/job/{job_name}/buildWithParameters")
            
            print(f"Triggering job: {job_name}")
            print(f"Job URL: {job_url}")
            
            if parameters:
                print(f"Parameters: {json.dumps(parameters, indent=2)}")
                # Make POST request with parameters
                response = requests.post(
                    job_url,
                    params=parameters,
                    auth=self.auth,
                    verify=False,  # Disable SSL verification for internal Jenkins
                    timeout=30
                )
            else:
                print("No parameters provided")
                # Make POST request without parameters
                response = requests.post(
                    job_url,
                    auth=self.auth,
                    verify=False,
                    timeout=30
                )
            
            # Check response status
            if response.status_code in [200, 201]:
                print(f"✅ Successfully triggered job: {job_name}")
                print(f"Response status: {response.status_code}")
                return True
            else:
                print(f"❌ Failed to trigger job: {job_name}")
                print(f"Response status: {response.status_code}")
                print(f"Response text: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False
    
    def get_job_info(self, job_name):
        """
        Get information about a Jenkins job.
        
        Args:
            job_name (str): Name of the Jenkins job
            
        Returns:
            dict: Job information or None if failed
        """
        try:
            job_url = urljoin(self.jenkins_url, f"/job/{job_name}/api/json")
            
            response = requests.get(
                job_url,
                auth=self.auth,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get job info: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting job info: {str(e)}")
            return None

def main():
    """Main function to handle command line arguments and run the script."""
    parser = argparse.ArgumentParser(description="Trigger Jenkins jobs with parameters")
    parser.add_argument("--jenkins-url", required=True, help="Jenkins server URL")
    parser.add_argument("--username", required=True, help="Jenkins username")
    parser.add_argument("--token", required=True, help="Jenkins API token")
    parser.add_argument("--job-name", required=True, help="Name of the Jenkins job to trigger")
    parser.add_argument("--parameters", help="JSON string of parameters (e.g., '{\"param1\":\"value1\",\"param2\":\"value2\"}')")
    
    args = parser.parse_args()
    
    # Initialize Jenkins runner
    runner = JenkinsJobRunner(args.jenkins_url, args.username, args.token)
    
    # Parse parameters if provided
    parameters = None
    if args.parameters:
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON parameters: {str(e)}")
            sys.exit(1)
    
    # Trigger the job
    success = runner.trigger_job(args.job_name, parameters)
    
    if success:
        print("🎉 Job triggered successfully!")
        sys.exit(0)
    else:
        print("💥 Failed to trigger job!")
        sys.exit(1)

if __name__ == "__main__":
    main()