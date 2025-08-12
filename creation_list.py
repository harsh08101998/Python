import requests
import base64 
import json
authKey ='4ed57a5ce3827f537aad70b5dcc7331d468f880170e045d0'
authToken='c1354dff0f06e0e340fdc15f01053d4993cefe89619f3ef6'
exotel_sub_domain='@api.in.exotel.com'
accountSid='fyers1m'

encoding = base64.b64encode((authKey + ":" + authToken).encode('utf-8 ).decode('utf-8 

url = "https://@api.in.exotel.com/v2/accounts/"+ accountSid+"/lists"

payload = json.dumps({
    "lists": [
        {
            "name": "Exotel_TS135554",
            
        }
 
    ]
})

headers = {
    'Authorization': "Basic " + encoding,
    'Content-Type': 'application/json'
}


response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
hh=json.dumps(json.loads(response.text), indent = 4, sort_keys = True)
jj=json.loads(response.text)
# print(response['response']['data']['list']['sid'])
print(jj['response'][0]['data']['sid'])


# fyers1m/list

# 2022-04-26T11:14
# 2022-04-26T17:

# curl -X DELETE 'https://4ed57a5ce3827f537aad70b5dcc7331d468f880170e045d0:c1354dff0f06e0e340fdc15f01053d4993cefe89619f3ef6@api.in.exotel.com/v2/accounts/fyers1m/lists/9278296fd5034682a08c3c687634d5b1'