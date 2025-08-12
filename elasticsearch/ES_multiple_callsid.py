import requests
import json,csv


params = (
    ('pretty', '') ,
    ('size',100000)
    # ('search_type 
)

count=0
print("           callsid           ", "    l1d ","    l2d   ","     call start_time", "     server")
with open("uniphore3_data2.csv", 'w',newline="") as fw:
        # file_writer=csv.DictWriter(fw,fieldnames=["tenant","sid","direction","vn","to","from","status","callStatus","created","start_time","l2d","duration","cause","cause_text","prediction","rawcc","sip_code","pdd_duration_in_ms"])
    file_writer=csv.DictWriter(fw,fieldnames=["sid","fromm","start_time","status"])
    file_writer.writeheader()
    
    callsid_list=['5d579965ce7d7499ec42a9dc5df7197s']

    for callsid in callsid_list:
        # print(callsid)
        # curl -s -XGET "http://es-inbox-2.internal.exotel.in:9200/calls_092024/call/_search?pretty" -d '{"query":{"bool":{"filter":[{"bool":{"must":[ {"match":{"tenant":"docsapp1"}},{"range":{"created":{"gte":"2024-09-01T20:00:00","lte":"2024-09-16T21:59:59"}}}, {"wildcard":{"to":"*-*"}}]}}]}}}

        # avg_query={"query":{"bool":{"must":[{"match":{"tenant":"hindustantimes3"}},{"match":{"from":str(callsid)}},{"range":{"start_time":{"gt":"2023-08-31T00:00:00","lt":"2023-08-31T23:59:49"}}}]}}}
        avg_query={"query":{"bool":{"must":[{"match":{"sid":str(callsid)}}]}}}
        avg_query1 = json.dumps(avg_query)
        # print(avg_query1)
        avg_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_072025,calls_032025/call/_search?pretty&size=10000', params=params, data=avg_query1)
        # print(avg_resp.json())
        hits=avg_resp.json()['hits']
        source=hits['hits']
        main_data=source[0]['_source']
        accountsid=main_data['tenant']
        start_time=main_data['start_time']
        callsid=main_data['sid']
        direction=main_data['direction']
        status=main_data['status']
        l1d=main_data['l1d']
        l2d=main_data['l2d']
        phoneNumberSid=main_data['phoneNumberSid']
        conversation_duration=main_data['conversation_duration']
        duration=main_data['duration']
        fromm=main_data['from']
        to=main_data['to']
        server=main_data['server']
        leg1CallerId=main_data['leg1CallerId']
        leg2CallerId=main_data['leg2CallerId']
        recordings=main_data['recordingUrl']
        direction2=main_data['direction']
        price=main_data['price']
        price_details=main_data['price_details']
        duration=main_data['duration']
        callStatus=main_data['callStatus']
        cost=main_data['cost']
        dialCallStatus=main_data['dialCallStatus']
        call_type=main_data['call_type']
        end_time=main_data['end_time']
        twcall_created_utc=main_data['twcall_created_utc']
        twcall_dateupdated=main_data['twcall_dateupdated']
        # print("      callsid           ", "  l1d ","l2d   ","   call start_time", "    server",    "direction", )
        # print(accountsid, callsid,',',l2d)
        print(callsid,',',phoneNumberSid,',',fromm,',',to,',',l1d,',',l2d,',',start_time,',',end_time,',',status,',',callStatus,',',dialCallStatus,',',server,',',recordings,',',cost)
        # file_writer.writerow({
        #     'sid' : callsid,
        #     'fromm' : fromm,
        #     'start_time' : start_time,
        #     'status' : status

        # })



        # print(source[0].get('_source )
        # print(source)
        # for i in source:
        #     try:
        #         main_data=i['_source']
        #         # print(main_data)
        #         cause_details=main_data['legs'][0]['cause_details']
        #         # print(cause_details.get('cause )
        #         sid=main_data['sid']
        #         tenant=main_data['tenant']
        #         to=main_data['to']
        #         from1=main_data['from']
        #         direction=main_data['direction']
        #         vn=main_data['vn']
        #         status=main_data['status']
        #         callStatus=main_data['callStatus']
        #         primary_status=main_data['created']
        #         start_tim=main_data['start_time']
        #         l2d=main_data['l2d']
        #         duration=main_data['duration']
        #         cause=cause_details.get('cause 
        #         cause_text=cause_details.get('cause_text 
        #         rawcc=cause_details.get('rawcc 
        #         sip_code=cause_details.get('sip_code 
        #         pdd_duration_in_ms=cause_details.get('pdd_duration_in_ms 
        #         prediction=cause_details.get('prediction 
        #         # "prediction","rawcc","sip_code","pdd_duration_in_ms"])
        #         file_writer.writerow({
        #             'sid' : sid,
        #             'tenant' : tenant,
        #             'direction':direction,
        #             'to' : to,
        #             'from':from1,
        #             'callStatus':callStatus,
        #             'vn':vn,
        #             'status' : status,
        #             'created':primary_status,
        #             'start_time':start_tim,
        #             'l2d':l2d,
        #             'duration':duration,
        #             'cause':cause,
        #             'cause_text':cause_text,
        #             'rawcc':rawcc,
        #             'sip_code':sip_code,
        #             'pdd_duration_in_ms':pdd_duration_in_ms,
        #             'prediction':prediction
        #         })
        #         print(count)
        #         print(sid)
        #         count+=1
        #     except TypeError:
        #         pass

            
