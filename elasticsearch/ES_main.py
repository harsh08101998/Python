import requests
import json,csv


params = (
    ('pretty', ' ,
    ('size',100000)
    # ('search_type 
)

count=0
current_time='2021-12-'
days=['01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
with open("callfffs.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=["Time","VN","App_ID","Call_count","Price_Sum","Conversation_Duration"])
    file_writer.writeheader()
    
    for i in days:
        time1=current_time+str(i)+'T00:00:00'
        time2=current_time+str(i)+'T23:59:59'
        time3=current_time+str(i)

        # avg_query={"query":{"bool":{"must":[{"wildcard":{"vn":"0794*"}},{"range":{"start_time":{"gt":"2022-03-19T00:00:00","lt":"2022-03-19T23:59:59"}}},{"wildcard":{"primary_status":"outbound*"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
        # avg_query={"query":{"bool":{"must":[{"wildcard":{"vn":"02071*"}},{"wildcard":{"to":"+6*"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
        get_vn_detail={"query":{"bool":{"must":[{"term":{"tenant":{"value":"shipsy1"}}},{"range":{"created":{"gte":str(time1),"lte":str(time2)}}}]}},"aggs": {"group_by_server": {"terms": {"field": "vn","size":50000}}}}
        avg_query1 = json.dumps(get_vn_detail)
        print(get_vn_detail)
        avg_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_122021/call/_search?pretty&search_type=count&size=100000', params=params, data=avg_query1)
        hits=avg_resp.json()['aggregations']
        count=hits['group_by_server']
        # actual_value=count['value']
        ll=count['buckets']
        vn_list=[]
        for i in ll:
            vn=i['key']
            vn_list.append(vn)

        print(vn_list)
#         for vn in vn_list:
#             try:
#                 flow_detail={"query":{"bool":{"must":[{"term":{"vn":{"value":str(vn)}}},{"range":{"created":{"gte":str(time1),"lte":str(time2)}}}]}},"aggs": {"group_by_app": {"terms": {"field": "app_flow_id"}}}}
#                 avg_query2 = json.dumps(flow_detail)
#                 print(avg_query2)
#                 avg_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_122021/call/_search?pretty&search_type=count&size=100000', params=params, data=avg_query2)
#                 hits=avg_resp.json()['aggregations']
#                 count=hits['group_by_app']
#                 app_list=count['buckets']
#                 for i in app_list:
#                     app_id=str(i["key"])
#                     call_count=i['doc_count']
#                     price_sum={"query":{"bool":{"must":[{"term":{"vn":{"value":str(vn)}}},{"term":{"app_flow_id":{"value":str(app_id)}}},{"range":{"created":{"gte":str(time1),"lte":str(time2)}}}]}},"aggs": {"summm": {"sum": {"field": "price"}}}}
#                     price_sum_query = json.dumps(price_sum)
#                     avg_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_122021/call/_search?pretty&search_type=count&size=100000', params=params, data=price_sum_query)
#                     hits=avg_resp.json()['aggregations']
#                     price_sum=hits['summm']

#                     conversation_duration_sum={"query":{"bool":{"must":[{"term":{"vn":{"value":str(vn)}}},{"term":{"app_flow_id":{"value":str(app_id)}}},{"range":{"created":{"gte":str(time1),"lte":str(time2)}}}]}},"aggs": {"summmm": {"sum": {"field": "l2d"}}}}
#                     conversation_duration_query = json.dumps(conversation_duration_sum)
#                     avg_resp2 = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_122021/call/_search?pretty&search_type=count&size=100000', params=params, data=conversation_duration_query)
#                     hits2=avg_resp2.json()['aggregations']
#                     conversation_duration=hits2['summmm']

#                     print("vn :- ", vn)
#                     print("App Id :- ", app_id)
#                     print("call count :- ", call_count)
#                     print("price sum :- ", price_sum['value'])
#                     print("sume con :- ", conversation_duration['value'])


# # "V    N","    App_ID","Call_count","Price_Sum","Conversation_Duration"

#                     file_writer.writerow({
#                         "Time" : time3,
#                         "VN": vn,
#                         "App_ID" :app_id,
#                         "Call_count" : call_count,
#                         "Price_Sum":price_sum['value'],
#                         "Conversation_Duration":conversation_duration['value']
#                     })
#             except KeyError:
#                 continue


 # hits=avg_resp.json()['hits']
    # source=hits['hits']
    # for i in source:
    #     main_data=i['_source']
    #     sid=main_data['sid']
    #     tenant=main_data['tenant']
    #     to=main_data['to']
    #     from1=main_data['from']
    #     vn=main_data['vn']
    #     status=main_data['status']
    #     primary_status=main_data['primary_status']
    #     start_tim=main_data['start_time']
    #     l2d=main_data['l2d']
    #     duration=main_data['duration']
    #     file_writer.writerow({
    #         'sid' : sid,
    #         'tenant' : tenant,
    #         'to' : to,
    #         'from':from1,
    #         'vn':vn,
    #         'status' : status,
    #         'primary_status':primary_status,
    #         'start_time':start_tim,
    #         'l2d':l2d,
    #         'duration':duration

    #     })
    #     print(count)
    #     count+=1
   
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