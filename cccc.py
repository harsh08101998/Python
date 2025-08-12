import mysql.connector

conn3=mysql.connector.connect(host='10.0.128.26', user='postern', password='spyonme', database='campaignix 
my_cursor3=conn3.cursor()

query="select date_created, campaign_sid,call_schedule.from as Exophone, number,attempt from call_schedule where account_sid='hindustantimes3'  and date_created >='2021-10-05 00:00:00' and date_created <= '2021-10-08 00:00:00' limit 5"
my_cursor3.execute(query)
data=my_cursor3.fetchall()
print(data)