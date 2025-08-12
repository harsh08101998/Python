import requests
import json,csv

listt=['02071172082','02071172085','02071177874','03340585129','03340585140','03340585317','03340585496','02048552341','02048552573','01141170569','01141170668','01141169606','01141133851','08046807512','08046810383','04045207578','04045207586','04071963020','07941058651','04440114060','04440114069','04440114134','04440114292','03340838528','03340838532','07949108372','04448132977','04448133139','04448134705','01140845356','08045683889','08045686180','08045691410','04049170354','04049170744','02048563481','08047092600','08047106807','08047109451','08047110524','08047163193','08047170605','01141197523','01141197525','01141197526','07948059762','08047185175','08047185418','08047186339','08047187793','08047189674','07314850135','07314850160','07314850281','07314853683','01414931304','04954260092','04954262365','04954262465','08068507759','08069451805','08069451997','08069452174','08069453645','08069453891','08069455131','08069459691','08045888299','08045888952','08047358967','08047359048','02047169998','02047170008','02047170023']


# listt=['08047091999']
params = (
    ('pretty', '') ,
    ('search_type', 'count') 
)


with open("swiggyosp1_last_call_on_VNcsv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['Tenant','VN','Last_call_made','Last_call_received','Total_call_count'])
    file_writer.writeheader()
    for i in listt:
        try :
            inbound_count_query={"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"vn":{"value":str(i),"boost":1}}},{"wildcard":{"direction":"inbound*"}}]}}]}},"size":1,"sort" : [{"created" : {"order" : "desc"}}]}

            query1 = json.dumps(inbound_count_query)

            outbound_count_query={"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"vn":{"value":str(i),"boost":1}}},{"wildcard":{"direction":"outbound*"}}]}}]}},"size":1,"sort" : [{"created" : {"order" : "desc"}}]}

            query2 = json.dumps(outbound_count_query)

            # total_call_count={"query":{"bool":{"must":[{"match":{"vn":"str(i)"}}]}}}
            total_call_count={"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"vn":{"value":str(i),"boost":1}}}]}}]}}}
            query3=json.dumps(total_call_count)
            # print(query3)


            url="http://es-inbox-2.internal.exotel.in:9200/calls_082024,calls_072024,calls_062024,calls_052024,calls_042024/call/_search?pretty"

            

            # avg_resp1 = requests.get('http://es-inbox-2.internal.exotel.in:9200/calls_012023,calls_122022,calls_112022,calls_102022,calls_092022/call/_search?pretty', params=params, data=query1)
            avg_resp1=requests.get(url, data=query1)

            # print(avg_resp1.json())
            hits2=avg_resp1.json()['hits']
            hits=hits2['hits']
            # print(hits[0]['_source']['tenant'])
            tenant=hits[0]['_source']['tenant']
            vn=hits[0]['_source']['vn']
            Last_call_received=hits[0]['_source']['created']

            # hits=avg_resp1.json()['aggregations']
            # count=hits['sum_of_duration']
            # actual_value=count['value']

        except IndexError:
            tenant=0;Last_call_received=0;vn=i
        try :
            avg_resp2 = requests.get(url, data=query2)
            hits4=avg_resp2.json()['hits']
            hit5=hits4['hits']
            # outbound_count_calls=hits2['total']
            Last_call_made=hit5[0]['_source']['created']

        except IndexError:
           Last_call_made=0

        # try :
        #     url2="http://es-inbox-2.internal.exotel.in:9200/calls_072024,calls_062024,calls_052024,calls_042024/call/_search?pretty&search_type=count"
        #     total_count_es=requests.get(url2, data=query3)
        #     # print(total_count_es)
        #     total_count_hits=total_count_es.json()['hits']
        #     # print(total_count_hits)
        #     actual_call_count=total_count_hits['total']
        # except IndexError:
        #     actual_call_count=0



        print(tenant,vn,Last_call_made,Last_call_received)
        file_writer.writerow({
            'Tenant' : tenant,
            'VN' : vn,
            'Last_call_made' : Last_call_made,
            'Last_call_received' : Last_call_received,
            # 'Total_call_count' :actual_call_count

        })
