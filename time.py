import datetime,csv
import mysql.connector
from datetime import date, timedelta
# Get current time in local timezone
with open("deccanherald1_sms_data.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['From_Date','To_Date','Status','SMS_count', 'unit_count',])
    file_writer.writeheader()
    current_time = datetime.datetime(2022, 2, 1, 0, 0, 0)
    h=0
    conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
    my_cursor=conn.cursor()
    for i in range(0,372):
        
        n = 2
        future_time = current_time + timedelta(hours=n)
        print(current_time, future_time)
        query="select count(*),  Status, sum(_NumUnits) from SMSMessage where AccountSid='deccanherald1' and DateCreated>='{}' and DateCreated<'{}' group by Status".format(current_time,future_time)
        my_cursor.execute(query)
        kk=my_cursor.fetchall()
        
        for i in kk:
            h2=0
            for j in i:
                if h2==0:
                    count=j
                if h2==1:
                    status=j.decode()
                if h2==2:
                    summ=j
                h2+=1
                print(j)
            file_writer.writerow({
                'From_Date':current_time,
                'To_Date':future_time,
                'Status' :status,
                'SMS_count' :count,
                'unit_count' :summ
                })
            print(count,summ)
        current_time=future_time
