import mysql.connector
import os,csv,boto3
from datetime import date, timedelta
from email.message import EmailMessage
from sys import maxsize
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)
########### Obelix SG Databases ###########################
def get_csv(query, *argv):
    conn=mysql.connector.connect(host='10.0.2.208', user='postern', password='Spyonme1$', database='obdialer 
    my_cursor=conn.cursor()
    my_cursor.execute(query)
    for i in argv:
        if i=='csv' or i=='CSV':
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
        

query1="select account_sid, count(*) from obd_campaigns where send_at BETWEEN '{} 00:00:00' AND '{} 23:59:59' group by account_sid".format(startdate,lastdate)
query2="select account_sid , count(*), status from obd_call_schedule where date_created BETWEEN '{} 00:00:00' AND '{} 23:59:59'  group by account_sid, status".format(startdate,lastdate)
query3="SELECT Sid,account_sid,(LENGTH(`from`) - LENGTH(REPLACE(`from`,\",\",\"\")) + 1) AS MyCol2Count FROM obd_campaigns where send_at BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(startdate,lastdate)

print(query1)
print(query2)
print(query3)
print(get_csv(query1,'csv','Total_Number_of_Campaign_triggered.csv )
print(get_csv(query2,'csv','Number_of_calls_that_happened_per_tenant.csv )
print(get_csv(query3,'csv','User_count_Per_Campaign.csv )

############ Email sending part ###########################

# sesClient = boto3.client('ses', region_name='us-east-1 
# msg = MIMEMultipart()
# recipients = "harsh.kumar@exotel.in,partha.mandal@exotel.in,techsupport@exotel.in"
# msg['to'] = recipients
# SENDER = "noreply@exotel.com"
# msg.preamble = 'Multipart message.\n'
# msg.set_charset("utf-8")
# msg['Subject'] = 'NEW OBD Campaign Data From {} - TO {}'.format(startdate,lastdate)
# body="Please find NEW OBD Campaign Data files  in attachement."
# body = MIMEText(body) # convert the body to a MIME compatible string
# msg.attach(body) # attach it to your main message
  
# if os.path.isfile('Total_Number_of_Campaign_triggered.csv :
#     part = MIMEApplication(open('Total_Number_of_Campaign_triggered.csv', 'rb .read())
#     part.add_header('Content-Disposition', 'attachment',
#                         filename="Total_Number_of_Campaign_triggered.csv")
#     msg.attach(part)
    
# if os.path.isfile('Number_of_calls_that_happened_per_tenant.csv :
#     part1 = MIMEApplication(open('Number_of_calls_that_happened_per_tenant.csv', 'rb .read())
#     part1.add_header('Content-Disposition', 'attachment',
#                         filename="Number_of_calls_that_happened_per_tenant.csv")
#     msg.attach(part1)

# if os.path.isfile('User_count_Per_Campaign.csv :
#     part2 = MIMEApplication(open('User_count_Per_Campaign.csv', 'rb .read())
#     part2.add_header('Content-Disposition', 'attachment',
#                         filename="User_count_Per_Campaign.csv")
#     msg.attach(part2)

# sesClient.send_raw_email( Source=SENDER,  Destinations=recipients.split(', , RawMessage={'Data': msg.as_string()} )
