import requests


id=input("Enter Number Phone's : ").split(', 
# accountsid=input("Enter Client Accountsid : ")
for i in id:
    # url="http?s://default:f7127af352491a86127aad77d7a1419e9ca3cef4@twilix.exotel.in/v1/Accounts/default/AvailablePhoneNumbers/{}.json?_state=reserved&_ReservedFor={}".format(int(i),accountsid)
    data={
        'VoiceUrl':'https://my.exotel.com/zomato127/exoml/start_voice/362431'
    }
    url ="https://zomato127:becef9db5e37d0b48164329631b99401b2a5ea0f@twilix.exotel.in/v1/Accounts/zomato127/IncomingPhoneNumbers/{}".format(i)
    x = requests.post(url,data=data)
    print(x.text)


# curl -XPOST zomato127:becef9db5e37d0b48164329631b99401b2a5ea0f@twilix.exotel.in/v1/Accounts/zomato127/IncomingPhoneNumbers/08037501438 -d 'VoiceUrl=https://my.exotel.com/zomato127/exoml/start_voice/362431'