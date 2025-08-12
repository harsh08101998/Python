import requests
import json,csv


params = (
    ('pretty', ' '),
    ('size',100000)
    # ('search_type 
)

count=0

with open("manipalgroup2.csv", 'w',newline="") as fw:
    # file_writer=csv.DictWriter(fw,fieldnames=["id","direction","vn","to","from","status","callStatus","created","start_time","leg1CallerId","duration","cause","cause_text","recordingUrl","rawcc","sip_code","pdd_duration_in_ms"])
    # file_writer=csv.DictWriter(fw,fieldnames=["Id","Direction","ExotelNumber","From","To","Status","StartTime","EndTime","Duration","Price","RecordingUrls","PriceDetails","Leg1Status","Leg2Status","ConversationDuration","AppID","AppName","Digits","DisconnectedBy"])
    file_writer=csv.DictWriter(fw,fieldnames=["Id","Direction","ExotelNumber","From","To"])

    file_writer.writeheader()
    # avg_query={"query":{"bool":{"must":[{"wildcard":{"vn":"0794*"}},{"
    # range":{"start_time":{"gt":"2022-03-19T00:00:00","lt":"2022-03-19T23:59:59"}}},{"wildcard":{"primary_status":"outbound*"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
    # avg_query={"query":{"bool":{"must":[{"wildcard":{"from":"01141193130"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
    # avg_query={"query":{"bool":{"must":[{"match":{"tenant":"docsapp1"}},{"range":{"start_time":{"gt":"2024-09-21T00:00:00","lt":"2024-09-23T00:00:00"}}}]}}}
    # avg_query={"query":{"bool":{"must":[{"match":{"tenant":"wareiq1"}}]}}}
    avg_query={"query":{"bool":{"filter":[{"bool":{"must":[ {"match":{"tenant":"manipalgroup2"}},{"range":{"created":{"gte":"2024-09-01T00:00:00","lte":"2024-09-26T21:59:59"}}}, {"wildcard":{"to":"*_*"}}]}}]}}}
    avg_query1 = json.dumps(avg_query)
    print(avg_query1)
    avg_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_092024/call/_search?pretty&size=100000', params=params, data=avg_query1)
    print(avg_resp)
    hits=avg_resp.json()['hits']
    source=hits['hits']
    # print(source)
    # print(source[0].get('_source ))
    # print(source)
    for i in source:

        try:
            main_data=i['_source']
            # print(main_data)
            # cause_details=main_data['legs'][0]['cause_details']
            # print(cause_details.get('cause ))
            sid=main_data['sid']
            tenant=main_data['tenant']
            to=main_data['to']
            from1=main_data['from']
            direction=main_data['direction']
            vn=main_data['vn']
            # status=main_data['status']
            # callStatus=main_data['callStatus']
            # primary_status=main_data['created']
            # start_tim=main_data['start_time']
            # leg1CallerId=main_data['leg1CallerId']
            # duration=main_data['duration']
            # price=main_data['price']

            # recordingUrl=main_data.get('recordingUrl')
            # PriceDetails=main_data.get('price_details')
            # Leg1Status=main_data.get('callStatus')
            # Leg2Status=main_data.get('dialCallStatus')
            # ConversationDuration=main_data.get('conversation_duration')
            # AppName=main_data.get('app_flow_name')
            # Digits=main_data.get('app_dtmf')
            # DisconnectedBy=main_data.get('disconnected_by')
            # AppID=main_data.get('app_flow_id')


            # cause=cause_details.get('cause') 
            # cause_text=cause_details.get('cause_text')
            # rawcc=cause_details.get('rawcc')
            # sip_code=cause_details.get('sip_code')
            # pdd_duration_in_ms=cause_details.get('pdd_duration_in_ms') 

            # "prediction","rawcc","sip_code","pdd_duration_in_ms"])
            file_writer.writerow({
                'Id' : sid,
                'Direction':direction,
                'To' : to,
                'From':from1,
                'ExotelNumber':vn,
                # 'Status' : status,
                # 'StartTime':start_tim,
                # 'Duration':duration,
                # 'PriceDetails':PriceDetails,
                # 'Leg1Status':Leg1Status,
                # 'Leg2Status':Leg2Status,
                # 'ConversationDuration':ConversationDuration,
                # 'AppName':AppName,
                # 'Digits':Digits,
                # 'DisconnectedBy':DisconnectedBy,
                # 'AppID':AppID,
                # 'Price':price,
                # 'RecordingUrls':recordingUrl

                # 'cause':cause,
                # 'cause_text':cause_text,
                # 'rawcc':rawcc,
                # 'sip_code':sip_code,
                # 'pdd_duration_in_ms':pdd_duration_in_ms,
                
            })
            # print(count)
            # print(sid)
            count+=1
        except TypeError:
            pass

   
# ############################ For Aggregation usage
#     hits=avg_resp.json()['aggregations']
#     count=hits['avg_grade']
#     actual_value=count['value']
#     print(actual_value)
#     file_writer.writerow({
#         'AccountSid' : str(i),
#         'Call_Count' : count_calls,
#         'Avg_Duration' : actual_value
#     })