import requests
import json
import time

count=1

id=input("Enter Number Phone's : ").split(', 
for i in id:
    k='0'+str(i)
    data={
        'VoiceUrl':'https://my.exotel.com/zomato127/exoml/start_voice/362431'
    }
    url ="https://zomato127:becef9db5e37d0b48164329631b99401b2a5ea0f@twilix.exotel.in/v1/Accounts/zomato127/IncomingPhoneNumbers/{}".format(k)
    x = requests.post(url,data=data)
    print(x)


    url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/zomato127"

    j='+91'+str(i)
    payload = json.dumps([
    {
        "greenvn": str(j),
        "region": "MU",
        "number_type": "landline"
    }
    ])
    headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Authorization': 'Basic dGVjaG9wczp0dzc1Znp2ZG53MnQ2N2Rq'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text,' : ',i, "count : ", count)
    if count==300:
        time.sleep(10)
    count+=1


