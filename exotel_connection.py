import All_Connection
import All_Connection_MUM
import sys


# users=[384180,384829,384835]
# for i in users:

#     query="select * from user_activity where tenant_id=186470 and user_id={} order by event_time desc limit 1".format(i)
#     hh=All_Connection.Obelix_Small_Table(query, 'table','ayu5d1_template_backup.csv 
#     print(hh)

request_type=sys.argv[1]
conn_type=sys.argv[2]
print(request_type,conn_type)
query="select * from users where email='chetana.kotian+1@eurekaforbes.com'"

with open('Old_commands.txt', 'a  as f:
    f.write(query)
    f.write('\n\n 

if conn_type == 'obe':
    hh=All_Connection.Obelix_Small_Table(query,str(request_type),'netgen1_info.csv 
    print(hh)






# hh=All_Connection.Obelix_Small_Table(query, 'table','netgen1_info.csv 

# # hh=All_Connection_MUM.Obelix_Small_Table(query,'csv','mum_.csv 

# print(hh)


