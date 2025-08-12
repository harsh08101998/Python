import csv
import requests
import json

file = open('hhh.csv 
csvreader = csv.reader(file)
rows = []
for row in csvreader:
        rows.append(row)

# print(rows)
for i in rows:
  name=i[0]
  first_name=i[0]
  last_name=i[1]
  email=i[2]
  contact=i[3]
  number='+91'+str(contact)
  roleee=i[4]
  print(first_name, last_name,email,number,roleee)
  url = "https://financepeer:f94275df0986c9f6c15437a8a0a93c4737c7469a@ccm-api.exotel.com/v2/accounts/financepeer/users"
  payload = json.dumps({
    "first_name": str(first_name),
    "last_name": str(last_name),
    "email": str(email),
    "device_contact_uri": str(number),
    "role":str(roleee)
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.status_code)
  print(response.text)
  if response.status_code != 200:
    with open('failed.txt', 'a  as f:
      f.write(email)
      f.write('\n 
      f.write(response.text)
      f.write('\n\n 
