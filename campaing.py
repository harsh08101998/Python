import mysql.connector
import os
import csv
from datetime import date, timedelta

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

conn2=mysql.connector.connect(host='10.0.0.10', user='postern', password='spyonme', database='exotel 
my_cursor2=conn2.cursor()
query3=" select a.name,a.id,count(b.tenant_id) from tenants a , campaigns b where scheduled BETWEEN '{} 00:00:00' AND '{} 23:59:59' AND a.id = b.tenant_id GROUP BY b.tenant_id".format(startdate,lastdate)
my_cursor2.execute(query3)
data3=my_cursor2.fetchall()
with open("Campaign_Dashboard_Data.csv",'w', newline='  as cdd:
    file_writer=csv.DictWriter(cdd,fieldnames=['Tenant_Name','Tenant_ID','Campaign_Count'])
    file_writer.writeheader()
    for i in data3:
        first,second,third=i[0],i[1],i[2]
        file_writer.writerow({
            'Tenant_Name':first,
            'Tenant_ID' : second,
            'Campaign_Count':third
        })

query4="select  distinct id from exotel.campaigns where scheduled BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(startdate,lastdate)
my_cursor2.execute(query4)
data4=my_cursor2.fetchall()
data5=[]
for i in data4:
    for j in i:
        data5.append(j)
main_list=tuple(data5)

conn2.close()
conn=mysql.connector.connect(host='10.0.3.97', user='postern', password='spyonme', database='exotel 
my_cursor=conn.cursor()
                        # ll=[]
                        # with open('campaings.csv', 'r  as f:
                        #     file_reader=csv.DictReader(f)
                        #     for i in file_reader:
                        #         ll.append(i['id'])
                        # lll=tuple(ll)
query="select tenant,count(id) from outbound_queue where campaign_id in{} group by tenant".format(main_list)
query2="select tenant,count(id)  from outbound_queue where campaign_id in{} and status='success' group by tenant".format(main_list)
my_cursor.execute(query)
data=my_cursor.fetchall()

with open("Total_Call_Happened.csv", 'w', newline='  as tch:
    file_writer=csv.DictWriter(tch, fieldnames=['Tenant_ID','Total_Call'])
    file_writer.writeheader()
    for i in data:
        first,second=i[0],i[1]
        file_writer.writerow({
            'Tenant_ID':first,
            'Total_Call':second
        })


my_cursor.execute(query2)
data2=my_cursor.fetchall()
with open("Total_Completed_Calls.csv", 'w', newline='  as tch:
    file_writer=csv.DictWriter(tch, fieldnames=['Tenant_ID','Completed_Calls'])
    file_writer.writeheader()
    for i in data2:
        first,second=i[0],i[1]
        file_writer.writerow({
            'Tenant_ID':first,
            'Completed_Calls':second
        })
conn.close()
