
import requests
import time

use=1

if use==1:
  accountsid='exotel905'
  api_token='102ea1c06725eedc481e93ea61df480c702b648b'  
  data = {
    'From': '01204033606',
    'CallerId': '08047091999',

    # 'CallerId':'08047091999',
    'To' : '09819756590',
    # 'TimeOut':'1000',
    # 'To':'sip:koppresh03ab215a',
    # '__RequestedServerCode':'040_14',
    # 'CallType' : 'trans'
    # 'StatusCallback' : 'https://01jmewj2wtvykw6x7af7xwzykk00-74d2650929be906c0c67.requestinspector.com',
    # 'StatusCallbackEvents':'dial',
    # 'StatusCallbackEvents[1]':'ringing',
    # 'StatusCallbackEvents[2]':'answered',
    # 'StatusCallbackEvents[0]':'terminal',
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
  accountsid='exotelt'
  api_token='eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b'

  data = {
    'From': '08570027091',
    'CallerId': '08045246232',
    # '__RequestedServerCode':'022_veeno_01',
    'To':'07988532204',
    # "StartPlaybackTo":"Callee",
    # "StartPlaybackValue":"https:\/\/www.jotish.in\/backend\/exotel\/audio2.wav",
    # "time_limit":10,
    # "timeout":30,
    # '__RequestedServerCode':'0731_09',
    # "StartPlaybackTo":"Callee","StartPlaybackValue":"https://www.jotish.in/backend/exotel/audio2.wav","StatusCallbackContentType":"application/json",
    # "StatusCallback":"https://01hy014hwsa7yh1a83dsr0ggmj00-7abc6321b8ffbda550b2.requestinspector.com","StatusCallbackEvents[0]":"terminal","CallerId":"08071189988","CustomField":"1642",
    # "Record":"true","RecordingChannels":"single","TimeLimit":40,"TimeOut":30,"To":"08197111478","WaitUrl":"https://www.jotish.in/backend/exotel/audio1.wav"
    # # 'CallerId':'08035778063',
    # 'To' : '08295771258',
    # 'To':'sip:harshkc5f7f95c',
    # 'CallType' : 'trans'
    # 'StatusCallback' : 'https://01jp7y11b0gkzbmzsx4yxh0bq200-a005745220c1523aa876.requestinspector.com',
    # 'StatusCallbackEvents[0]':'terminal'
    # "StatusCallbackContentType" : "application/json",
    
        # 'CustomField':"{\"appointmentId\":27066,\"appointmentDate\":\"Friday, 22 September 23\",\"slot\":\"07:48 PM-07:58 PM\",\"brand\":\"MM\",\"source\":\"DA\",\"patientFirst\":true}"

    # 'TimeOut':'80',
    # 'Url': 'http://my.in.exotel.com/navi63m/exoml/start_voice/19713'
  }

  url='https://{}:{}@api.exotel.com/v1/Accounts/{}/Calls/connect'.format(accountsid,api_token,accountsid)
  # url='https://{}:{}@ccm-api.exotel.com/v3/accounts/{}/calls'.format(accountsid,api_token,accountsid)

  print(url)
  dataa=requests.post(url, data=data)

  print(dataa.text)



############################### for multiple number testing ###############################################


if use==3:
  accountsid='exotelt'
  api_token='eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b'

  number_list=['07971038774']
  for i in number_list:
    data = {
      'From': '08570027091',
      'CallerId': '07948220002',
      'To':'07988532204',
      '__RequestedServerCode':'079_veeno_01',
      '__IgnoreServerStatus':'true',
       'Record':'true'
    }
    url='https://{}:{}@api.exotel.com/v1/Accounts/{}/Calls/connect.json'.format(accountsid,api_token,accountsid)

    print(url)
    dataa=requests.post(url, data=data)

    print(dataa.text)
    # time.sleep(20)