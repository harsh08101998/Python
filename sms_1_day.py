import datetime,csv, time
import mysql.connector
from datetime import date, timedelta
# Get current time in local timezone
with open("flipkarthealthplus1_1_hours_without_price.csv", 'w',newline="") as fw:
    # file_writer=csv.DictWriter(fw,fieldnames=['Units','Price','Status'])
    file_writer=csv.DictWriter(fw,fieldnames=['FromTime','ToTime','Units','sms_count'])

    file_writer.writeheader()
    # current_time = datetime.datetime(2022, 8, 1, 0, 0, 0)
    # h=0
    conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
    my_cursor=conn.cursor()
    
    listt=['apna53']
    for sidd in listt :
        current_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
        n=1
        for i in range(0,744):
            if i%50==0:
                conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
                my_cursor=conn.cursor()

            # n = 1
            future_time = current_time + timedelta(hours=n)
            print(current_time, future_time)
            query="select sum(_NumUnits), count(*) from SMSMessage where AccountSid='flipkarthealthplus1' and  DateCreated > '{}' and DateCreated <= '{}' ".format(current_time,future_time)
            # query="select _NumUnits, Price, Status from SMSMessage where AccountSid='flipkarthealthplus1' and  DateCreated > '{}' and DateCreated < '{}' ".format(current_time,future_time)
           
            # print(query)
            # query="select _NumUnits, Price, Status from SMSMessage where AccountSid='flipkarthealthplus3' and  DateCreated > '2023-01-01 00:00:00' and DateCreated < '2023-01-02 07:00:00' "
            my_cursor.execute(query)
            kk=my_cursor.fetchall()
            for i in kk:
            # print(kk)
                data=kk[0]
            # print(data)

            # for i in kk:
            #     h2=0
            #     for j in i:
            #         if h2==0:
            #             Price=j.decode()
            #         if h2==1:
            #             count=j

            # n+=1
            file_writer.writerow({
                'FromTime':current_time,
                'ToTime':future_time,
                'Units':data[0],
                # 'Price' :data[1],
                'sms_count':data[1]

                })
            


            current_time=future_time
