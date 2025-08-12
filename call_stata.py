import uuid
import time
import json
import subprocess
import logging
import sys
import os
import re
import csv
import traceback
import shlex
import requests
import logging
import logging.config
import boto3
import requests
import json,csv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import ast
from datetime import datetime
from datetime import timedelta
import datetime as dtc
from collections import Counter
from dateutil.relativedelta import *
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import json, decimal
import pandas as pd

# def send_ses_email(details, AccountSid, sub, to, addBody=""):
#     sesClient = boto3.client('ses', region_name='us-east-1 
#     msg = MIMEMultipart()
#     msg['to'] = to
#     SENDER = "noreply@exotel.com"
#     name = to.split("@")[0].title()
#     msg.preamble = 'Multipart message.\n'
#     msg.set_charset("utf-8")
#     msg['Subject'] = sub
#     part = MIMEText(
#         "Hey " + name + " \n\n-- Here is the data that you've requested.\n\n" + str(addBody)+"\n\n")
#     msg.attach(part)
#     if os.path.isfile(details):
#         part = MIMEApplication(open(details, 'rb .read())
#         part.add_header('Content-Disposition', 'attachment',
#                         filename=details)
#         msg.attach(part)
#     result = sesClient.send_raw_email( Source=SENDER, Destinations=[msg['to']], RawMessage={'Data': msg.as_string()} )
#     return result

def getDates(date1, date2):
    date1 = datetime.strptime(str(date1), "%Y-%m-%d").date()
    date2 = datetime.strptime(str(date2), "%Y-%m-%d").date()
    delta = date2 - date1
    datelist = []
    for i in range(delta.days + 1):
        datelist.append(date1 + timedelta(days=i))
    return datelist

def getcallstats(account, fromdate, todate, user_id):
    try:
        if account == 'cloudfronts' or account == 'dummy' or account == 'eveningflavors' or account == 'exotel' or account == 'roopit' or account == 'zopnow':
            account = account.title()
        dateslist = getDates(fromdate, todate)
        outputFileName = account + "_" + fromdate + "_" + todate + ".csv"
        final_dict = dict()
        csvRow = ["AccountSid", "Date", "Direction", "Exophone","Status", "Count"]
        with open(account + "callstats" + fromdate + "_" + todate + ".csv", "w") as filewrite:
            wr = csv.writer(filewrite)
            wr.writerow(csvRow)
            username = user_id
            for dateto in dateslist:
                ind = dateto.strftime("%m%Y")
                client = Elasticsearch("http://es-inbox-2.internal.exotel.in:9200/")

                ins = Search(using=client, index="calls_"+ind+"") \
                    .filter('range' ,  **{'created': {'gte': "" + str(dateto) + "T00:00:00", 'lte': "" + str(dateto) + "T23:59:59"}}) \
                    .filter("term", tenant="" + account + "") \
                    .query('wildcard', direction='inbound 

                ins.aggs.bucket('leg2callerid', 'terms', field='vn', size=100000) \
                    .bucket('status', 'terms', field='dialCallStatus', size=100)

                outs = Search(using=client, index="calls_"+ind+"") \
                    .filter('range' ,  **{'created': {'gte': "" + str(dateto) + "T00:00:00", 'lte': "" + str(dateto) + "T23:59:59"}}) \
                    .filter("term", tenant="" + account + "") \
                    .query('wildcard', direction='out* 

                outs.aggs.bucket('leg2callerid', 'terms', field='vn', size=100000) \
                    .bucket('status', 'terms', field='dialCallStatus', size=100)

                inresponse = ins.execute()
                outresponse = outs.execute()
                fin_in = {}
                fin_out = {}
                for leg2CallerId in inresponse.aggregations.leg2callerid.buckets:
                    count = leg2CallerId.status.buckets
                    for i in range(len(count)):
                        fin_out.update({'date': str(dateto)})
                        fin_out.update({'direction': "inbound"})
                        fin_out.update({'tenant': str(account)})
                        fin_out.update({'l2c': leg2CallerId.key})
                        fin_out.update({'st': count[i]['key']})
                        fin_out.update({'co': count[i]['doc_count']})
                        wr.writerow([str(fin_out.get("tenant", "NULL")), str(fin_out.get("date", "NULL")), str(fin_out.get("direction", "NULL")), str(fin_out.get("l2c", "NULL")),str(fin_out.get("st", "NULL")), int(fin_out.get("co", "NULL"))])

                for leg2CallerId in outresponse.aggregations.leg2callerid.buckets:
                    count = leg2CallerId.status.buckets
                    for i in range(len(count)):
                        fin_out.update({'date': str(dateto)})
                        fin_out.update({'direction': "outbound"})
                        fin_out.update({'tenant': str(account)})
                        fin_out.update({'l2c': leg2CallerId.key})
                        fin_out.update({'st': count[i]['key']})
                        fin_out.update({'co': count[i]['doc_count']})
                        wr.writerow([str(fin_out.get("tenant", "NULL")), str(fin_out.get("date", "NULL")), str(fin_out.get("direction", "NULL")), str(fin_out.get("l2c", "NULL")),str(fin_out.get("st", "NULL")), int(fin_out.get("co", "NULL"))])
        df = pd.read_csv (account + "callstats" + fromdate + "_" + todate + ".csv")
        df = df.fillna('na 
        newf = df.pivot_table(index=['Date', 'Exophone','Direction'], columns='Status', values='Count',fill_value=0)
        col_list=['busy','canceled','completed','failed','no-answer','na']
        flattened = pd.DataFrame(newf.to_records())
        flattened.insert(0, 'AccountSid', account)
        flattened['Total'] = flattened[col_list].sum(axis=1)
        flattened.to_csv(outputFileName, index=False)
        
        mailsend = send_ses_email(outputFileName, account, "Call Stats For the Account " + account, username)
        if mailsend:
            print("Mail sent successfully for " + account + " " + fromdate)
            os.unlink(account + "callstats" + fromdate + "_" + todate + ".csv")
            os.unlink(outputFileName)

    except Exception as e:
        print (traceback.format_exc())

if __name__ == '__main__':
    #yesterday = datetime.now() - timedelta(1)
    #sdate = datetime.strftime(yesterday, '%Y-%m-%d 
    account = sys.argv[1]
    sdate = sys.argv[2]
    edate = sys.argv[3]
    email = sys.argv[4]
    getcallstats(account, sdate, edate, email)