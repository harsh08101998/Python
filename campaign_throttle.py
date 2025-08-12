import mysql.connector
import os,csv,json
import sys
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
from sys import maxsize
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


conn3=mysql.connector.connect(host='10.0.128.26', user='campaignix', password='cell4business', database='campaignix 
my_cursor3=conn3.cursor()
      
# query="select * from accounts where sid='exotel90'"

def campaign_throttle(task,accountSid, new_limit, approvedBy, userid):
    print("task is :- ", task)
    print("accountSid is :- ", accountSid)
    print("new_limit is :- ", new_limit)
    print("approvedBy is :- ", approvedBy)
    print("userid is :- ", userid)
    try:
        user = userid
        if user =='karthikeyan@exotel.in' or user =='sharanya@exotel.in' or user =='sachith@exotel.in' or user =='varun@exotel.in' or user =='apoorv@exotel.in' or user =='harikrishnan.kumar@exotel.in' or user =='saquib@exotel.in' or user =='bhavna.gupta@exotel.in' or user =='praneeth.alikonda@exotel.in' or user =='ankush@exotel.in' or user =='saurabh.sharma@exotel.in' or user =='aizadh.ateebh@exotel.in' or user =='sarthak@exotel.in' or user =='sravya@exotel.in' or user =='vimmey@exotel.in' or user =='karthikeyan.g@exotel.in' or user =='ashwin.ts@exotel.in' or user =='harsh.kumar@exotel.in' or user=='kanupriya.singh@exotel.in' or user=='rishi.ranjan@exotel.in' or user=='aditi.s@exotel.in' or user=='mokshith.reddy@exotel.in' or user=='aman.raj@exotel.in' or user=='toshitha.royan@exotel.in':
            if accountSid == 'Exotel' or accountSid == 'dummy' or accountSid == 'eveningflavors' or accountSid == 'exotel' or accountSid == 'roopit' or accountSid == 'zopnow':
                accountSid = accountSid.title()
            if task =='post':
                approvedBy = approvedBy
                # logger.info(approvedBy)
            # CheckAccount = checkvalidAccountSid(accountSid)
            # if not CheckAccount:
                # logger.info("[exobot]: Incorrect Account")
                # return "Wrong AccountSid. Kindly check again"
            if not task in ('get','post :
                # logger.info("[exobot]: Inorrect Task")
                return "You can only perform two actions. get - to get details of a throttle, and post: to change the value of the throttle"
            # if not feature in ('campaign :
            #     logger.info("[exobot]: Incorrect Feature")
                # return "Features supported by this command is campaign only"
            if not task in ('post' ,'get :
                # logger.info("[exobot]: Correct Method")
                return "The method can only be get and post"
            if task =='get':
                query="select * from accounts where sid='{}'".format(accountSid)
                # logger.info(query)
                my_cursor3.execute(query)
                data=my_cursor3.fetchall()
                return data
                # return "The relavant response will be sent to you on you mail"
            if task =='post':
                # query="select * from accounts where sid='{}'".format(accountSid)
                query="update accounts set call_capacity={} where sid='{}'".format(int(new_limit),accountSid)
                print(query)
                # logger.info(query)
                # my_cursor3.execute(query)
                # data=my_cursor3.fetchall()
                # return data
                # return "The relavant response will be sent to you on you mail"
        else:
            return "You do not have access to run this command. Kindly get in touch with TS to get the required access"
    except Exception as e:
        print(e)
        # logger.error(e)

# print(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
main_data=campaign_throttle(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
print(main_data)
print(main_data[0][0])
# if sys.argv[1]=='get':
#     campaign_throttle('get',sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

# def campaign_throttle(task,accountSid, new_limit, approvedBy, userid):

# get,exotel905,nill,nil,harsh.kumar@exotel.in
# update,exotel905,250,harsh.kumar+1@extel.in,harsh.kuarm@exotel.in


# my_cursor3.execute(query)
# data=my_cursor3.fetchall()
# print(data)   
# def campaign(accountSid, throttle):
#     try:        
#         campaignconn = get_campaignix_conn()
#             campaigncur = campaignconn.cursor()
#         query = query + " update accounts set call_capacity='"+throttle+"' where sid='"+accountSid+"';".format( accountSid=accountSid, throttle=throttle)
#         query = query + " commit;"
#         campaigncur.execute(query)
#         campaigncur.close()
#         res = get_results(campaigncursor, query)