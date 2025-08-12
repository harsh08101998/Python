import mysql.connector
from prettytable import from_db_cursor
import csv

connection=mysql.connector.connect(host='10.0.0.65',user='postern',password='spyonme',database='twilix 
my_cursor=connection.cursor()

connection2=mysql.connector.connect(host='10.0.0.65',user='postern',password='spyonme',database='twilix 
my_cursor2=connection2.cursor()

query="select p.AccountSid as AccountSid, p.VirtualNumber as VirtualNumber, p.PhysicalNumber as PhysicalNumber, a.Region as Region, o.Name as Operator,  a.NumberType as NumberType , I.VoiceUrl as AppId from PhysicalVirtualMap p LEFT OUTER JOIN AvailablePhoneNumber a on (p.VirtualNumber = a.PhoneNumber) JOIN IncomingPhoneNumber I on (I.PhoneNumber = a.PhoneNumber) JOIN Operator o on a.Operator = o.id where p.AccountSid = 'bundl' and I.DateCreated <= '2022-11-27 14:21:24.075636' order by p.VirtualNumber"
my_cursor.execute(query)
data=my_cursor.fetchall()
for x in data:
    result = []
    AccountSid = x[AccountSid]
    VirtualNumber = x['VirtualNumber']
    PhysicalNumber = x['PhysicalNumber']
    Region = x['Region']
    Operator = x['Operator']
    NumberType = x['NumberType']
    if x['AppId'] is None:
        AppId = ''
    else:
        AppId = ''.join(str(e) for e in [int(s) for s in x['AppId'].split("/") if s.isdigit()])
    flow_query = "select name from flows where id = '{AppId}';".format(AppId=AppId)
    print(VirtualNumber,AppId)