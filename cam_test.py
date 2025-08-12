import requests, base64, json, os
# accountSid = "exotel905"
# authToken = "b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858"
# authKey = "f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255"


# # data_string = os.environ['INTRINIO_USER'] + ":" + os.environ['INTRINIO_PASSWORD']

# # data_bytes = data_string.encode("utf-8")

# # base64.b64encode(data_bytes

# data_string=os.environ
# encoding = base64.b64encode(authKey + ":" + authToken)


accountSid = "exotel905"
apiKey = "f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255"
apiToken = "b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858"
str1=apiKey + ":" + apiToken
encoding = base64.b64encode(bytes(str1, encoding="utf8"))

# url = "https://api.exotel.com/v2/accounts/exotel905/campaigns"
url = "https://api.exotel.com/v2/accounts/"+accountSid+"/campaigns"

payload = json.dumps({ "campaigns": [{ 
          "caller_id": "08045681136", 
          "name": "diwali_campaign",
          "type":"trans",
          "lists": [8489770544,7988532204]}]
        })
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic " + encoding
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
print(json.dumps(json.loads(response.text), indent = 4, sort_keys = True))