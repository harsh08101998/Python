from concurrent.futures.process import _python_exit
from re import A
import requests

accountsid='exotel905'
api_token='102ea1c06725eedc481e93ea61df480c702b648b'




payload = '{ "from": { "user_contact_uri": "08570027091" }, "to": { "customer_contact_uri": "08570027091" }, "virtual_number": "+918047091999" , "status_callback" : [{"event": "terminal","url": "https://1663-35-154-174-161.ngrok.io"}]}'


url='https://{}:{}@ccm-api.exotel.com/v2/accounts/{}/calls'.format(accountsid,api_token,accountsid)
print(url)


headers = {
'content-type': "application/json"
    }

dataa=response = requests.request("POST", url, data=payload, headers=headers)


print(dataa.text)

