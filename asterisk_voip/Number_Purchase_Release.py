from io import TextIOBase
import requests
import mysql.connector

################### Twilix DB connection #############################
conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()

print("Enter 1 for Purchase Numbers  \nEnter 2 for Release Numbers ")
choice=int(input(""))
if choice==1:
    id=input("Enter Number Phone Number : ").split(', 
    accountsid=input("Enter Client Accountsid : ")
    for i in id:
        query="select AuthToken from Account where Sid='{}'".format(accountsid)
        print(query)
        my_cursor.execute(query)
        token=(my_cursor.fetchall()[0])[0].decode()
        data={
            'PhoneNumber':int(i)
        }
        url="https://{}:{}@twilix.exotel.in/v1/Accounts/{}/IncomingPhoneNumbers/IN/Purchase".format(accountsid,token,accountsid)
        x = requests.post(url, data=data)
        print(x.text)

elif choice==2:
    id=input("Enter Number Phone Number : ").split(', 
    accountsid=input("Enter Client Accountsid : ")
    for i in id:
        query="select AuthToken from Account where Sid='{}'".format(accountsid)
        print(query)
        my_cursor.execute(query)
        token=(my_cursor.fetchall()[0])[0].decode()
        data={
            'PhoneNumber':int(i)
        }
        url="https://{}:{}@twilix.exotel.in/v1/Accounts/{}/IncomingPhoneNumbers/IN/Release".format(accountsid,token,accountsid)
        x = requests.delete(url, data=data)
        print(x.text)
