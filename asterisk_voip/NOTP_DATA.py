import csv
import mysql.connector
from csv import DictWriter
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

####################### Data Base connection #################################
conn=mysql.connector.connect(host='10.0.2.49', user='postern', password='spyonme',database='notp 
my_cursor=conn.cursor()
query="select account_sid, count(*), status from flash_calls where created_at>='{} 00:00:00' and created_at<='{} 23:59:59' group by account_sid, status".format(startdate,lastdate)
my_cursor.execute(query)
notp_data=my_cursor.fetchall()
print(query)
print(notp_data)
