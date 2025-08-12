import mysql.connector
from prettytable import from_db_cursor
import csv


conn=mysql.connector.connect(host='10.0.0.10', user='postern', password='spyonme', database='exotel 
my_cursor=conn.cursor()


def get_UserActivity(name,fromdate,enddate, userid):
    try:
        # oblxconn = get_obelix_conn()
        # oblxcur = oblxconn.cursor()
        if name:
            query1 = "select first_name, last_name, users.email as Email, value as Value, event_time as Time from users join user_activity on users.id=user_activity.user_id where user_activity.tenant_id in (select id from tenants where name in ('%s ) and event_time >='%s 00:00:00' and event_time<='%s 23:59:59'" % (name, fromdate, enddate)
            #logger.info("Query: "+get_user_q)
            # logger.info("Trying to Get User details for " +
            # name + " Request from " + userid)
            # res = get_results(oblxcur, get_user_q)
            my_cursor.execute(query1)
            res=my_cursor.fetchall()
            print(res)

            if res:
                emailid = userid
                subject = "UserActivity for the Account " + name
                body = "Please find the Below For the UserActivity for the Account " + name
                with open("" + name + "useractivity.csv", "w") as filewrite:
                    fileheaders = ['first_name','last_name','email','device','date']
                    print(fileheaders)
                    # logger.info(fileheaders)
                    writer = csv.DictWriter(filewrite, fileheaders)
                    writer.writeheader()
                    for i in res:
                        print(i)
                    # first_name=res
                    # last_name	
                    # Email	
                    # Value	
                    # Time
                        writer.writerows(res)
                # mailsend = send_ses_email(
                #     "" + name + "useractivity.csv", "Exotel", subject, emailid)
                # if mailsend:
                #     os.unlink(name + "useractivity.csv")
                #     logger.info("useractivity for " +
                #             name + " sent to " + emailid)
                # return "`Data sent to your email... Please check your email (Spam folder too)` :relieved: :relieved: "
            else:
                return "Warning: Data not available :cry: "
    except Exception as e:
        print("hh")
        # logger.error(e)
        #send_email(str(e), "There was an error while taking the action.. Please fix it you deadbeat",
                #"[ExoBot] [Very Important] Exeception at get_userdetails_account", "techsupport@exotel.in")
        # print(traceback.format_exc())

get_UserActivity("exotel905","2022-11-01","2022-11-31","h")
