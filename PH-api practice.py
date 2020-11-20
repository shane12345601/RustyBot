import requests

response = requests.get('https://meme-api.herokuapp.com/gimme')

response = response.json()

print(response['url'])