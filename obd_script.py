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
query="elect Sum(a.Amount) as Amount, p.FcvPlan , o.Name,p.pilot from PriUsage a join Pri p on (a.Pri = p.id) join FcvPlan f on (f.id = p.FcvPlan) join Operator o on (o.id=f.Operator) where a.Pri in (select id from Pri where FcvPlan in (select id from FcvPlan)) and a.UsageDate >='{} 00:00:00'and a.UsageDate <= '{} 23:59:59' group by p.FcvPlan order by f.Operator".format(startdate,lastdate)
print(query)
my_curosr.execute(query)
main_data=my_curosr.fetchall()
print(main_data)
# with open('SG_FCV_DATA.csv','w',newline='  as fr:
#     csv_writer=DictWriter(fr,fieldnames=['Count', 'Status','Tenant_ID'])
#     csv_writer.writeheader()
#     for i in harsh:
#         first, second,third=i[0],i[1],i[2]
#         csv_writer.writerow({
#             'Count' : first,
#             'Status' : second,
#             'Tenant_ID' : third
#         })



conn.close()

# msg=EmailMessage()
# msg['Subject']='Data Request | OBD (Auto Dialer) From {} - TO {}'.format(startdate,lastdate)
# msg['From']='Harsh Kumar <noreply@exotel.in'
# msg['To']='harsh.kumar@exotel.in'   # for sending multiple write multiple email seperated by comma
# msg.set_content("Please find OBD (Auto Dialer) Data files in attachement.")

# # with open('SMSTemplate.txt  as myfile:
# #     data=myfile.read()
# #     msg.set_content(data)

# with open('/tmp/OBD_Campaigns_Schedule_per_Tenant.csv','rb  as f:
#     file_data=f.read()
#     file_name='OBD_Campaigns_Schedule_per_Tenant.csv'
#     msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)

# with open('/tmp/OBD_Calls_per_Tenant.csv','rb  as f:
#     file_data=f.read()
#     file_name='OBD_Calls_per_Tenant.csv'
#     msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)

# server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.login("harsh.kumar@exotel.in","ydjkosppfnpgsvnq")
# server.send_message(msg)
# server.quit()
