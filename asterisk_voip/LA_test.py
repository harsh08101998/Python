import time
import requests,json
import mysql.connector



#select Id,PhoneNumber,Region,Operator, _state, _ReservedFor, AccountSid From twilix.AvailablePhoneNumber where AccountSid is Null and _state='pn' and Region='TN' and Operator=5 and Rental <0 and _ReservedFor is NUll  and PhoneNumber not in(select PhysicalNumber from twilix.PhysicalVirtualMap) and _Pri in(select id from twilix.Pri where pilot=4471819201) limit 1900;

# accountsid=input("Enter Client Accountsid : ")
accountsid='zomato127'

conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()
query="select AuthToken from Account where Sid='{}'".format(accountsid)
my_cursor.execute(query)
token=(my_cursor.fetchall()[0])[0].decode()

    ############################ connection #################################################
    # conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
    # my_cursor=conn.cursor()

    ######################## Number converting to VN #########################
def convert_vn_to_pn(i):
    data={
        "Rental":"499",
        "_state":"available"
    }
    url="https://default:f7127af352491a86127aad77d7a1419e9ca3cef4@api.exotel.com/v1/Accounts/default/AvailablePhoneNumbers/{}/makevn.json".format(i)
    y=requests.post(url,data=data)
    
def Number_Reserve(i,accountsid):
    ###################### NUmber Reservation #####################################
    url="https://default:f7127af352491a86127aad77d7a1419e9ca3cef4@twilix.exotel.in/v1/Accounts/default/AvailablePhoneNumbers/{}.json?_state=reserved&_ReservedFor={}".format(int(i),accountsid)
    x = requests.post(url)
    
def Number_Purchase(vn,accountsid,token):
    ################### Number Purchase #####################################

    number={
        'PhoneNumber':vn
    }
    url="https://{}:{}@twilix.exotel.in/v1/Accounts/{}/IncomingPhoneNumbers/IN/Purchase".format(accountsid,token,accountsid)
    z = requests.post(url, data=number)
   

def number_added_to_flow(vn):
    ############################################## Number added to Flow ######################
    
    data={
        'VoiceUrl':'https://my.exotel.com/zomato127/exoml/start_voice/362431'
    }
    url ="https://zomato127:becef9db5e37d0b48164329631b99401b2a5ea0f@twilix.exotel.in/v1/Accounts/zomato127/IncomingPhoneNumbers/{}".format(vn)
    x = requests.post(url,data=data)


########################################### Number added to LA #######################################
def LA(vn):
    url = "https://leadassist.exotel.in/v1/internal/tenants/techops/add-greenvn/zomato127"

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
   



id=input("Enter Number ID's : ").split(', 
for i in id:
    query1="select PhoneNumber from AvailablePhoneNumber where id='{}'".format(i)
    my_cursor.execute(query1)
    vn=(my_cursor.fetchall()[0])[0].decode()

    a=convert_vn_to_pn(i)
    b=Number_Reserve(i,accountsid)
    c=Number_Purchase(vn,accountsid,token)
    d=number_added_to_flow(vn)
    e=LA(vn)
        
