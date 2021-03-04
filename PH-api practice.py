import requests
import random
import pymongo

tags = ['blowjob', 'bj', 'boobs', 'cum', 'feet', 'hentai', 'wallpapers', 'spank', 'lesbian', 'lewd', 'pussy']

link ='http://api.nekos.fun:8080/api/'

choice = random.choice(tags)

try:
    response = requests.get(link+choice)
    temp = response.json()['image']
    #await context.message.channel.send(f'{temp}')
except:
    print("Error with loli api")


client = pymongo.MongoClient("mongodb+srv://rustyAdmin:Neverever786@cluster0.ds0yx.mongodb.net/RustyBot?retryWrites=true&w=majority")
db = client.test