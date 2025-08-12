
import requests, base64, json,os
url='https://notp.exotel.com/v2/notp-numbers'



headers = {
    'accept': 'application/json',
    'content-type': "application/json",
    'verification-app-secret' : 'secret',
    'verification-app-id': 'abcdef',
    'version': '1.6.0'
  
    }

number=input("Enter Phone Numbers  \n").split(', 

for i in number:
    payload =json.dumps({
        "vn": i,
        "country_code": "ID",         # Enter country_code as required
        "account_sid": "exotel230",   # Enter Account Sid is required
        "active": "true",
        "pool_id": 1                  # Enter pool as required
    })
    json_object = json.dumps(payload, indent = 4) 
    response = requests.request("POST", url,data=json_object,headers=headers)
    print(response.text)
    print(json_object)
















os.system(
    "curl --location --request POST 'https://notp.exotel.com/v2/notp-numbers' \
    --header 'accept: application/json' \
    --header 'content-type: application/json' \
    --header 'verification-app-secret: secret' \
    --header 'verification-app-id: abcdef' \
    --header 'version: 1.6.0' \
    --data-raw {
            'vn': '+6285592020571',
            'country_code': 'ID',
            "account_sid": "exotel230",
            "active": true,
            "pool_id": 1
        }"
    )