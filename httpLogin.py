import requests
pload = {'username':'harsh.kumar@gmail.com','password':'HK1998@k'}
r = requests.post('https://dashboard.ngrok.com/login',data = pload)
print(r.text)