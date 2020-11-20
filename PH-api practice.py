import requests

response = requests.get("https://sv443.net/jokeapi/v2/joke/Any?type=single")

response = response.json()

print(response['joke'])