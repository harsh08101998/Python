from io import TextIOBase
import requests
import json

# script == php /home/exotel/jenkins/workspace/execution_machine-monthly-vnsplit-generator/RandomFoo/nirmal/callPriceSplitter.php 'docsapp1' "harsh.kumar@exotel.in" "2021-09-01 00:00:00" "2021-09-30 23:59:59"
accountsid=input("Please enter AccountSid :  ")
numbers=input("Please enter Numbers :  ").split(', 
for i in numbers:
    j='0'+str(i)
    data={"query":{"bool":{"must":[{"range":{"created":{"gte":"2022-04-01T00:00:00","lte":"2022-04-31T23:59:59"}}},{"term":{"tenant":str(accountsid)}},{"term":{"vn":str(j)}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{"vn_based_sum":{"sum":{"field":"price"}}}}

    data_json = json.dumps(data)
    # print(data_json)
    url="http://es-inbox-2.internal.exotel.in:9200/calls_102021/call/_search?pretty&search_type=count"
    x = requests.get(url, data=data_json)
    hits=x.json()['hits']
    count=hits['total']
    agg=x.json()['aggregations']
    value=agg["vn_based_sum"]
    price=value['value']
    print("| VN :",j,"| Call_Count :", count, "| Total_Price :", price)
   