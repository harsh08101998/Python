import requests
import json

url = "https://72d86d86e565424b5e42159f80fd7cdd58992539c22cdbd9:a35b3a346a1670399a721d1bd25126ef4cb07b3742a2c1c7@ccm-api.in.exotel.com/v2/accounts/icicibank100m/users"

payload = json.dumps({
  "first_name": "Akash",
  "last_name": "Kumar",
  "email": "akash.kumar7@icicibank.com",
  "device_contact_uri": "+918274970866"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
print(response.url)


