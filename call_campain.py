import requests, base64, json
accountSid = "Exotel"
apiKey = "3deac04804d9e0f0392053870477665916044ca2943e998f"
apiToken = "0f2dff58dac3e783466d4b5faece7d197f067e22c89d4a4f"
str1=apiKey + ":" + apiToken
# https://my.exotel.com/exotel905/flows/edit/383749#flowline/start
encoding = base64.b64encode(bytes(str1, encoding="utf8"))
url="https://api.exotel.com/v2/accounts/Exotel/campaigns"
payload = json.dumps({ "campaigns": [{ 
					"caller_id": "02248931400", 
					"url": "https://my.exotel.com/Exotel/flows/edit/383749#flowline/start", 
					"from": [ "08570027091"], 
					# "status_callback": "http://<callback custom domain>/1gvta9f1", 
					# "call_status_callback": "http://<callback custom domain>/1gvta9f1"
                    }]
				})
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic ".encode() + encoding
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
print(json.dumps(json.loads(response.text), indent = 4, sort_keys = True))