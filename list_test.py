import base64 
import json
import requests
exotel_api_key ='4ed57a5ce3827f537aad70b5dcc7331d468f880170e045d0'
exotel_api_token='c1354dff0f06e0e340fdc15f01053d4993cefe89619f3ef6'


exotel_sub_domain='@api.in.exotel.com'
list_sid='e28474a0605345e1b62a1218f8d18562'
exotel_sid='fyers1m'
auth_token = base64.b64encode((exotel_api_key + ":" + exotel_api_token).encode('utf-8 ).decode('utf-8 
headers1 = {'Authorization': 'Basic ' + auth_token}
# import pdb; pdb.set_trace()
url = "https://" + exotel_api_key + ":" + exotel_api_token + exotel_sub_domain + "/v2/accounts/fyers1m/contacts/csv-upload/" + list_sid
payload = {"file_path": "input1.csv"}
files = {"file_name": open("input1.csv", 'rb }

# payload = json.dumps({ "list_name":"hk","filepath":"input1.csv" })

request = requests.put(url, data=payload, files=files,headers=headers1)
response = request.json()
# print(response['response']['data']['list']['sid'])
print(response)
if request:
    response = request.json()
    if response['response']['data']['list']['sid']:
        url = "https://" + exotel_api_key + ":" + exotel_api_token + exotel_sub_domain + "/v2/accounts/" + exotel_sid + "/campaigns"
        payload = json.dumps({"campaigns": [{
            "caller_id": '+9107948060730',
            "name": "campaign-"+"test17423",
            "type": "trans",
            "lists": ['e28474a0605345e1b62a1218f8d18562'],
            "url": 'http://my.exotel.com/fyers1m/exoml/start_voice/3894'
        }]
        })
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic " + auth_token
        }
        request = requests.post(url, data=payload,headers=headers)
        print(request.text)

        