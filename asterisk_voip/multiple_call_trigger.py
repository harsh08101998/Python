
import requests, json
import time,sys


accountsid='exotelt'
api_token='eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b'



# number_list=['08045246232','08045246233']
from_number=sys.argv[1]
to_number=sys.argv[2]
number_list=sys.argv[3].split(',')
interval=sys.argv[4]

region=sys.argv[5]

if region=='MUM':
  domain='api.in.exotel.com'
if region=='SG':
  domain='api.exotel.com'


print(domain)
for i in number_list:
  data = {
    'From': from_number,
    'CallerId': i,
    'To':to_number,
    '__RequestedServerCode':'0731_09',
    '__IgnoreServerStatus':'true'
  }
  print(data)
  url='https://{}:{}@{}/v1/Accounts/' \
  '{}/Calls/connect.json'.format(accountsid,api_token,domain,accountsid)
  dataa=requests.post(url, data=data)
  status_code=dataa.status_code
  if status_code==200:
    call_json=json.loads(dataa.text)
    call_detail=call_json["Call"]
    sid=call_detail["Sid"]
    from_numberr= call_detail["From"]
    to_number=call_detail["To"]
    callerid=call_detail["PhoneNumberSid"]
  
    print("           Sid                 ","  CallerId  ","  From       ", "  To          ")
    print(sid, callerid,from_number,to_number)
    time.sleep(int(interval))
  else:
    print(dataa.text)