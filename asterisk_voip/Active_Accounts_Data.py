import All_Connection
import All_Connection_MUM
import mysql.connector


## Twilix connection 
conn=mysql.connector.connect(host='10.0.0.65', user='postern', password='spyonme', database='twilix 
my_cursor=conn.cursor()

### For getting Twilix_closed_2022_new.csv   from Twilix small table ###########
query="select AccountSid, Description, DateCreated from AuditLog where Description in  ('{\"old\": \"active\", \"new\": \"closed\"}','{\"old\": \"suspended\", \"new\": \"active\"}', '{\"old\": \"active\", \"new\": \"suspended\"}','{\"old\": \"closed\", \"new\": \"active\"}','{\"old\": \"suspended\", \"new\": \"closed\"}  and Type='AccountStatusUpdate'"
## For gettging Twilix_Live_2022.csv  from Twilix small table #############
query1="select AccountSid, DateCreated from AuditLog where Description= '{\"old\": \"Trial\", \"new\": \"Full\"}' and Type='AccountTypeUpdate' "
## For getting data_2022.csv  from Twilix small table ##############
query2="select Sid, Status, Type, BillingType, KycStatus from Account where Type='Full'"

## For getting Live_date_2022.csv from Execution machine SQL  ##########
query3 ="select AccountSid , LiveDate , ChurnDate from accountdetails"
## For getting Currency_2022.csv  from Billix DB ########
query4="select AccountSid , Value  from Settings where Name='billing_currency' "
## For getting Balance.csv from Billix
query5="select AccountSid, Balance , CouponBalance , CreditLimit , UnBilledBalance from AccountBalance"

## Getting list of all Accounts from Twilix
query6="select Sid from Account where Type='Full'"
my_cursor.execute(query6)
hh=my_cursor.fetchall()
account_list=[]
for i in hh:
    for j in i:
        account_list.append(j.decode())
main_list=tuple(account_list)

## For getting paid_2022.csv from billix ##
query7="select distinct(AccountSid) from BillEvents where SkuId='payment' and AccountSid in {} and Amount >0".format(main_list)

hh=All_Connection.Twilix_Small_Table(query, 'csv','Twilix_closed_2022_new.csv 
print(hh)
hh=All_Connection.Twilix_Small_Table(query1, 'csv','Twilix_Live_2022.csv 
print(hh)
hh=All_Connection.Twilix_Small_Table(query2, 'csv','data_2022.csv 
print(hh)
hh=All_Connection.exe_mqchine(query3, 'csv','Live_date_2022.csv 
print(hh)
hh=All_Connection.Billix_Master_Table(query4, 'csv','Currency_2022.csv 
print(hh)
hh=All_Connection.Billix_Master_Table(query5, 'csv','Balance.csv 
print(hh)
hh=All_Connection.Billix_Master_Table(query7, 'csv','paid_2022.csv 
print(hh)