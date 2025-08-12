import mysql.connector
from prettytable import from_db_cursor
import csv
import os,sys


# sys.path.insert(0, '/home/exotel/bumblebee/internal')
# import text_utils
# import logging.config
# import boto3

# accountsid=sys.argv[1]
# start_date=sys.argv[2]
# end_date=sys.argv[3]
# report_name=sys.argv[4]

accountsid='exotel905'
start_date='2022-04-21 00:00:00'
end_date='2022-04-29 23:59:59'
report_name='exotel905_report.csv'

conn=mysql.connector.connect(host='10.0.0.10', user='postern', password='spyonme', database='exotel')
my_cursor=conn.cursor()


############################################# Mail sending part ########################################################################       
def send_ses_email(csv_name, to, count, for_mail):
    sesClient = boto3.client('ses', region_name='us-east-1')
    msg = MIMEMultipart()
    msg['to'] = to
    SENDER = "noreply@exotel.com"
    name = to.split("@")[0].title()
    msg.preamble = 'Multipart message.\n'
    msg.set_charset("utf-8")
    msg['Subject'] = "Call Report Data for {}".format(accountsid)
    part = MIMEText(
        "Hey " + name + " \n\n-- Here is the data that you've requested.\n\n " + str(for_mail) )
    msg.attach(part)
    if os.path.isfile(csv_name):
        part = MIMEApplication(open(csv_name, 'rb').read())
        part.add_header('Content-Disposition', 'attachment',
                        filename=csv_name)
        msg.attach(part)
    result = sesClient.send_raw_email( Source=SENDER, Destinations=[msg['to']], RawMessage={'Data': msg.as_string()} )
    return result

############################### take input in CSV  ##########################################################

def get_output_into_csv(report_name,row_name,hh):
    # row_name=my_cursor.description
    listt=[]
    for i in row_name:
        listt.append(i[0])
    with open(report_name, 'w', newline="") as fopen:
        csvwrite=csv.DictWriter(fopen,fieldnames=listt)
        csvwrite.writeheader()
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
    # mailsend=send_ses_email(report_name,email, for_mail)
    # print(mailsend)
    # if mailsend:
    #     print("Mail sent successfully")
    #     os.unlink(csv_name)



query='''select start_date, end_date, url from report where tenant_id in(select id from tenants where name="{}")  and type='call'  and _internal= '{}' and start_date='{}' and end_date="{}"'''.format(accountsid,str('{"VN":null}'),start_date,end_date)
my_cursor.execute(query)
row_name=my_cursor.description
hh=my_cursor.fetchall()

if hh:
    get_output_into_csv(report_name,row_name,hh)

else:
    query2='''select start_date, end_date, url from report where tenant_id in(select id from tenants where name='{}') and type='call' and _internal= '{}' and (start_date between DATE_SUB('{}', INTERVAL 10 DAY) and DATE_ADD('{}', INTERVAL 10 DAY) OR end_date between DATE_SUB('{}', INTERVAL 10 DAY) and DATE_ADD('{}', INTERVAL 10 DAY) ) order by start_date asc'''.format(accountsid,str('{"VN":null}'),start_date,end_date,start_date,end_date)
    my_cursor.execute(query2)
    hh2=my_cursor.fetchall()
    if hh2:
        get_output_into_csv(report_name,row_name,hh2)
    else:
        print('No reports present for this tenant, for given time')

