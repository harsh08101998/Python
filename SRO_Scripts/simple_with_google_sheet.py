import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
client = gspread.authorize(creds)
sheet = client.open("YourSheetName").sheet1  # or .worksheet('Sheet1')

# Read parameters from row 2
row = 2
values = sheet.row_values(row)
params = {
    "CallerID": values[0],
    "From_Number": values[1],
    "To_Number": values[2],
    "Time_Interval": values[3],
    "Region": values[4],
    "AccountSid": values[5],
    "Account_token": values[6]
}

# Jenkins details
JENKINS_URL = "https://build.corp.exotel.in:8080"
JOB_NAME = "Trigger_Multiple_calls"
USERNAME = "your_jenkins_username"
API_TOKEN = "your_jenkins_api_token"

# Build URL
build_url = f"{JENKINS_URL}/job/{JOB_NAME}/buildWithParameters"

# Trigger the job
response = requests.post(
    build_url,
    params=params,
    auth=(USERNAME, API_TOKEN),
    verify=False
)

# Write status back to the sheet
status_col = 8  # Column H
if response.status_code in [200, 201]:
    sheet.update_cell(row, status_col, "Triggered")
else:
    sheet.update_cell(row, status_col, f"Error: {response.status_code}")

# (Optional) Poll Jenkins for build status and update sheet
# You can enhance this by parsing the queue/build number from Jenkins and polling for completion.