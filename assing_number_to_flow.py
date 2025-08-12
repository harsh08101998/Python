import time
import requests,json
import mysql.connector



#select Id,PhoneNumber,Region,Operator, _state, _ReservedFor, AccountSid From twilix.AvailablePhoneNumber where AccountSid is Null and _state='pn' and Region='TN' and Operator=5 and Rental <0 and _ReservedFor is NUll  and PhoneNumber not in(select PhysicalNumber from twilix.PhysicalVirtualMap) and _Pri in(select id from twilix.Pri where pilot=4471819201) limit 1900;

# accountsid=input("Enter Client Accountsid : ")
accountsid='indeed11'

conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()
query="select AuthToken from Account where Sid='{}'".format(accountsid)
my_cursor.execute(query)
token=(my_cursor.fetchall()[0])[0].decode()

count=1
id=input("Enter Number ID's : ").split(', 
for i in id:
    ############################ connection #################################################
    # conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
    # my_cursor=conn.cursor()

   
    vn=(my_cursor.fetchall()[0])[0].decode()

    number={
        'PhoneNumber':vn
    
   

    ############################################## Number added to Flow ######################
    
    data={
        'VoiceUrl':'https://my.exotel.com/indeed11/exoml/start_voice/330382'
    }
    url ="https://indeed11:03fd80770e93125e3fed98956ef7a358a58e892d@twilix.exotel.in/v1/Accounts/indeed11/IncomingPhoneNumbers/{}".format(vn)
    x = requests.post(url,data=data)


########################################### Number added to LA #######################################
    url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/indeed11"

    j='+91'+str(int(vn))
    payload = json.dumps([
    {
        "greenvn": str(j),
        "region": "MU",
        "number_type": "landline"
    }
    ])
    headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Authorization': 'Basic dGVjaG9wczp0dzc1Znp2ZG53MnQ2N2Rq'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text,' : ',vn, "count : ", count)
    count+=1

        
        