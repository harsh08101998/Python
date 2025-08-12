import requests
url = '{"custom_data":"1255067982117","status_callback":"https://stage-whatsappbot.xbees.in/whatsapp-bot-service/exotel_webhook_events","whatsapp":{"messages":[{"from":"913340585384","to":"9503372694","content":{"type":"template","template":{"name":"ndr_varfiy_ques_v1","language":{"policy":"deterministic","code":"en"},"components":[{"type":"body","parameters":[{"type":"text","text":"1255067982117"},{"type":"text","text":"as you refused to accept"}]}]}}}]}}'
headers = {'Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)