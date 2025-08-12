import time
import requests,json


# number=[61480005023,61480005026,61480005027,61480005028,61480005029,61480005031,61480005032,61480005034,61480005035,61480005038,61480005039,61480005042,61480005045,61480005046,61480005052,61480005054]
number=[61480005021,61480005022,61480005023,61480005024,61480005026,61480005027,61480005028,61480005029,61480005031,61480005032,61480005034,61480005035,61480005036,61480005038,61480005039,61480005041,61480005042,61480005043,61480005044,61480005045,61480005046,61480005049,61480005052,61480005054]
for i in number:

    ############################################## Number added to Flow ######################
    k='+'+str(i)
    data={
        'VoiceUrl':'https://my.exotel.com/urbancompany17/exoml/start_voice/411434'
    }
    url ="https://urbancompany17:666b2d5eb75bd5bdd35dbb91182e605b7e7968d1@twilix.exotel.in/v1/Accounts/urbancompany17/IncomingPhoneNumbers/{}".format(k)
    print(url)
    x = requests.post(url,data=data)
    print(x.text,"\n")

 
# ######################################## Number added to LA #######################################
#     url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/urbancompany17"

#     j='+'+str(int(i))

#     payload = json.dumps([
#     {
#         "greenvn": str(j),
#         "region": "AU",
#         "number_type": "landline"
#     }
#     ])
#     headers = {
#     'Content-Type': 'application/json',
#     'Cache-Control': 'no-cache',
#     'Authorization': 'Basic dGVjaG9wczp0dzc1Znp2ZG53MnQ2N2Rq'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     print(response.text)

#     print(payload)
    
        