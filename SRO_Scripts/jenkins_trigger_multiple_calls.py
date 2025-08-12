from ast import arg
import requests, json
import time,sys
import subprocess
from datetime import datetime

# 
# python3 jenkins_trigger_multiple_calls.py 08570027091 08570094268 8989,8989 30 SG exotelt eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b 080_28 true 

# number_list=['08045243232','08045246232','08045243732','08044620202','08047359899','08062314002','08062322702','08035009097','08035273380','08037905006'

def make_exotel_call_subprocess(curl_command,numberr):
    try:
        #result = subprocess.run(curl_command, capture_output=True, text=True)
        result = subprocess.run( curl_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)  # equivalent to text=True in Python < 3.7)
        if result.returncode == 0:
            hhh=result.stdout
            try:
                call_data=json.loads(result.stdout)
                call_sid = call_data["Call"]["Sid"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n{timestamp} :- {numberr} :- {call_sid}", flush=True)
                time.sleep(int(interval))
            except Exception as e:
                print(f"\nError: {numberr} : {hhh}", flush=True)
                return None
            return result.stdout
        else:
            print(hhh)
            return None
    except Exception as e:
        print(f"\nError making call: {e}", flush=True)
        return None

param_len=len(sys.argv)

from_number=sys.argv[1]
to_number=sys.argv[2]
number_list=sys.argv[3].split(',')


interval=sys.argv[4]
region=sys.argv[5]
if region=='MUM':
  domain='api.in.exotel.com'

if region=='SG':
  domain='api.exotel.com'

accountsid=sys.argv[6]
api_token=sys.argv[7]
if param_len > 8:
    server_code=sys.argv[8]
    ignore_server_status=sys.argv[9]
    for i in number_list:

        curl_command = [
            'curl', '-X', 'POST',
            'https://{}:{}@{}/v1/Accounts/{}/Calls/connect.json'.format(accountsid,api_token,domain,accountsid),
            '-d', f'From={from_number}',
            '-d', f'CallerId={i}',
            '-d', f'To={to_number}',
            '-d', f'__RequestedServerCode={server_code}',
            '-d', f'__IgnoreServerStatus={ignore_server_status}',
            '-d', 'Record=true'
            ]
        # print(curl_command)
        make_exotel_call_subprocess(curl_command,i )
        #time.sleep(int(interval))


else:
    for i in number_list:
        curl_command = [
        'curl', '-X', 'POST',
        'https://{}:{}@{}/v1/Accounts/{}/Calls/connect.json'.format(accountsid,api_token,domain,accountsid),
        '-d', f'From={from_number}',
        '-d', f'CallerId={i}',
        '-d', f'To={to_number}',
        '-d', 'Record=true'
        ]

        make_exotel_call_subprocess(curl_command,i)
        #time.sleep(int(interval))