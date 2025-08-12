import requests

data = {
  'From' : '8570027091',
  'CallerId': '08047092644',
  'To': '07988532204'
}
# ll=requests.post("https://f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255:b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858@api.exotel.com/v1/Accounts/exotel905/Calls/connect" , data=data)

ll=requests.post('https://81f34d21c604c944f2ca7ce9100625bbc735ac4668fc1f4c:b5e91a460be6566187d9d1a351a9f466e7b0eda2a846e675@api.exotel.com/v1/Accounts/srnmehtaschool1/Calls/connect', data=data)

print(ll.text)
