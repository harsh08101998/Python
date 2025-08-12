import csv
import mysql.connector
from csv import DictWriter
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

################ connection to obelix big db ################################
conn=mysql.connector.connect(host='10.0.3.97', user='postern', password='spyonme', database='exotel 
my_curosr=conn.cursor()
############## connection to Obelix small table ########################
conn2=mysql.connector.connect(host='10.0.0.10', user='postern', password='spyonme', database='exotel 
my_curosr2=conn2.cursor()


query="select count(*), status, tenant_id from obd where created>='{} 00:00:00' and created<='{} 23:59:59' group by status, tenant_id".format(startdate,lastdate)
my_curosr.execute(query)
data=my_curosr.fetchall()
listt=[]
for i in data:
    listt.append(i[2])
tenant_list=tuple(listt)

query2="select id,name from tenants where id in{}".format(tenant_list)
my_curosr2.execute(query2)
data2=my_curosr2.fetchall()
tenant_detail={}
for i in data2:
    tenant_id=i[0]
    tenant_name=i[1]
    tenant_detail[tenant_id]=tenant_name


with open('OBD_Campaigns_Schedule_per_Tenant.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Tenant_Name','Status', 'Count'])
    csv_writer.writeheader()
    for i in data:
        first, second,third=i[0],i[1],i[2]
        csv_writer.writerow({
            'Tenant_Name' : tenant_detail.get(third),
            'Status' : second,
            'Count' : first            
            
        })

query2="select tenant_id,count(name) from obd where created BETWEEN '{} 00:00:00' AND '{} 23:59:59' GROUP BY tenant_id".format(startdate,lastdate)
my_curosr.execute(query2)
harsh2=my_curosr.fetchall()
with open('OBD_Calls_per_Tenant.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Tenant_Name','Count'])
    csv_writer.writeheader()
    for i in harsh2:
        first, second=i[0],i[1]
        csv_writer.writerow({
            'Tenant_Name' : tenant_detail.get(first),
            'Count' : second
        })


conn.close()

msg=EmailMessage()
msg['Subject']='Data Request | OBD (Auto Dialer) From {} - TO {}'.format(startdate,lastdate)
msg['From']='Harsh Kumar <noreply@exotel.in'
msg['To']='harsh.kumar@exotel.in'   # for sending multiple write multiple email seperated by comma
msg.set_content("Please find OBD (Auto Dialer) Data files in attachement.")

# with open('SMSTemplate.txt  as myfile:
#     data=myfile.read()
#     msg.set_content(data)

with open('/tmp/OBD_Campaigns_Schedule_per_Tenant.csv','rb  as f:
    file_data=f.read()
    file_name='OBD_Campaigns_Schedule_per_Tenant.csv'
    msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)

with open('/tmp/OBD_Calls_per_Tenant.csv','rb  as f:
    file_data=f.read()
    file_name='OBD_Calls_per_Tenant.csv'
    msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)

server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("harsh.kumar@exotel.in","ydjkosppfnpgsvnq")
server.send_message(msg)
server.quit()
