import requests

url="https://exotel905:102ea1c06725eedc481e93ea61df480c702b648b@ccm-api.exotel.com/v2/accounts/exotel905/users/d0e8d969d80144268da76e0332266838"
# url = "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/users/<user_id>"

payload={}
headers = {

}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)