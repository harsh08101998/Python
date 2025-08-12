from io import TextIOBase
import requests
import mysql.connector
import sys, csv, time

################### Twilix DB connection #############################
conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
twxconn=conn.cursor()


def purchase(phonenumbers,accountsid):
    accountsid=accountsid
    n=len(phonenumbers)
    print(n)
    a=phonenumbers[0:n]
    print(a)
    phonenumbers1=a.replace(", ",",")
    print(phonenumbers1)
    phonenumbers1=phonenumbers1.split(', 
    print(phonenumbers1)

    a=len(phonenumbers1)
    print(a)
    phonenumbers2=phonenumbers
    phonenumbers3=phonenumbers2.replace(",","','")
    print(phonenumbers3)
    query = "select count(id) from AvailablePhoneNumber where PhoneNumber in ('"+phonenumbers3+"  and _state ='reserved' AND Rental > 0 AND  NumberType='Landline' AND AccountSid IS NULL AND _ReservedFor='"+accountsid+"'"
    print(query)
    # res = get_results(twxcur, query)
    twxconn.execute(query)
    token=(twxconn.fetchall())
    # b=res[0]['count(id)']
    print(a)
    print(token)
    # if int(a)==int(b):
    #     print('done 

purchase(sys.argv[1],sys.argv[2])