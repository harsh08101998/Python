import requests
import json

url = "https://exotelt:eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b@ccm-api.exotel.com/v2/accounts/exotelt/users"
# streetgainsresearchservices1
payload = json.dumps({
  "first_name": "harsh",
  "last_name": "kumar",
  "email": "harsh.kumar+exotelt@exotel.com",
  "device_contact_uri": "+918570027091",
  "role" : "admin"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# "first_name": "Pooja",
#     "last_name": "Dhokane",
#     "email": "pooja.dhokane@bajajfinserv.in",
#     "device_contact_uri": "+919607926037"
# Apoorv Saxena12:49 PM
# apoorv.saxena+exotelt@exotel.in
# Apoorv Saxena1:25 PM
# apoorv.saxena+exotelt@exotel.in
# 9981594564

# curl --location --request DELETE 'https://streetgainsresearchservices1:de0b6b99ef4546bb474c1a15570e30016915984f@ccm-api.exotel.com/v2/accounts/streetgainsresearchservices1/users/85f566848b0e421793f95547d7788441'