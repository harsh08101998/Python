import csv
import mysql.connector
from csv import DictWriter
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_curosr=conn.cursor()
query="select Sum(a.Amount) as Amount, p.FcvPlan , o.Name,p.pilot from PriUsage a join Pri p on (a.Pri = p.id) join FcvPlan f on (f.id = p.FcvPlan) join Operator o on (o.id=f.Operator) where a.Pri in (select id from Pri where FcvPlan in (select id from FcvPlan)) and a.UsageDate >='{} 00:00:00'and a.UsageDate <= '{} 23:59:59' group by p.FcvPlan order by f.Operator".format(startdate,lastdate)
print(query)
my_curosr.execute(query)
main_data=my_curosr.fetchall()
print(main_data)
with open('SG_FCV_DATA.csv','w',newline='  as fr:
    csv_writer=DictWriter(fr,fieldnames=['Amount', 'FcvPlan','Operator_Name','Pilot'])
    csv_writer.writeheader()
    for i in main_data:
        first, second,third,fourth=i[0],i[1],i[2].decode(),i[3].decode()
        csv_writer.writerow({
            'Amount' : first,
            'FcvPlan' : second,
            'Operator_Name' : third,
            'Pilot': fourth
        })



conn.close()



############ Email sending part ###########################

sesClient = boto3.client('ses', region_name='us-east-1 
msg = MIMEMultipart()
recipients = "harsh.kumar@exotel.in,partha.mandal@exotel.in,techsupport@exotel.in,ankush@exotel.in"
#recipients="harsh.kumar@exotel.in"
msg['to'] = recipients
SENDER = "noreply@exotel.com"
msg.preamble = 'Multipart message.\n'
msg.set_charset("utf-8")
msg['Subject'] = 'List of all FCVs with Utilization FromFrom {} - TO {}'.format(startdate,lastdate)
body="Please find list of all FCVs with Utilization Data files in attachement."
body = MIMEText(body) # convert the body to a MIME compatible string
msg.attach(body) # attach it to your main message


if os.path.isfile('SG_FCV_DATA.csv :
    part = MIMEApplication(open('SG_FCV_DATA.csv', 'rb .read())
    part.add_header('Content-Disposition', 'attachment',
                        filename="SG_FCV_DATA.csv")
    msg.attach(part)
sesClient.send_raw_email( Source=SENDER,  Destinations=recipients.split(', , RawMessage={'Data': msg.as_string()} )
