import requests
import json


params = (
    ('pretty', ' ,
    #('search_type', 'count ,
)

# totadata ='{"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"sid":{"value":"f2844f9c6df90a7600db86eeb29f157s","boost":1}}}]}}]}},"size":2,"aggs": {"group_by_status": {"terms": {"field": "status"}}},"sort" : [{"created" : {"order" : "desc"}}]}'
totadata='{"query":{"bool":{"must":[{"term":{"name":"verified_call_register_api"} }, {"term":{"tags.account_sid":"cartheroleadassist"} } ] } }, "aggs":{"group_by_http_code": {"terms": {"field": "tags.http_code","size":5}}}}'
toresp = requests.post('http://ts_product_metrics_crons:ts@crons!@odfe-metrics.internal.exotel.in:9200/odfe-metrics-application-2021.10.25/_search?pretty', params=params, data=totadata)
if toresp.ok:
    res = toresp.text

print(res)