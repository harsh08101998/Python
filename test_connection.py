import mysql.connector
# for MUM freshdesk - conn=mysql.connector.connect(host='10.1.220.27', user='root', password='Exotel@123', database='Exotel 
#conn=mysql.connector.connect(host='10.1.2.29', user='root', password='cell4Business 
conn=mysql.connector.connect(host='10.0.128.20', user='root', password='cell4business    # campaignix
#conn=mysql.connector.connect(host='', user='root', password=' 
#conn=mysql.connector.connect(host='', user='root', password=' 
#conn=mysql.connector.connect(host='', user='root', password=' 

my_curosr=conn.cursor()

query="show databases"
print(my_curosr.execute(query))