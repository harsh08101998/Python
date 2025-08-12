import datetime,csv
import mysql.connector
from datetime import date, timedelta
from datetime import datetime,timedelta

# Get current time in local timezone
with open("SMS_DATA_2_hourss.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['AccountSid','To','From', 'Body','Status','_SmsType','_Pipe'])
    file_writer.writeheader()
    current_time = datetime.now()
    h=0
    conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
    my_cursor=conn.cursor()
    for i in range(0,276):
        
        n = 2
        future_time = current_time - timedelta(hours=n)
        print(current_time, future_time)
        query="select AccountSid,`To`,`From`,Body,_SmsType,_Pipe,Status from SMSMessage where `To` like '+60%' and DateCreated>='{}' and DateCreated<'{}'".format(current_time,future_time)
        my_cursor.execute(query)
        kk=my_cursor.fetchall()
        for i in kk:
            h2=0
            for j in i:
                if h2==0:
                    accountsid=j.decode()
                # if h2==1:
                #     datec=j.decode()
                if h2==1:
                    too=j.decode()
                if h2==2:
                    fromm=j.decode()
                if h2==3:
                    boddy=j.decode()    
                if h2==4:
                    smstype=j.decode()
                if h2==5:
                    pipe=j.decode()
                if h2==6:
                    status=j.decode()
                h2+=1
            file_writer.writerow({
                'AccountSid':accountsid,
                # 'DateCreated':datec,
                'To' :too,
                'From' :fromm,
                'Body' :boddy,
                '_SmsType':smstype,
                '_Pipe':pipe,
                'Status':status
                })

        current_time=future_time
