import mysql.connector
import os,csv,json
# import boto3
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart



## Ticket -- https://support.exotel.com/a/tickets/682270

# lastdate=date.today().replace(day=1) - timedelta(days=1)
# startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)
lastdate='2023-01-31'
startdate='2023-01-01'


#####################################  Campaign API Part ##############################################################################################
####################################################################################################################################################

################### Connection of campaignix DB ############################################
conn3=mysql.connector.connect(host='10.0.128.20', user='postern', password='spyonme', database='campaignix 
my_cursor3=conn3.cursor()


######  Total Number of Campaigns triggered by each tenant  in Campaig API.  #########################
query5="select account_sid as Tenant_ID , count(*) as Campaing_Count from campaigns where send_at >='{} 00:00:00' and send_at <='{} 23:59:59' group by account_sid".format(startdate,lastdate)
print(query5)
my_cursor3.execute(query5)
data=my_cursor3.fetchall()
listt_api=[]
for i in data:       ## List of Tenant_Name 
    listt_api.append(i[0])
print(listt_api)

dict5={}
for i in data:    
    tenant_id = i[0]
    total_camp = i[1]
    dict5[tenant_id] = total_camp

# ########### Total Number of calls happened per tenant through Campaigns  in API.  #################
#query6="select campaigns.account_sid as Tenant_ID , count(*) as Calls_Happened_Count from calls join campaigns on calls.campaign_sid =campaigns.sid where calls.date_created >='{} 00:00:00' and calls.date_created <='{} 23:59:59' group by campaigns.account_sid".format(startdate,lastdate)
total_calls={}
total_completed_calls={}

for i in listt_api:
    print(i)
    query6="select count(*) from calls where campaign_sid in(select sid from campaigns where send_at >='{} 00:00:00' and send_at <='{} 23:59:59' and account_sid='{} ".format(startdate,lastdate,i)
    my_cursor3.execute(query6)
    data2=my_cursor3.fetchall()
    total_calls_count = data2[0][0]
    total_calls[i] = total_calls_count

# ############  Total Number of Completed Calls per tenant through Campaigns in API.  ################
    query7="select count(*) from calls where campaign_sid in(select sid from campaigns where send_at >='{} 00:00:00' and send_at <='{} 23:59:59' and account_sid='{}  and calls.status='completed'".format(startdate,lastdate,i)

    my_cursor3.execute(query7)
    data3=my_cursor3.fetchall()
    complete_calls = data3[0][0]
    total_completed_calls[i] = complete_calls

print(total_calls)
print(total_completed_calls)
# ##################################################
stat_dict_camp={}
for i in listt_api:
    stat2_dict_camp={}
    query="select account_sid,stats from campaigns where account_sid='{}' and send_at>='{} 00:00:00' and send_at <='{} 23:59:59'".format(i,startdate,lastdate)
    print(query)
    my_cursor3.execute(query)
    result=my_cursor3.fetchall()
    created,in_progress,retry,retrying,failed,failed_dnd,invalid,paused,failed_no_attempt=0,0,0,0,0,0,0,0,0
    for j in result:
        res = json.loads(j[1])
        try:
            created+=res["created"]
        except KeyError:
            continue
        try:
            in_progress+=res["in-progress"]
        except KeyError:
            continue
        try:
            retry+=res["retry"]
        except KeyError:
            continue
        try:
            retrying+=res["retrying"]
        except KeyError:
            continue
        try:
            failed+=res["failed"]
        except KeyError:
            continue
        try:
            failed_dnd+=res["failed-dnd"]
        except KeyError:
            continue
        try:
            invalid+=res["invalid"]
        except KeyError:
            continue
        try:
            paused+=res["paused"]
        except KeyError:
            continue
        try:
            failed_no_attempt+=res["failed-no-attempt"]
        except KeyError:
            continue

    stat2_dict_camp["created"]=created; stat2_dict_camp["in_progress"]= in_progress;stat2_dict_camp["retry"]= retry;stat2_dict_camp["retrying"]= retrying;stat2_dict_camp["failed"]= failed;stat2_dict_camp["failed_dnd"]= failed_dnd;stat2_dict_camp["invalid"]= invalid;stat2_dict_camp["paused"]= paused;stat2_dict_camp["failed_no_attempt"]= failed_no_attempt
    stat_dict_camp[i]=stat2_dict_camp

##############################################
############################### Entry in CSV FILE #############################################
with open("Campaign_API_Data.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['Tenant_Name','Campaign_Count','Toatal_Calls','Completed_Calls','created','in_progress','retry','retrying','failed','failed_dnd','invalid','paused','failed_no_attempt'])
    file_writer.writeheader()
    for i in listt_api:
        file_writer.writerow({
           'Tenant_Name' :i,
           'Campaign_Count' : dict5.get(i),
           'Toatal_Calls' : total_calls.get(i),
           'Completed_Calls' : total_completed_calls.get(i),
           'created' :(stat_dict_camp.get(i))['created'],
           'in_progress' :(stat_dict_camp.get(i))['in_progress'],
           'retry' :(stat_dict_camp.get(i))['retry'],
           'retrying' :(stat_dict_camp.get(i))['retrying'],
           'failed' :(stat_dict_camp.get(i))['failed'],
           'failed_dnd' :(stat_dict_camp.get(i))['failed_dnd'],
           'invalid' :stat_dict_camp.get(i)['invalid'],
           'paused' :(stat_dict_camp.get(i))['paused'],
           'failed_no_attempt' :(stat_dict_camp.get(i))['failed_no_attempt'],
        })
    print("Data Sent")

conn3.close()

############ Email sending part ###########################

# sesClient = boto3.client('ses', region_name='us-east-1 
# msg = MIMEMultipart()
# #recipients = "harsh.kumar@exotel.in,partha.mandal@exotel.in,techsupport@exotel.in,ankush@exotel.in"
# recipients="harsh.kumar@exotel.in"
# msg['to'] = recipients
# SENDER = "noreply@exotel.com"
# msg.preamble = 'Multipart message.\n'
# msg.set_charset("utf-8")
# msg['Subject'] = 'Campaign API Data From {} - TO {}'.format(startdate,lastdate)
# body="Please find Campaign API Data files  in attachement."
# body = MIMEText(body) # convert the body to a MIME compatible string
# msg.attach(body) # attach it to your main message


# if os.path.isfile('Campaign_API_Data.csv :
#     part = MIMEApplication(open('Campaign_API_Data.csv', 'rb .read())
#     part.add_header('Content-Disposition', 'attachment',
#                         filename="Campaign_API_Data.csv")
#     msg.attach(part)
# sesClient.send_raw_email( Source=SENDER,  Destinations=recipients.split(', , RawMessage={'Data': msg.as_string()} )
