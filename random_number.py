from datetime import datetime
import random,csv
from traceback import print_tb
import All_Connection

hhh=0
with open("transactional_sms.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['Sub_Time','Sent_Time','Latency','Final_Status','SMSType'])
    file_writer.writeheader()
    for i in range(1,110):
        day=random.randint(1,30)
        hour=random.randint(1,23)
        minute=random.randint(1,60)
        second=random.randint(1,60)
        import mysql.connector
        conn=mysql.connector.connect(host='10.0.3.59', user='postern', password='spyonme', database='twilix 
        my_cursor=conn.cursor()
        date1="2022-01-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
        hour+=1
        date2="2022-01-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
        # print(date1)
        # print(date2)
        query="select Sid, DateSent ,  Status , _SmsType, _internal from SMSMessage where _SmsType='transactional' and DateCreated > '{}'  and DateCreated < '{}' limit 1000".format(date1,date2)
        print(query)
        my_cursor.execute(query)
        hh=my_cursor.fetchall()
    
        
        # file_writer.writeheader()
        for i in hh:
            # A1,A2,A3,A4,A5=0,0,0,0,0
            count=1
            for j in i:
                # print(j)
                if count==1:
                    A1=j.decode()
                if count==2:
                    A2=j
                if count==3:
                    A3=j.decode()
                if count==4:
                    A4=j.decode()
                if count==5:
                    A5=j.decode()
                count+=1
            # print(hhh)
            hhh+=1
            nn=str(A5).find("subTime")
            A6=str(A5)[nn+10:nn+29]
            nn2=str(A5).find("statUpdTime")
            A7=str(A5)[nn2+14:nn2+33]
            # print(A1,A2,A3,A4,A6)
            file_writer.writerow({
                'Sub_Time' :A6,
                'Sent_Time':A7,
                'Latency':A1,
                'Final_Status':A3,
                'SMSType':A4
            })
        print(hhh)
# [S    ub_Time','Sent_Time','Toatal_Calls','Final_Status','SMSType'])
 # for i in hh:
    #     count=0
    #     stat2_dict={}
    #     for j in i:
    #         name="A"+str(count)
    #         print(name)
    #         if str(type(j))=="<class 'bytearray'>":
    #             name=j.decode()
    #             stat2_dict[name]=j.decode()
    #         else :
    #             stat2_dict[name]=j
    #         print(type(name))
    #         count+=1
    # # print(listt2)


    # print(stat2_dict)
