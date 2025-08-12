import datetime,csv, time
import mysql.connector
from datetime import date, timedelta
# Get current time in local timezone
with open("SMS_DATA_2_hourss2.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['AccountSid','FromTime','ToTime','Sum_Units'])
    file_writer.writeheader()
    current_time = datetime.datetime(2022, 7, 1, 0, 0, 0)
    h=0
    conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
    my_cursor=conn.cursor()
    
    # listt=['capitalfloat','dunzo4','khatabook1','paysense ','urbanclap8','flipkarthealthplus1','dreamplug','apna53','vipatra1','vastuhfc','zivame','bitlasoft2','shiprocket1']
    # for sidd in listt :
    for i in range(0,745):
        n = 2
        future_time = current_time + timedelta(hours=n)
        print(current_time, future_time)
        query="select AccountSid,count(*) from SMSMessage where DateCreated > '{}' and DateCreated < '{}' and (JSON_EXTRACT(_internal,'$.dltTemplateId = '' or _internal not like '%dltTemplateId%' ) and _SmsType ='promotional' and AccountSid in('capitalfloat','dunzo4','khatabook1','paysense ','urbanclap8','flipkarthealthplus1','dreamplug','apna53','vipatra1','vastuhfc','zivame','bitlasoft2','shiprocket1  group by AccountSid".format(current_time,future_time)
        print(query)
        my_cursor.execute(query)
        kk=my_cursor.fetchall()
        for i in kk:
            h2=0
            for j in i:
                if h2==0:
                    Price=j.decode()
                if h2==1:
                    count=j
                h2+=1
            file_writer.writerow({
                'AccountSid':Price,
                'FromTime':current_time,
                'ToTime':future_time,
                # 'DateCreated':datec,
                'Sum_Units' :count,
                })
        current_time=future_time
