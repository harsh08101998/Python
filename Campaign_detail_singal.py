import requests, base64, json

count_size=int(input("Please Enter Campaign Count Size :  "))
count2=count_size+20
size=0
j=0
while size <= count2:
    url= "https://fba268a787c817b6ef8f45cd8d46f5c4265f5ea2dc7ceaf8:a4f2b3c5eff362665742ef63847219969c8467cef8ad73d9@api.exotel.com/v2/accounts/monjin1/campaigns/687ab6bb58953a2c83236a020daa6b8115ci/call-details?limit=20&offset={}".format(size)
    response = requests.request("GET", url)
    data=response.text
    size +=20
    # for i in data:
    #     print(j," : ", i)
    #     j+=1
    print(data)
    print(url)