def get_users():
    import requests

    url = 'https://www.zohoapis.com/crm/v2/users'

    headers = {
        'Authorization': 'Zoho-oauthtoken 1000.fc1881f2fad9c41c1abf4f0d2a479062.e3097da4180369ab209aff3c5172e195'
        # 'If-Modified-Since': '2020-05-15T12:00:00+05:30'
    }

    parameters = {
        'type': 'AllUsers',
        'page': 1,
        'per_page': 10
    }

    response = requests.get(url=url, headers=headers, params=parameters)

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

get_users()