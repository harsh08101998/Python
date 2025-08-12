import mysql.connector
import os,csv,boto3,json
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


## Ticket -- https://support.exotel.com/a/tickets/682270

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

##################### Connection of Obelix Small Table ######################################
conn=mysql.connector.connect(host='10.0.0.10', user='postern', password='spyonme', database='exotel 
my_cursor=conn.cursor()
query1=" select a.name,a.id,count(b.tenant_id) from tenants a , campaigns b where scheduled BETWEEN '{} 00:00:00' AND '{} 23:59:59' AND a.id = b.tenant_id GROUP BY b.tenant_id".format(startdate,lastdate)
my_cursor.execute(query1)
data=my_cursor.fetchall()
listt=[]
acount_sid_list=[]
for i in data:
    listt.append(i[1])
    acount_sid_list.append(i[0])

################################ Dict file of Campaign and Tenant Name #################
dict1={}
dict2={}
for i in data:    
    tenant_name = i[0]
    tenant_id = i[1]
    camp=i[2]
    dict1[tenant_id] = tenant_name
    dict2[tenant_id]=camp


########################## For Campaign Count per Tenant #######################################
query2="select  distinct id from exotel.campaigns where scheduled BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(startdate,lastdate)
my_cursor.execute(query2)
data2=my_cursor.fetchall()
ll=[]
for i in data2:
    for j in i:
        ll.append(j)
main_list=tuple(ll)



######################################  For States ##########################################
stat_dict={}
for i in listt:
    stat2_dict={}
    query="select tenant_id,stats from campaigns where tenant_id={} and scheduled>='{} 00:00:00' and scheduled <='{} 23:59:59'".format(i,startdate,lastdate)
    data=my_cursor.execute(query)
    result=my_cursor.fetchall()
    scheduled,in_progress,failed,failed_dnd,failed_balance,invalid=0,0,0,0,0,0
    for j in result:
        res = json.loads(j[1])
        try:
            scheduled+=res["scheduled"]
        except KeyError:
            continue
        try:
            in_progress+=res["in-progress"]
        except KeyError:
            continue
        try:
            failed+=res["failed"]
        except KeyError:
            continue
        try:
            failed_dnd+=res["failed_dnd"]
        except KeyError:
            continue
        try:
            failed_balance+=res["failed_balance"]
        except KeyError:
            continue
        try:
            invalid+=res["invalid"]
        except KeyError:
            continue
  
   # state= ("scheduled:" ,h_scheduled,"in_progress:",in_progress,"failed:",failed,"success:",success,"failed_dnd:",failed_dnd,"failed_balance:",failed_balance,"invalid:",invalid)
    stat2_dict["scheduled"]=scheduled; stat2_dict["in_progress"]= in_progress;stat2_dict["failed"]= failed;stat2_dict["failed_dnd"]= failed_dnd;stat2_dict["failed_balance"]= failed_balance;stat2_dict["invalid"]= invalid
    stat_dict[i]=stat2_dict

conn.close()


###################### Connection of Obelix Big Table #################################
conn2=mysql.connector.connect(host='10.0.3.97', user='postern', password='spyonme', database='exotel 
my_cursor2=conn2.cursor()

############################### For Total Callss ########################################          
query3="select tenant,count(id) from outbound_queue where campaign_id in{} group by tenant".format(main_list)
my_cursor2.execute(query3)
data3=my_cursor2.fetchall()
dict3={}
for i in data3:    
    tenant_id = i[0]
    total_call = i[1]
    dict3[tenant_id] = total_call

###################################### For Completed Calls #################################################
query4="select tenant,count(id)  from outbound_queue where campaign_id in{} and status='success' group by tenant".format(main_list)
my_cursor2.execute(query4)
data4=my_cursor2.fetchall()
dict4={}
for i in data4:    
    tenant_id = i[0]
    completed_call = i[1]
    dict4[tenant_id] = completed_call


conn2.close()

############################## Entry in CSV FILE #############################################
with open("Dashboard_Campaign_Data.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['Tenant_Name','Campaign_Count','Toatal_Calls','Completed_Calls','scheduled','in_progress','failed','failed_dnd','failed_balance','invalid'])
    file_writer.writeheader()
    for i in listt:
        file_writer.writerow({
           'Tenant_Name' :dict1.get(i),
           'Campaign_Count' : dict2.get(i),
           'Toatal_Calls' : dict3.get(i),
           'Completed_Calls' : dict4.get(i),
           'scheduled' :(stat_dict.get(i))['scheduled'],
           'in_progress' :(stat_dict.get(i))['in_progress'],
           'failed' :(stat_dict.get(i))['failed'],
           'failed_dnd' :(stat_dict.get(i))['failed_dnd'],
           'failed_balance' :(stat_dict.get(i))['failed_balance'],
           'invalid' :(stat_dict.get(i))['invalid']

        })



#####################################  Campaign API Part ##############################################################################################
####################################################################################################################################################

################### Connection of campaignix DB ############################################
conn3=mysql.connector.connect(host='10.0.128.20', user='postern', password='spyonme', database='campaignix 
my_cursor3=conn3.cursor()


######  Total Number of Campaigns triggered by each tenant  in Campaig API.  #########################
query5="select account_sid as Tenant_ID , count(*) as Campaing_Count from campaigns where send_at >='{} 00:00:00' and send_at <='{} 23:59:59' group by account_sid".format(startdate,lastdate)
my_cursor3.execute(query5)
data=my_cursor3.fetchall()
listt_api=[]
for i in data:       ## List of Tenant_Name 
    listt_api.append(i[0])

dict5={}
for i in data:    
    tenant_id = i[0]
    total_camp = i[1]
    dict5[tenant_id] = total_camp

########### Total Number of calls happened per tenant through Campaigns  in API.  #################
query6="select campaigns.account_sid as Tenant_ID , count(*) as Calls_Happened_Count from calls join campaigns on calls.campaign_sid =campaigns.sid where calls.date_created >='{} 00:00:00' and calls.date_created <='{} 23:59:59' group by campaigns.account_sid".format(startdate,lastdate)
my_cursor3.execute(query6)
data2=my_cursor3.fetchall()
dict6={}
for i in data2:    
    tenant_id = i[0]
    total_calls = i[1]
    dict6[tenant_id] = total_calls


############  Total Number of Completed Calls per tenant through Campaigns in API.  ################
query7="select campaigns.account_sid as Tenant_ID, count(*) as Completed_Calls from calls join campaigns on calls.campaign_sid =campaigns.sid where calls.date_created >='{} 00:00:00' and calls.date_created <='{} 23:59:59' and calls.status='completed' group by campaigns.account_sid".format(startdate,lastdate)
my_cursor3.execute(query7)
data3=my_cursor3.fetchall()
dict7={}
for i in data3:    
    tenant_id = i[0]
    complete_calls = i[1]
    dict7[tenant_id] = complete_calls


##################################################
stat_dict_camp={}
for i in listt_api:
    stat2_dict_camp={}
    query="select account_sid,stats from campaigns where account_sid='{}' and send_at>='{} 00:00:00' and send_at <='{} 23:59:59'".format(i,startdate,lastdate)
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
           'Toatal_Calls' : dict6.get(i),
           'Completed_Calls' : dict7.get(i),
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

conn3.close()

