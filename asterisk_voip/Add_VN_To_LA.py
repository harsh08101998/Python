import requests
import json

url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/zomato127"

count=1
numbers=input("Please enter Numbers :  ").split(', 
for i in numbers:
    j='+91'+str(i)
    payload = json.dumps([
    {
        "greenvn": str(j),
        "region": "TN",
        "number_type": "landline"
    }
    ])
    headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Authorization': 'Basic dGVjaG9wczp0dzc1Znp2ZG53MnQ2N2Rq'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text,' : ',count)
    count+=1
