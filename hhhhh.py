import json,csv

inbound_count_query='{"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"vn":{"value":"08047091999","boost":1}}},{"wildcard":{"recordingUrl":"https*"}}]}}]}},"size":1,"sort" : [{"created" : {"order" : "desc"}}]}'

print(inbound_count_query)