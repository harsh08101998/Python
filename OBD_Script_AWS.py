import os,boto3,csv
import mysql.connector
from csv import DictWriter
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

## Ticket -- https://support.exotel.com/a/tickets/682272

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)
conn=mysql.connector.connect(host='10.0.3.97', user='postern', password='spyonme', database='exotel 
my_curosr=conn.cursor()
query="select count(*), status, tenant_id from obd where created>='{} 00:00:00' and created<='{} 23:59:59' group by status, tenant_id".format(startdate,lastdate)
my_curosr.execute(query)
harsh=my_curosr.fetchall()
with open('/tmp/OBD_Campaigns_Schedule_per_Tenant.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Count', 'Status','Tenant_ID'])
    csv_writer.writeheader()
    for i in harsh:
        first, second,third=i[0],i[1],i[2]
        csv_writer.writerow({
            'Count' : first,
            'Status' : second,
            'Tenant_ID' : third
        })

query2="select tenant_id,count(name) from obd where created BETWEEN '{} 00:00:00' AND '{} 23:59:59' GROUP BY tenant_id".format(startdate,lastdate)
my_curosr.execute(query2)
harsh2=my_curosr.fetchall()
with open('/tmp/OBD_Calls_per_Tenant.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Tenant_ID','Count'])
    csv_writer.writeheader()
    for i in harsh2:
        first, second=i[0],i[1]
        csv_writer.writerow({
            'Tenant_ID' : first,
            'Count' : second
        })
conn.close()


sesClient = boto3.client('ses', region_name='us-east-1 
msg = MIMEMultipart()
recipients = "harsh.kumar@exotel.in"
msg['to'] = recipients
SENDER = "noreply@exotel.com"
msg.preamble = 'Multipart message.\n'
msg.set_charset("utf-8")
msg['Subject'] = 'Data Request | OBD (Auto Dialer) From {} - TO {}'.format(startdate,lastdate)
body="Please find OBD (Auto Dialer) Data files  in attachement."
body = MIMEText(body) # convert the body to a MIME compatible string
msg.attach(body) # attach it to your main message
  
if os.path.isfile('/tmp/OBD_Campaigns_Schedule_per_Tenant.csv :
    part = MIMEApplication(open('/tmp/OBD_Campaigns_Schedule_per_Tenant.csv', 'rb .read())
    part.add_header('Content-Disposition', 'attachment',
                        filename="OBD_Campaigns_Schedule_per_Tenant.csv")
    msg.attach(part)
    
if os.path.isfile('/tmp/OBD_Calls_per_Tenant.csv :
    part1 = MIMEApplication(open('/tmp/OBD_Calls_per_Tenant.csv', 'rb .read())
    part1.add_header('Content-Disposition', 'attachment',
                        filename="OBD_Calls_per_Tenant.csv")
    msg.attach(part1)
sesClient.send_raw_email( Source=SENDER,  Destinations=recipients.split(', , RawMessage={'Data': msg.as_string()} )

