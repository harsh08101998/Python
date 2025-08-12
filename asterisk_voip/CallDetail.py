import requests

ll=requests.get("https://f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255:b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858@api.exotel.com/v1/Accounts/exotel905/Calls/61a2791c0e2c6a4f8c0f539d081a157n")

print(ll)
print(ll.text)
# requests.get('https://<your_api_key>:<your_api_token><subdomain>/v1/Accounts/<your_sid>/Calls/b6cfaf5f5cef3ca0fc937749ef960e25 
# APIKEY :- f1f05b6e5932e1848dbb4ef76da49830d00bfe419adcd255
# APITOKEN :-  b4221d3ac4b3b2d0cf90dd3f415d9a8afe75142bec465858 
# SubDomain :- @api.exotel.com
# Account_Sid :-  080-456-81136 