import requests

link ='http://yoda-api.appspot.com/api/v1/yodish?text='

quote = "Shane is a shit riven"

response = requests.get(f'http://yoda-api.appspot.com/api/v1/yodish?text={quote}')

response = response.json()

print(response['yodish'])

