import mysql.connector
import csv


listt=['smartive1','esitsindia1','olacabs1','incassabletechnologies1','cartheroleadassist','docsapp1','gojek4','whitehatjr','campk121','k21academy3','piggyride1','zerodha2','lidolearning','hooahapp1','aeriestechnology3','piggyride','Exotel','hiranandani1','oyorooms50','nextyn1','propertyshare2','uvihealth2','thehindu2','cs5f92','ubsforums1','culturealley1','probe','medibuddy3','designspace1','skilllync1','nestaway8','livspace8','yellowmessenger2','campk1212','crossbowlabs','ynotdesignmanufacturing1','elevatedirect2','hiranandani2','increff1','lidolearning9','portiqo','equitymaster1','greatlearning7','ipicert1','auw5c','carthero','enterprisebot1','vovinfotech']
conn=mysql.connector.connect(host='10.0.3.163', user='postern', password='spyonme', database='billix2 
my_cursor=conn.cursor()


for i in listt:
    query="select BillPlan from AccountBillPlan where SkuId ='call' and  AccountSid=\"{}\" order by FromTime desc limit 1".format(i)
    my_cursor.execute(query)
    idd=my_cursor.fetchall()
    # print(idd[0][0])
    try:
        query2="select Name, Description, Data from BillPlans where Id={}".format(idd[0][0])
        my_cursor.execute(query2)
        iddd=my_cursor.fetchall()
        if iddd[0][0]:
            print("yes")
        try:
            with open('Data.csv','a',newline='  as fr:
                csv_writer=csv.DictWriter(fr,fieldnames=['Sid','Name','Description','data'])
                # csv_writer.writeheader()
                try:
                    csv_writer.writerow({
                        'Sid' : i,
                        'Name':iddd[0][0],
                        'Description': iddd[0][1],
                        'data': iddd[0][2]

                    })
                except IndexError:
                    continue
        except IndexError:
            continue
    except IndexError:
        continue
