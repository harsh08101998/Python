import time
import requests,json

accountsid='abc6058'


id=input("Enter Numbers's : ").split(', 
for i in id:

    ############################################## Number adding to Flow ######################
    
    # data={
    #     'VoiceUrl':'https://my.exotel.com/indeed13/exoml/start_voice/338415'
    # }
    # url ="https://indeed13:7ddb7b69c19ea34f7e42a7a6a7c9e8270afc2c02@twilix.exotel.in/v1/Accounts/indeed13/IncomingPhoneNumbers/{}".format(i)
    # # x = requests.post(url,data=data)
    # print(url)

########################################### Number adding to LA #######################################
    url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/abc6058"

    j='+91'+str(int(i))
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
    print(response)
        
        