import requests
url='https://cc75da0e5063855e3e52054290c4a44de9c3f6d6dd59f1ab:5c0a16d4dc0ebd6e43fa643980fff5bf84052f8bfb6d4c79@api.exotel.com/v2/accounts/xpressbees4/messages'
payload = '{"custom_data":"1255067982117","status_callback":"https://stage-whatsappbot.xbees.in/whatsapp-bot-service/exotel_webhook_events","whatsapp":{"messages":[{"from":"913340585384","to":"917988532204","content":{"type":"template","template":{"name":"ndr_varfiy_ques_v1","language":{"policy":"deterministic","code":"en"},"components":[{"type":"body","parameters":[{"type":"text","text":"1255067982117"},{"type":"text","text":"as you refused to accept"}]}]}}}]}}'
headers = {'Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)