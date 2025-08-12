import mysql.connector
import csv


listt=['3works1','abccorpjustatestaccount1','ekagga2','exotel535','graphy3','iteanz1','jadhavcompany1','leadschool4','leadsuneed1','mihuru2','neuraldaytechnologiesllp1','ohfound1','sharmastore1','shipmnts2','skygoal1','teamvariance1','xyz616']

conn=mysql.connector.connect(host='10.0.1.78', user='postern', password='spyonme', database='exotel 
my_cursor=conn.cursor()


for i in listt:
    query="select email, tenants.name from users join tenants on users.tenant_id=tenants.id  where is_admin=1 and tenant_id in(select id from tenants where name='{}  order by date_created limit 1".format(str(i))
    my_cursor.execute(query)
    idd=my_cursor.fetchall()
    print(idd, i)
    for j in idd:
        with open('hhh.csv','a',newline='  as fr:
            csv_writer=csv.DictWriter(fr,fieldnames=['Sid','Email'])
            # csv_writer.writeheader()
            csv_writer.writerow({
                'Sid' : i,
                'Email':j[0]
            })
         

    #                 })
    #             except IndexError:
    #                 continue
    #     except IndexError:
    #         continue
    # except IndexError:
    #     continue