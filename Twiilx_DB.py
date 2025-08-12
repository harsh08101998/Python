import mysql.connector
from prettytable import from_db_cursor

# con=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
con=mysql.connector.connect(host='10.1.2.202', user='postern', password='spyonme', database='twilix',ssl_disabled=True)

my_cursor=con.cursor()


#query="select count(value), value from numbers  where user_id in (select id from users where last_login >= '2021-07-01 00:00:00' )group by value having count(value)>1 "
# query="select id, AccountSid, DltTemplateId from SmsTemplate where AccountSid='minsure1'"
# query="select id,AccountSid from AvailablePhoneNumber limit 5000"
query="select * from Server where code='079_18'"
query="select * from Pri where card in (select id from Card where server in (select id from Server where code ='079_18')) order by span"

my_cursor.execute(query)
# print(my_cursor.fetchmany())
mytable = from_db_cursor(my_cursor)
print(mytable)

con.commit()
con.close()