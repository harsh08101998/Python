import requests, base64, json
accountSid = "monjin1"
authToken = "fba268a787c817b6ef8f45cd8d46f5c4265f5ea2dc7ceaf8"
authKey = "a4f2b3c5eff362665742ef63847219969c8467cef8ad73d9"

encoding = base64.b64encode(authKey.encode('utf-8  + ":".encode('utf-8  + authToken.encode('utf-8 )

url = "https://api.exotel.com/v2/accounts/"+accountSid+"/campaigns"

payload = json.dumps({ "campaigns": [{ 
          "caller_id": "02071178294", 
          "name": "testtt_campaign",
          "type":"trans",
          "call_duplicate_numbers": 'true',
          "url": "http://my.exotel.com/<your_sid>/exoml/start_voice/416499", 
          "lists": ["08570027091"],
          "status_callback": "https://php-int.azurewebsites.net/monjin-exotel/Campaign/callback_url", 
          "call_status_callback": "https://mycallback.sampledomain.in/1gvta9f1"}]
        })
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic " + encoding
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
print(json.dumps(json.loads(response.text), indent = 4, sort_keys = True))