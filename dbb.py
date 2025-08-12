import mysql.connector
from prettytable import from_db_cursor

conn=mysql.connector.connect(host='10.1.1.94', user='postern', password='spyonme', database='metrics 
my_cursor=conn.cursor()
query1="select AccountSid , LiveDate , ChurnDate from accountdetails"
my_cursor.execute(query1)
data=from_db_cursor(my_cursor)
print(data)