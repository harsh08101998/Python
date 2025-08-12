import requests
import json


params = (
    ('pretty', ' ,
    #('search_type', 'count ,
)

totadata ='{"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"sid":{"value":"f2844f9c6df90a7600db86eeb29f157s","boost":1}}}]}}]}},"size":2,"aggs": {"group_by_status": {"terms": {"field": "status"}}},"sort" : [{"created" : {"order" : "desc"}}]}'
toresp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_062021,calls_072021,calls_082021,calls_092021/_search', params=params, data=totadata)
if toresp.ok:
    res = toresp.text

print(res)