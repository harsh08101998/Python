from datetime import date, timedelta
import mysql.connector
import smtplib, csv
from email.message import EmailMessage
from sys import maxsize
import mysql.connector
lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

################### connection of fd-integration-db in (MUM stamp) ###########################
conn=mysql.connector.connect(host='10.1.220.27', user='postern', password='Spyonme1$', database='Exotel 
my_curosr=conn.cursor()

################### connection of Twilix small db ############################################
conn2=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_curosr2=conn2.cursor()


#-------------------------------------------------------------------------------------------------------
query="select exotelAccountSid , createdAt from accounts where createdAt BETWEEN '{} 00:00:00' and '{} 23:59:59'".format(startdate,lastdate)
my_curosr.execute(query)
data=my_curosr.fetchall()
listt=[]
for i in data:
    listt.append(i[0])

sid_list=tuple(listt)
dict={}
for i in data:
    exotelAccountSid=i[0]
    createdAt=i[1]
    dict[exotelAccountSid]=createdAt

#------------------------------------------------------------------------------------------------
query1="select Sid, Type from Account where Sid in{}".format(sid_list)
my_curosr2.execute(query1)
data1=my_curosr2.fetchall()
dict1={}
for i in data1:
    sid=i[0].decode()
    type=i[1].decode()
    dict1[sid]=type

#-------------------------------------------------------------------------------------
query2="select count(*) as Total_Count,callDirection from calls where createdAt BETWEEN '{} 00:00:00' and '{} 23:59:59' group by callDirection".format(startdate,lastdate)
my_curosr.execute(query2)
data2=my_curosr.fetchall()
dict2={}
for i in data2:
    Total_Count=i[0]
    callDirection=i[1]
    dict2[callDirection]=Total_Count

#------------------------------------------------------------------------------------------
query3="select count(*) , accountSid from usermappings where accountSid IN (select exotelAccountSid from accounts where createdAt BETWEEN '{} 00:00:00' and '{} 23:59:59  group by accountSid".format(startdate,lastdate)
my_curosr.execute(query3)
data3=my_curosr.fetchall()
dict3={}
for i in data3:
    count=i[0]
    accountsid=i[1]
    dict3[accountsid]=count

############################## Entry in CSV Part ##############################
with open('Tenants_Detail.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['ExotelAccountSid', 'CreatedAt',])
    csv_writer.writeheader()
    for i in dict:
        first, second=i[0],i[1]
        csv_writer.writerow({
            'ExotelAccountSid' : first,
            'CreatedAt' : second
           
        })

with open('Incomding_Outbound_Calls.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Call_Direction', 'Count',])
    csv_writer.writeheader()
    for i in dic2:
        first, second=i[0],i[1]
        csv_writer.writerow({
            'Call_Direction' : first,
            'Count' : second
           
        })

with open('User_Mapped_Data.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['AccountSid', 'Count',])
    csv_writer.writeheader()
    for i in dict3:
        first, second=i[0],i[1]
        csv_writer.writerow({
            'AccountSid' : first,
            'Count' : second
           
        })