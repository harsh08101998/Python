import mysql.connector
from prettytable import from_db_cursor
import csv
from datetime import date, timedelta
import os,csv,boto3
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


########### For making CSV ###########################
def get_csv(host_ip, user_name, password, database_name, query, *argv):
    conn=mysql.connector.connect(host=host_ip, user=user_name, password=password, database=database_name)
    my_cursor=conn.cursor()
    my_cursor.execute(query)
    for i in argv:
        if i=='Table' or i=='table':
            data=from_db_cursor(my_cursor)
            return data
        elif i=='Normal' or i=='normal':
            data=my_cursor.fetchall()
            return data
        elif i=='csv' or i=='CSV':
            file_name=argv[1]
            row_name=my_cursor.description
            listt=[]
            for i in row_name:
                listt.append(i[0])
            with open(file_name, 'w', newline="") as fopen:
                csvwrite=csv.DictWriter(fopen,fieldnames=listt)
                csvwrite.writeheader()
                hh=my_cursor.fetchall()
                for i in hh:
                    listt2=[]
                    for j in i:
                        if str(type(j))=="<class 'bytearray'>":
                            listt2.append(j.decode())
                        else:
                            listt2.append(j)
                    count=0
                    try:
                        dict={}
                        for i in listt:
                            dict[i]=listt2[count]
                            count+=1
                        csvwrite.writerow(dict)
                    except IndexError:
                       continue
            return "File created"
        else:
            data2=my_cursor.fetchall()
            return data2



################################# Product DB Access ###################################
def Product_DB(query1,*argv):
    data=get_csv('10.0.2.208', 'postern','Spyonme1$', 'zoho_crm',query1, *argv)
    return data

def Product_DB_Desk(query1,*argv):
    data=get_csv('10.0.2.208', 'postern','Spyonme1$', 'zoho_desk',query1, *argv)
    return data

def Billix_Small_Table(query1,*argv):
    data=get_csv('10.0.3.163','postern', 'spyonme', 'billix2',query1, *argv)
    return data

####################### For getting Time ######################################
lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

########################## Zoho - CRM Mysql Quries ####################################

query1="select accountSid, createdOn, status   from exotel_account where createdOn BETWEEN '{} 00:00:00' AND '{} 23:59:59'  order by createdOn asc".format(startdate,lastdate)
Product_DB(query1, 'csv','Zoho_CRM_Tenants_Enabled.csv 

query2="select count(*) as Call_Count, callType  from exotel_call_log where createdOn BETWEEN '{} 00:00:00' AND '{} 23:59:59' group by callType".format(startdate,lastdate)
hh=Product_DB(query2, 'normal','Zoho_CRM_Tenants_Enabled.csv 

Inbound = 'Count of Inbound Call for Zoho CRM is :- {}'.format(hh[0][0])
Outbound = 'Count of Outbound Call for Zoho CRM is :- {}'.format(hh[1][0])

print(Inbound, '\n', Outbound)

query3="select accountSid, count(*) from zoho_user group by accountSid"
Product_DB(query3, 'csv','Zoho_CRM_User_Count.csv 

query4="select accountSid from exotel_account where status = 'active'"
listt=Product_DB(query4, 'normal','tt.csv 
zoho_crm_account_list=[]
for i in listt:
    zoho_crm_account_list.append(i[0])

revenue="select sum(Quantity), sum(Amount) as InvoiceAmount, AccountSid from AggregateUsage where AccountSid in {} and SkuId='call' and FromTime>='{} 00:00:00' and FromTime<='{} 23:59:59' group by AccountSid".format(tuple(zoho_crm_account_list),startdate, lastdate)
Billix_Small_Table(revenue, 'csv','Zoho_CRM_Tenant_Revenue.csv 



########################## Zoho - Desk Mysql Quries ####################################

query1=" select sid, createdOn, status   from exotel_account where createdOn >= '{} 00:00:00' and createdOn < '{} 23:59:59' order by createdOn asc".format(startdate,lastdate)
Product_DB_Desk(query1, 'csv','Zoho_Desk_Tenants_Enabled.csv 

query2="select count(*), callType  from exotel_call_log where createdOn > '{} 00:00:00'  and createdOn < '{} 23:59:59' group by callType ;".format(startdate,lastdate)
hh=Product_DB_Desk(query2, 'normal','Zoho_CRM_Tenants_Enabled.csv 

Inbound1 = 'Count of Inbound Call for Zoho Desk is :- {}'.format(hh[0][0])
Outbound1 = 'Count of Outbound Call for Zoho Desk is :- {}'.format(hh[1][0])

print(Inbound1, '\n', Outbound1)

query3="select exotel_account.sid , count(*) from zoho_user JOIN exotel_account on exotel_account.id=zoho_user.exotelId group by zoho_user.exotelId"
Product_DB_Desk(query3, 'csv','Zoho_Desk_User_Count.csv 

query4="select sid from exotel_account where status ='active'"
listt=Product_DB_Desk(query4, 'normal','tt.csv 
zoho_desk_account_list=[]
for i in listt:
    zoho_desk_account_list.append(i[0])


revenue="select sum(Quantity), sum(Amount) as InvoiceAmount, AccountSid from AggregateUsage where AccountSid in {} and SkuId='call' and FromTime>='{} 00:00:00' and FromTime<='{} 23:59:59' group by AccountSid".format(tuple(zoho_desk_account_list),startdate, lastdate)
Billix_Small_Table(revenue, 'csv','Zoho_Desk_Tenant_Revenue.csv 


########### Email sending part ###########################

sesClient = boto3.client('ses', region_name='us-east-1 
msg = MIMEMultipart()
recipients = "harsh.kumar@exotel.in"
msg['to'] = recipients
SENDER = "noreply@exotel.com"
msg.preamble = 'Multipart message.\n'
msg.set_charset("utf-8")
msg['Subject'] = 'Zoho integration Data From {} - TO {}'.format(startdate,lastdate)
body="Zoho integration Data files  in attachement.\n\n\n {} \n {} \n\n\n\n {} \n {}".format(Inbound, Outbound, Inbound1,Outbound1 )
body = MIMEText(body) # convert the body to a MIME compatible string
msg.attach(body) # attach it to your main message

if os.path.isfile('Zoho_CRM_Tenants_Enabled.csv :
    part = MIMEApplication(open('Zoho_CRM_Tenants_Enabled.csv', 'rb .read())
    part.add_header('Content-Disposition', 'attachment',
                        filename="Dashboard_Campaign_Data.csv")
    msg.attach(part)

if os.path.isfile('Campaign_API_Data.csv :
    part1 = MIMEApplication(open('Campaign_API_Data.csv', 'rb .read())
    part1.add_header('Content-Disposition', 'attachment',
                        filename="Campaign_API_Data.csv")
    msg.attach(part1)
sesClient.send_raw_email( Source=SENDER,  Destinations=recipients.split(', , RawMessage={'Data': msg.as_string()} )