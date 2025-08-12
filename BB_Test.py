from PyMess import *
from sql_utils import *
from general_utils import *
from datetime import datetime
from tabulate import tabulate
import uuid
import time
import simplejson
import subprocess
import logging
import sys
import os
from os.path import exists
import re
import csv
import traceback
import shlex
import requests
import logging
import logging.config
from elasticsearch import Elasticsearch
import ast
from datetime import datetime as dt
from datetime import timedelta
import datetime as dtc
import config as cfg
from collections import Counter
from dateutil.relativedelta import *
import json, decimal

def getDowntimeClients(data, userid):
    try:
        print(data, userid)
        twxconn = get_twilix_conn()
        twxcur = twxconn.cursor()
        #logger.info(data)
        region = data[0].upper()
        operator = data[1].title()
        numbertype = data[2].title()

        if numbertype == 'Tollfree':
            numbertype = 'TollFree'

        clients = []
        username = userid

        file1 = uuid.uuid4().hex+".csv"
        print(file1)
        targetFile = open(file1, 'w 
        #wr = csv.writer(targetFile, delimiter=',', lineterminator='\n 
        wr = csv.writer(targetFile)

        if(len(data)>3):
            pilot=data[3].title()
            print(len(data))
        
        print(pilot)

        if data:
            if(len(data)>3 and (numbertype == "Mobile" or numbertype == "Tollfree")):
                clients_query = "select distinct AccountSid from AvailablePhoneNumber where NumberType='%s' and Rental>=0 and AccountSid IN (select sid from Account where Type='Full' and Status='active  and _divert in (select id from AvailablePhoneNumber where Region='%s' and Operator in (select id from Operator where name='%s  and  _Pri in(select id from Pri where pilot='%s ) order by AccountSid" % (numbertype, region, operator,pilot)

            if(len(data)>3 and (numbertype =="Landline")):
                clients_query = "select distinct AccountSid from AvailablePhoneNumber where NumberType='%s' and Rental>0 AND Region='%s'and AccountSid IN (select sid from Account where Type='Full' and Status='active  and Operator in (select id from Operator where name='%s  and _Pri in(select id from Pri where pilot='%s  order by AccountSid" % (numbertype, region, operator,pilot)

            elif (numbertype == "Mobile" or numbertype == "Tollfree"):
                clients_query = "select distinct AccountSid from AvailablePhoneNumber where NumberType='%s' and AccountSid IS NOT NULL and Rental>=0 and AccountSid IN (select sid from Account where Type='Full' and Status='active  and _divert in (select id from AvailablePhoneNumber where Region='%s' and Operator in (select id from Operator where name='%s ) order by AccountSid" % (numbertype, region, operator)
            else:
                clients_query = "SELECT DISTINCT AccountSid FROM AvailablePhoneNumber WHERE AccountSid IS NOT NULL AND Region='%s' AND Operator IN (select id from Operator where name = '%s  AND NumberType='%s' AND Rental>0 AND AccountSid IN (SELECT Sid FROM Account WHERE Type='Full' and Status='active  and _state!= 'pn' ORDER BY AccountSid" % (region, operator, numbertype)
            print(clients_query)
            res = get_results(twxcur, clients_query)
            # print (res)
            if res:
                for x in range(len(res)):
                    sid = []
                    sid.append(res[x]['AccountSid'])
                    wr.writerows([sid])
            targetFile.close()
            if(len(data)==4):
                subject= "Downtime clients - "+region+ " " +operator +" "+pilot
            else:
                subject= "Downtime clients - "+region+ " " +operator+" "+numbertype
                return "`Since the Data size is very high its been sent to your email. Please check your email (Spam too)` :relieved:  :relieved:"
        else:
            return "Empty result. No tenant found"
    except Exception as e:
        print("Error")


def is_valid_request(text, userid):
    if text != '':
        texter = shlex.split(text)
        if texter[0] == 'downtimeclients':
                if len(texter) == 5 or len(texter) == 4:
                    #region = regionChecker(texter[1]);
                    #operator = operatorChecker(texter[2]);
                    region = texter[1]
                    operator = texter[2]
                    #logger.info(texter)
                    numberType = (texter[3] == 'Mobile' or texter[3] == 'Landline' or texter[3] == 'TollFree ;
                    if region and operator and numberType:
                        return getDowntimeClients(texter[1:], userid);
                    else:
                        return "`Sorry!! Parameters mentioned are not correct`  :expressionless: :expressionless: "
                # elif len(texter) == 4:
                #     userid = texter[1]
                #     if (texter[2] == 'all  and (texter[3] == 'indian' or texter[3] == 'international :
                #         return getAllClients(texter, userid);
                #     else:
                #         return "`Sorry!! Parameters mentioned are not correct` :expressionless: :expressionless: "
                # else:
                #     if len(texter) > 4:
                #         return "`Sorry!! I can't accept more than required params sirji` :expressionless: :expressionless: "
                #     elif len(texter) < 3:
                #         return "`Sorry!! Very few arguments` :expressionless: :expressionless:"
                else:
                    print("Wrong Parameter")


text='downtimeclients AP TATA Landline 04069160000'
userid='harsh.kumar@exotel.in'
is_valid_request(text, userid)
