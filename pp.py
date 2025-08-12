import requests
import json,csv

listt=['72networks1m','Exotel','accenture1m','adityabirlacapital1m','adityabirlacapital23m','adityabirlacapital2m','adityabirlacapital48m','adlbsolutions1m','agrostar1m','ameyo1m','ameyo2m','ameyo3m','angelbroking1m','anveya1m','armman1m','avanienterprises1m','avivaindia1m','avivainfo1m','avsar1m','bajajallianz2m','bajajallianz3m','bajajallianz4m','bajajallianz7m','bharatpe2m','blah51m','cams510m','cams511m','cams512m','cams514m','cams517m','cams52m','cams54m','cams55m','cams59m','cams61m','cams62m','camslnt1m','camsonline2m','camsonline3m','camssbi1m','cardsplay','cattleyatechnosys1m','ccplexopoc1m','chingari1m','coindcx1m','connectionsdirect1m','conneqtbusinessservices1m','conneqtbusinesssolutions1m','conneqtbusinesssolutions2m','creditonepayments1m','default','dharmalife1m','donnotcall1','donotcall1','donotcall24','donotcall26','donotcall50','donotcall59','donotcall60','donotcall68','donotcall69','donotcall70','donotcall71','donotcall72','donotcall77','donotcall78','exo5c1b','exotel20','exotel29','exotel2m','exotel30m','exotel31m','exotel32','exotel42m','exotel46m','exotel49','exotel4m','exotel51','exotel57m','exotelbugtestmum1m','exotelbugtestmumtele1m','exoteldonotcall3m','exoteltechcom1m','exotest1m','findeed1m','fyers1m','getvymo1m','gichf1m','gmoney1m','gocollab','goconatus1m','greenlightplanet1m','hdfc51m','hdfcbank10m','hdfcbank3m','hdfcbank4m','hdfcsec1m','healthylife1m','hssupplychain1m','icanpe1m','icicibank100m','icicibank104m','icicibank144m','icicibank145m','icicibank146m','icicibank147m','icicibank1m','icicibank26m','icicibank2m','icicibank38m','icicibank40m','icicibank99m','icicisecurities1m','idfcfirstbank10m','idfcfirstbank1m','indianmoney1m','infosys1m','inthreeaccess1m','kotak3m','kotak4m','lnfinvest1m','mahindra1m','midlandmicrofin1m','muthoot1m','myspotlight1m','navi51m','navi61m','nexusi1m','nirmalbang1m','pennco1m','penncoenterprises1m','raushankumar7','raushankumar8','raushankumar9','rblbank1m','rblbank2m','rblbank3m','rblfinserve1m','relianceada1m','revolutionarynutrition1m','rlexotest1m','rpggroup1m','rpggroup2m','satsureanalyticsindia1m','sgagtech1m','skit61m','suportbackup1m','tcs5f1m','tcs601m','tcs611m','teamvedika1m','testexotel','thecadre1m','timesinternet1m','toyotaconnected1m','truecaller1m','truesoftwarescandinaviaab1m','ts6091m','unicef1m','urjamoney1m','uwbengaluru1m','velocity1m','vengage1m','vishienterprises1m','visionaryskincare1m']

params = (
    ('pretty', ' ,
    ('search_type', 'count 
)


with open("Feb_MUM_Calls_Count_and_Duration.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['AccountSid','Call_Count','Avg_Duration'])
    file_writer.writeheader()
    for i in listt:
        # count_query={"query":{"bool":{"must":[{"term":{"tenant":{"value":str(i)}}}]}}}
        avg_query={"query":{"bool":{"must":[{"term":{"tenant":{"value":str(i)}}}]}},"aggs": {"avg_grade": { "avg": { "field": "duration"}}}}
        # count_query1=json.dumps(count_query)
        avg_query1 = json.dumps(avg_query)
        # print(count_query1)
        print(avg_query1)
        avg_resp = requests.post('"http://es-inbox.internal.mum1.exotel.in:9200/calls_022022/call/_search?pretty&search_type=count', params=params, data=avg_query1)
  
        hits=avg_resp.json()['hits']
        count_calls=hits['total']
        print(count_calls)
############################# For Aggregation usage
        hits=avg_resp.json()['aggregations']
        count=hits['avg_grade']
        actual_value=count['value']
        print(actual_value)
        file_writer.writerow({
            'AccountSid' : str(i),
            'Call_Count' : count_calls,
            'Avg_Duration' : actual_value

        })
