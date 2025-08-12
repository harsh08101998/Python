import requests, mysql.connector
import json,csv, time

listt=['72networks1m','Exotel','accenture1m','adityabirlacapital1m','adityabirlacapital23m','adityabirlacapital2m','adityabirlacapital48m','adlbsolutions1m','agrostar1m','ameyo1m','ameyo2m','ameyo3m','angelbroking1m','anveya1m','armman1m','avanienterprises1m','avivaindia1m','avivainfo1m','avsar1m','bajajallianz2m','bajajallianz3m','bajajallianz4m','bajajallianz7m','bharatpe2m','blah51m','cams510m','cams511m','cams512m','cams514m','cams517m','cams52m','cams54m','cams55m','cams59m','cams61m','cams62m','camslnt1m','camsonline2m','camsonline3m','camssbi1m','cardsplay','cattleyatechnosys1m','ccplexopoc1m','chingari1m','coindcx1m','connectionsdirect1m','conneqtbusinessservices1m','conneqtbusinesssolutions1m','conneqtbusinesssolutions2m','creditonepayments1m','default','dharmalife1m','donnotcall1','donotcall1','donotcall24','donotcall26','donotcall50','donotcall59','donotcall60','donotcall68','donotcall69','donotcall70','donotcall71','donotcall72','donotcall77','donotcall78','exo5c1b','exotel20','exotel29','exotel2m','exotel30m','exotel31m','exotel32','exotel42m','exotel46m','exotel49','exotel4m','exotel51','exotel57m','exotelbugtestmum1m','exotelbugtestmumtele1m','exoteldonotcall3m','exoteltechcom1m','exotest1m','findeed1m','fyers1m','getvymo1m','gichf1m','gmoney1m','gocollab','goconatus1m','greenlightplanet1m','hdfc51m','hdfcbank10m','hdfcbank3m','hdfcbank4m','hdfcsec1m','healthylife1m','hssupplychain1m','icanpe1m','icicibank100m','icicibank104m','icicibank144m','icicibank145m','icicibank146m','icicibank147m','icicibank1m','icicibank26m','icicibank2m','icicibank38m','icicibank40m','icicibank99m','icicisecurities1m','idfcfirstbank10m','idfcfirstbank1m','indianmoney1m','infosys1m','inthreeaccess1m','kotak3m','kotak4m','lnfinvest1m','mahindra1m','midlandmicrofin1m','muthoot1m','myspotlight1m','navi51m','navi61m','nexusi1m','nirmalbang1m','pennco1m','penncoenterprises1m','raushankumar7','raushankumar8','raushankumar9','rblbank1m','rblbank2m','rblbank3m','rblfinserve1m','relianceada1m','revolutionarynutrition1m','rlexotest1m','rpggroup1m','rpggroup2m','satsureanalyticsindia1m','sgagtech1m','skit61m','suportbackup1m','tcs5f1m','tcs601m','tcs611m','teamvedika1m','testexotel','thecadre1m','timesinternet1m','toyotaconnected1m','truecaller1m','truesoftwarescandinaviaab1m','ts6091m','unicef1m','urjamoney1m','uwbengaluru1m','velocity1m','vengage1m','vishienterprises1m','visionaryskincare1m']



# '10.0.3.163','postern', 'spyonme', 'billix2'
conn3=mysql.connector.connect(host='10.1.2.6', user='postern', password='spyonme', database='billix2 
my_cursor3=conn3.cursor()
count=1
with open("Feb_MUM_SMS_Count.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['AccountSid','Call_Count'])
    file_writer.writeheader()
    for hk in listt:
        accountsid=hk
        query="select AccountSid, sum(Quantity) from AggregateUsage where  AccountSid ='{}' and SkuId ='sms' and FromTime between '2022-02-01 00:00:00' and '2022-02-28 23:59:59' ".format(str(hk))
        my_cursor3.execute(query)
        data2=my_cursor3.fetchall()
        for i in data2:
            # print(i)
            accountsid=i[0]
            count=i[1]
            # duration=i[2]
            print(hk, count)
        
        file_writer.writerow({
            'AccountSid' : str(hk),
            'Call_Count' : count,
            # 'Duration' :duration

        })
        # count+=1
        # if count%200==0:
        #     time.sleep(2)
        # if count%2000==0:
        #     conn3.close()
        #     conn3=mysql.connector.connect(host='10.0.3.163', user='postern', password='spyonme', database='billix2 
        #     my_cursor3=conn3.cursor()

