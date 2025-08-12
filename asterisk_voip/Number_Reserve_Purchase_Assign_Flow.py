import time
import requests,json
import mysql.connector

 ############################ connection #################################################
conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()


# accountsid=input("Enter Client Accountsid : ")
accountsid='squadrun1'


query="select AuthToken from Account where Sid='{}'".format(accountsid)
my_cursor.execute(query)
token=(my_cursor.fetchall()[0])[0].decode()

count=1
id=input("Enter Number ID's : ").split(', 

for i in id:
   
    
    ###################### NUmber Reservation #####################################
    url="https://default:f7127af352491a86127aad77d7a1419e9ca3cef4@twilix.exotel.in/v1/Accounts/default/AvailablePhoneNumbers/{}.json?_state=reserved&_ReservedFor={}".format(int(i),accountsid)
    x = requests.post(url)
    
    ################### Number Purchase #####################################
    
    query1="select PhoneNumber from AvailablePhoneNumber where id='{}'".format(i)
    my_cursor.execute(query1)
    vn=(my_cursor.fetchall()[0])[0].decode()

    number={
        'PhoneNumber':vn
    }
    url="https://{}:{}@twilix.exotel.in/v1/Accounts/{}/IncomingPhoneNumbers/IN/Purchase".format(accountsid,token,accountsid)
    z = requests.post(url, data=number)
   
    print(x,", : ",z,":",vn, " : count : ", count)

    ############################################## Number added to Flow ######################
    
    data={
        'VoiceUrl':'https://my.exotel.com/squadrun1/exoml/start_voice/294434'
    }
    url ="https://squadrun1:94c065450564c5a3e82e181026e4fd5e01f6d501@twilix.exotel.in/v1/Accounts/squadrun1/IncomingPhoneNumbers/{}".format(vn)
    x = requests.post(url,data=data)
    count+=1
    if count % 50== 0 :
        conn.close()
        conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
        my_cursor=conn.cursor()