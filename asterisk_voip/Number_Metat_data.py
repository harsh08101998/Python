import requests

hh=requests.get('https://f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255:b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858@api.exotel.com/v1/Accounts/exotel905/Numbers/09815088338')
print(hh.text)