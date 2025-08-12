import mysql.connector
import requests,json, csv
from dateutil.relativedelta import relativedelta
from datetime import date
import sys

def dnd_check(callsid) :

    ############################# Time selection ###############################################

    todays_date = date.today()

    current= "calls_" + str(todays_date.strftime('%m')) + str(todays_date.year)
    last_month = date.today() + relativedelta(months=-1)
    _last_month= "calls_" + str(last_month.strftime('%m')) + str(last_month.year)
    last_month_2= date.today() + relativedelta(months=-2)
    _last_month_2= "calls_" + str(last_month_2.strftime('%m')) + str(last_month_2.year)
    last_month_3 = date.today() + relativedelta(months=-3)
    _last_month_3= "calls_" + str(last_month_3.strftime('%m')) + str(last_month_3.year)
    last_month_4 = date.today() + relativedelta(months=-4)
    _last_month_4= "calls_" + str(last_month_4.strftime('%m')) + str(last_month_4.year)
    last_month_5 = date.today() + relativedelta(months=-5)
    _last_month_5= "calls_" + str(last_month_5.strftime('%m')) + str(last_month_5.year)

    last_six_months=str(current) + "," + str(_last_month) + "," + str(_last_month_2) + "," + str(_last_month_3) + "," + str(_last_month_4) + "," + str(_last_month_5)

    ###########################################################################

    es_query={"query":{"bool":{"must":[{"term":{"sid":{"value":str(callsid)}}}]}}}
    avg_query1 = json.dumps(es_query)
    requestt='http://es-inbox-2.internal.exotel.in:9200/{}/call/_search?pretty&size=100000'.format(last_six_months)
    avg_resp = requests.post(requestt, data=avg_query1)
    print(avg_resp.text)

    # connection=mysql.connector.connect(host='10.0.0.65',user='postern',password='spyonme',database='twilix 
    # my_cursor=connection.cursor()

    # number=str(numbers)
    # query="select PhoneNumber, AccountSid from AvailablePhoneNumber where PhoneNumber='{}'".format(number)
    # my_cursor.execute(query)
    # data=my_cursor.fetchall()
    # if data:
    #     print(data)
    # else :
    #     print("Number not related to any account")



    # count=0
    # csv_name=str(number)+"_calls.csv"
    # with open(csv_name, 'w',newline="") as fw:
    #     file_writer=csv.DictWriter(fw,fieldnames=["tenant","sid","vn","to","from","status","created","start_time","l2d","duration"])
    #     file_writer.writeheader()
    #     # avg_query={"query":{"bool":{"must":[{"wildcard":{"to":"079885322770*"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
    #     es_query={"query":{"bool":{"must":[{"term":{"to":{"value":str(number)}}}]}}}
    #     avg_query1 = json.dumps(es_query)
    #     print(avg_query1)
    #     requestt='http://es-inbox-2.internal.exotel.in:9200/{}/call/_search?pretty&size=100000'.format(last_six_months)
    #     print(requestt)
    #     avg_resp = requests.post(requestt, data=avg_query1)
    #     print(avg_resp)
    #     hits=avg_resp.json()['hits']
    #     source=hits['hits'] 
    #     for i in source:
    #         main_data=i['_source']
    #         sid=main_data['sid']
    #         tenant=main_data['tenant']
    #         to=main_data['to']
    #         from1=main_data['from']
    #         vn=main_data['vn']
    #         status=main_data['status']
    #         primary_status=main_data['created']
    #         start_tim=main_data['start_time']
    #         l2d=main_data['l2d']
    #         duration=main_data['duration']
    #         file_writer.writerow({
    #             'sid' : sid,
    #             'tenant' : tenant,
    #             'to' : to,
    #             'from':from1,
    #             'vn':vn,
    #             'status' : status,
    #             'created':primary_status,
    #             'start_time':start_tim,
    #             'l2d':l2d,
    #             'duration':duration

    #         })
    #         count+=1

    # if count==0:
    #     print("No call found")
    # else:
    #     print("Total Call count is : ", count)


dnd_check(sys.argv[1])
