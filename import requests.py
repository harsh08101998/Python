import requests
from requests.auth import HTTPBasicAuth
  
# Making a get request
url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/zomato127"
data = {
    "greenvn": "+914471273077",
    "region": "TN",
    "number_type": "landline"
  }
response = requests.post(url, data=data,auth = HTTPBasicAuth('techops', 'tw75fzvdnw2t67dj )
  
# print request object
print(response)