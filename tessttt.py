import imp
import mysql.connector
from prettytable import from_db_cursor
import csv

def Twilix_Small_Table(query1,*argv):
    conn=mysql.connector.connect(host='10.0.3.163', user='postern', password='spyonme', database='billix2 
    my_cursor=conn.cursor()
    my_cursor.execute(query1)
    for i in argv:
        if i=='Table' or i=='table':
            data=from_db_cursor(my_cursor)
            return data
        elif i=='csv' or i=='CSV':
            file_name=argv[1]
            row_name=my_cursor.description
            listt=[]
            for i in row_name:
                listt.append(i[0])
            with open(file_name, 'w', newline="") as fopen:
                csvwrite=csv.DictWriter(fopen,fieldnames=listt)
                csvwrite.writeheader()
                hh=my_cursor.fetchall()
                for i in hh:
                    listt2=[]
                    for j in i:
                        if str(type(j))=="<class 'bytearray'>":
                            listt2.append(j.decode())
                        else:
                            listt2.append(j)
                    count=0
                    try:
                        dict={}
                        for i in listt:
                            dict[i]=listt2[count]
                            count+=1
                        csvwrite.writerow(dict)
                    except IndexError:
                       continue
            return "File created"
        else:
            data2=my_cursor.fetchall()
            return data2