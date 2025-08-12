
import requests
use=2

if use==1:
  accountsid='exotel905'
  api_token='102ea1c06725eedc481e93ea61df480c702b648b'  
  data = {
    'From': '08570027091',
    'CallerId': '08047091999',

    # 'CallerId':'08047091999',
    'To' : '08570027091',
    # 'TimeOut':'1000',
    # 'To':'sip:koppresh03ab215a',
    # '__RequestedServerCode':'0141_05',
    # 'CallType' : 'trans'
    'StatusCallback' : 'https://01jjp8cz7h98p7zr5dcpqmajnd00-2c7bd546399c838b1b37.requestinspector.com',
    # 'StatusCallbackEvents[0]':'dial',
    # 'StatusCallbackEvents[1]':'ringing',
    # 'StatusCallbackEvents[2]':'answered',
    'StatusCallbackEvents[0]':'terminal',
    # 'StartPlaybackValue':'https://s3-ap-southeast-1.amazonaws.com/exotelaudiouploads/f81b91db9822acd88bba950e96f507ff.wav',
    # 'StartPlaybackTo':'both'

    # 'Record':'true',
    # 'CustomField':'this is test'
    # 'Url': 'http://my.exotel.com/exotel905/exoml/start_voice/690756'
  } 
  url='https://{}:{}@api.exotel.com/v1/Accounts/{}/Calls/connect'.format(accountsid,api_token,accountsid)
  print(url)
  dataa=requests.post(url, data=data) 
  print(dataa.text)


###########################################################################################################################
if use==2:
  accountsid='exotel132m'
  api_token='b892ac29d703c208b415f9dce9f6c4412e264baf'

  data = {
    'From': '08570027091',
    'CallerId': '09228830528',
    # '__RequestedServerCode':'022_veeno_01',
    'To':'07988532204',
    # "StartPlaybackTo":"Callee",
    # "StartPlaybackValue":"https:\/\/www.jotish.in\/backend\/exotel\/audio2.wav",
    # "time_limit":10,
    # "timeout":30,
    '__RequestedServerCode':'022_veeno_01',
    # "StartPlaybackTo":"Callee","StartPlaybackValue":"https://www.jotish.in/backend/exotel/audio2.wav","StatusCallbackContentType":"application/json",
    # "StatusCallback":"https://01hy014hwsa7yh1a83dsr0ggmj00-7abc6321b8ffbda550b2.requestinspector.com","StatusCallbackEvents[0]":"terminal","CallerId":"08071189988","CustomField":"1642",
    # "Record":"true","RecordingChannels":"single","TimeLimit":40,"TimeOut":30,"To":"08197111478","WaitUrl":"https://www.jotish.in/backend/exotel/audio1.wav"
    # # 'CallerId':'08035778063',
    # 'To' : '08295771258',
    # 'To':'sip:harshkc5f7f95c',
    # 'CallType' : 'trans'
    # 'StatusCallback' : 'https://01j1q5fpb058nm0dm8xqqty0q000-a34ec8f4c45b4b01e64a.requestinspector.com',
    # 'StatusCallbackEvents[0]':'terminal',
    # "StatusCallbackContentType" : "application/json",
    
        # 'CustomField':"{\"appointmentId\":27066,\"appointmentDate\":\"Friday, 22 September 23\",\"slot\":\"07:48 PM-07:58 PM\",\"brand\":\"MM\",\"source\":\"DA\",\"patientFirst\":true}"

    # 'TimeOut':'80',
    # 'Url': 'http://my.in.exotel.com/navi63m/exoml/start_voice/19713'
  }

  url='https://{}:{}@api.in.exotel.com/v1/Accounts/{}/Calls/connect.json'.format(accountsid,api_token,accountsid)
  # url='https://{}:{}@ccm-api.exotel.com/v3/accounts/{}/calls'.format(accountsid,api_token,accountsid)

  print(url)
  dataa=requests.post(url, data=data)

  print(dataa.text)