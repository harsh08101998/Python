import requests

data = {
  'From': '08047096299',
  'To': '08570027091',
  'Body': 'Dear {#var#}, We sincerely thank you for your valuable support in the form of donations. On behalf of our teams, we have a special message for you from Dr Farhat Mantoo, General Director, MSF India (https://youtu.be/yqFQwUqMtNc). To know more about our projects in India, visit www.msfsouthasia.org. For queries related to your donations reach out to our donor service team at DonorService@new-delhi.msf.org or call us at +919958159797. -MSF India',
  # 'Priority' : 'high'
}

hh=requests.post('https://2c5e756f71793e4dcc8100b8957a93e672ad8cc51bbddcce:f4c3bedeacdeeb2c52be40537dd3749948dbc4c5fd8046bc@api.exotel.com/v1/Accounts/msfindia1/Sms/send', data=data)

print(hh.text)            
