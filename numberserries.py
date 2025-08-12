import mysql.connector

listt=[]
conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()
# query="select Id,PhoneNumber, Region,Operator, AccountSid, Rental, _ReservedFor, _state, NumberType from  AvailablePhoneNumber where AccountSid is NULL and _ReservedFor is NULL and Rental>0 and NumberType='Landline' order by PhoneNumber "
# query="select PhoneNumber from  AvailablePhoneNumber where AccountSid is NULL and _ReservedFor is NULL and Rental>0 and NumberType='Landline' and IsoCountry='IN' order by PhoneNumber"
query="select  PhoneNumber from AvailablePhoneNumber where AccountSid is NULL and _ReservedFor is NULL and Operator=3 and Region='DL' and Rental>0 and NumberType='Landline' and _state='available' and _Pri in (select id from Pri where pilot=1141168200) limit 500"

my_cursor.execute(query)
number=my_cursor.fetchall()
# vn=(my_cursor.fetchall()[0])[0].decode()
for i in number:
    nn="+91"+str(int(i[0].decode()))
    listt.append(nn)

print(listt)



