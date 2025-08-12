import requests
import json,csv

listt=['srishti2','angelbroking4','accenture56','joinditto1','williamoneilindia2','coutloot1','zarity1','xseededucation3','sensibull1','snitch1','mvni61','mobitrade2','solethreads1','chezuba','ankerinnovations1','aptech3','unotag1','digitalaicademy1','nilkamal2','gdfs61','shodashisutras1','akshaykalyanjisavla1','xploresystems1','nova63','dawaadost1','kazam3','topchop1','nikahforever1','spicywagon1','jansahasindia3','lorrycircle1','jvias2','secondconsult1','edmingle1','singledebt1','byteridge2','vdalphtech1','namastedwaar1','instrucko1','upsure1','boomitra1','buenofinance1','onsite3','claimfriendy1','parkendo1','functionup2','shiminly1','theprimelearning1','coditas2','mobilitxfuture1','emhealth1','trayahealth1','novabenefitsinsurancebrokers1','lawctopus2','meesho62','vivitrapharma2','ssedutech1','getinstacash1','glamlooksstudio1','liquiloans1','planettechnologies1','pw6201','avantifellows3','prokaart1','optimumtechnologies1','lenditt1','gtholidays1','fpa621','interviewkickstart1','medbikri1','k624a1','nureca2','tutorac1','spectratally1','tadworld1','materialdepot1','animall3','bookbyrooms1','tssolutions2','betheshyft1','aurusit1','oracare1','narayanahealth5','ketoindia2','evbazaar1','adventsystems1','i30success1','agriconnectindia1','olx621','edyoda3','turbo1','boodmo3','draravindsivf1','liquiloans3','mcapital1','oawa61','asyouplan1','technoje1','openplaytech1','alignbooks1','blusmartmobilitytech1','spardhaschoolofmusic2','bombayshirts2','edanafarms1','innocirc1','financedoctor1','empowerpragati1','mtandt2','studytabletest1','savein1','suryahotelsandproperties1','expertrating1','trashin1','arkinfo1','unschool3','printwellindia1','mapmycrop1','pocketly1','vizzve2','smartinterviews2','affinidi1','shareindia1','conreitechnologies1','campus3651','mahindra71','tallysolutions','eagle4','sparkconsultancypro1','adhyayanmantra1','superk1','wooqer1','thesettl1','moonstonehammock1','vonixtechnologies1','pradeepit2','vaidban1','waycool4','rahlegal1','snapmint','brightlifecare2','chaloexam1','kasturilifestyle1','neodove9','levi62','ivypods2','manuvarghesedigital2','prepinsta2','diagnosticbazar1','ezyschooling1','kesavmedical1','cleanz242','swarupraodg1','prashantadvaitfoundation2','mallwise1','memoapp1','ayurvaid1','tellyon1','dspeedup1','mykarehealth1','narainsons3','straightline2','tossinpizza1','nimbuspost2','altfspaces3','brandscaleindia1','snovasys4','gloplax1','staysturmfrei1','xime62','gazick2','techtrade1','indicschools1','prodigycart2','wizkidscarnival2','jurasystems1','scaler6','ppreciate1','jyotisyam1','damngood2','leapforword5','accenture1m','healthylife1m','myspotlight1m','visionaryskincare1m','anveya1m','globalbees1m','revolutionarynutrition1m','getveganway1m','rain61m','yantralive1m','theextraaedge1m','exotel905']

# listt=['exotel905']
params = (
    ('pretty', ' ,
    ('search_type', 'count 
)

# totadata ='{"query":{"bool":{"filter":[{"bool":{"must":[{"term":{"sid":{"value":"f2844f9c6df90a7600db86eeb29f157s","boost":1}}}]}}]}},"size":2,"aggs": {"group_by_status": {"terms": {"field": "status"}}},"sort" : [{"created" : {"order" : "desc"}}]}'
# toresp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_062021,calls_072021,calls_082021,calls_092021/_search', params=params, data=totadata)
# if toresp.ok:
#     res = toresp.text

#todata='{"query":{"bool":{must:[{"term":{"tenant":{"value":"exotel905"}}},{"range":{"created":{"gte":"2021-10-01T00:00:00","lte":"2021-10-31T23:59:59"}}}]}}}'
with open("Feb_SG_Calls_Count_and_Duration1.csv", 'w',newline="") as fw:
    file_writer=csv.DictWriter(fw,fieldnames=['AccountSid','Inbound_total','Invound_completed','Outbound_total','Outbound_completed'])
    file_writer.writeheader()
    for i in listt:
        try :
            # count_query={"query":{"bool":{"must":[{"term":{"tenant":{"value":str(i)}}}]}}}
            # avg_query={"query":{"bool":{"must":[{"term":{"tenant":{"value":str(i)}}}]}},"aggs": {"avg_grade": { "avg": { "field": "duration"}}}}
            inbound_count_query={"query":{"bool":{"must":[{"match":{"tenant":str(i)}},{"wildcard":{"direction":"inbound*"}}]}},"aggs": {"sum_of_duration": {"sum": {"field": "duration"}}}}
            query1 = json.dumps(inbound_count_query)

            outbound_count_query={"query":{"bool":{"must":[{"match":{"tenant":str(i)}},{"wildcard":{"direction":"outbound*"}}]}},"aggs": {"sum_of_duration": {"sum": {"field": "duration"}}}}
            query2 = json.dumps(outbound_count_query)

            # count_resp = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_032022/call/_search?pretty&search_type=count', params=params, data=count_query1)
            avg_resp1 = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_112022/call/_search?pretty&search_type=count', params=params, data=query1)

            hits=avg_resp1.json()['hits']
            inbound_count_calls=hits['total']
            # print(inbound_count_calls)

            hits=avg_resp1.json()['aggregations']
            count=hits['sum_of_duration']
            actual_value=count['value']
            # print(actual_value)
            # inbound_count_completed=actual_value[0]['doc_count']
            # print(inbound_count_completed)
        except IndexError:
            inbound_count_calls=0;inbound_count_completed=0
        try :
            avg_resp2 = requests.post('http://es-inbox-2.internal.exotel.in:9200/calls_112022/call/_search?pretty&search_type=count', params=params, data=query2)
            hits2=avg_resp2.json()['hits']
            outbound_count_calls=hits2['total']

            hits2=avg_resp2.json()['aggregations']
            count2=hits2['sum_of_duration']
            actual_value2=count2['value']
            # print(actual_value2)
            # outbound_count_completed=actual_value2[0]['doc_count']
        except IndexError:
            outbound_count_calls=0;outbound_count_completed=0
        print(i, ',',actual_value,',', actual_value2)

        
        # print(i, inbound_count_calls, inbound_count_completed, outbound_count_calls, outbound_count_completed)
        # file_writer.writerow({
        #     'AccountSid' : str(i),
        #     'Inbound_total' : inbound_count_calls,
        #     'Invound_completed' : inbound_count_completed,
        #     'Outbound_total' : outbound_count_calls,
        #     'Outbound_completed' : outbound_count_completed

        # })
