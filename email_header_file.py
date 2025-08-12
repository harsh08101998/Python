import csv
import mysql.connector
from csv import DictWriter
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize
from email.mime.text import MIMEText

from tabulate import tabulate


sid_list=('anujjindal2','bikayi1','coindcx1m','exotel550','futwork1','getfleek1','mybiznis1','onthegomodel1','probe 
conn2=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_curosr2=conn2.cursor()
query1="select Sid, Type from Account where Sid in{}".format(sid_list)
my_curosr2.execute(query1)
data1=my_curosr2.fetchall()
dict1={}
for i in data1:
    sid=i[0].decode()
    type=i[1].decode()
    dict1[sid]=type
print(dict1)


text = """
Hello, Friend.

Here is your data:

{table}

Regards,

Me"""

html = """
<html><body><p>Hello, Friend.</p>
<p>Here is your data:</p>
{table}
<p>Regards,</p>
<p>Me</p>
</body></html>
"""

with open('input.csv  as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

msg=EmailMessage()
msg['Subject']='Data Request | OBD (Auto Dialer) From'
msg['From']='Harsh Kumar <noreply@exotel.in'
msg['To']='harsh.kumar@exotel.in'   # for sending multiple write multiple email seperated by comma
msg.set_content("Please find OBD (Auto Dialer) Data files in attachement.")
body = MIMEText(body) # convert the body to a MIME compatible string
msg.attach(body) # attach it to your main messa

# with open('SMSTemplate.txt  as myfile:
#     data=myfile.read()
#     msg.set_content(data)


server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("harsh.kumar@exotel.in","ydjkosppfnpgsvnq")
server.send_message(msg)
server.quit()
