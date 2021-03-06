import discord
from discord.ext import commands, tasks
import imaplib, email, quopri, requests
from pornhub.pornhub_api import PornhubApi
import random
import os
from dotenv import load_dotenv
load_dotenv('.env')

api = PornhubApi()

client = commands.Bot(command_prefix='?')

@client.command(name='meme', help='For random meme')
async def meme(context):
    response = requests.get('https://meme-api.herokuapp.com/gimme')
    response = response.json()
    await context.message.channel.send(response['url'])

@client.command(name='loli', help='The best time of your life')
async def loli(context):
    if context.channel.is_nsfw():
        tags = ['blowjob', 'bj', 'boobs', 'cum', 'feet', 'hentai', 'wallpapers', 'spank', 'lesbian', 'lewd', 'pussy']
        link = 'http://api.nekos.fun:8080/api/'
        choice = random.choice(tags)
        try:
            response = requests.get(link + choice)
            temp = response.json()['image']
            await context.message.channel.send(f'{temp}')
        except:
            print("Error with loli api")
    else:
        await context.message.channel.send(f'You need to be in a NSFW channel')

@client.command(name='joke', help='For random joke')
async def joke(context):
    try:
        rply = requests.get('https://sv443.net/jokeapi/v2/joke/Any?type=single')
        rply = rply.json()
        msg = rply['joke']
        ebd = discord.Embed(colour=discord.Colour.dark_purple())
        ebd.add_field(name='Joke: ', value=msg, inline=False)
        await context.message.channel.send(embed=ebd)
    except:
        print("Error from joke api")

@client.command(name='ping', help='To show latency of bot')
async def ping(context):
    await context.message.channel.send(f'{round(client.latency * 1000)}ms')

@client.command(name='clear', help='To delete a specified amount of messages.')
@commands.has_permissions(manage_messages=True)
async def clear(context, amount: int):
    await context.channel.purge(limit=amount)

@clear.error
async def clear_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.message.channel.send("Please specify the amount of messages")
    if isinstance(error, commands.MissingPermissions):
        await context.message.channel.send("You do not have permission to Manage Messages")

@client.command(name='problem', help='To get your daily coding problem')
async def search(context):
    try:
        username = os.getenv('emailEmail')
        password = os.getenv('emailPassword')
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select('"CodingProblems"')
        result, data = mail.uid('search', None, "ALL")
        msgs = data[0].split()
        most_recent = msgs[-1]
        result ,data = mail.uid('fetch', most_recent, '(RFC822)')
        raw = data[0][1]
        decoded = quopri.decodestring(raw)
        emailMsg = email.message_from_bytes(decoded)
        payload = emailMsg.get_payload()
        sep = "printable"
        stripped = payload.split(sep, 1)[1]
        sep = "--------"
        stripped = stripped.split(sep, 1)[0]
        problem = stripped.strip()
        ebd = discord.Embed(colour=discord.Colour.teal())
        ebd.add_field(name='Problem: ', value=problem, inline=False)

        await context.message.channel.send(embed=ebd)
    except imaplib.IMAP4.error as e:
        print("Error: ", e)


@client.command(name='search', help='To find porn')
async def search(context, searchTerm):
    if context.channel.is_nsfw():
        data = api.search.search(q=searchTerm, ordering="mostviewed", period="weekly")
        for i in range(5):
            await context.message.channel.send(f'{i+1}. {data.videos[i].title}')

        await context.message.channel.send("Please send the number of the video for the url: ")

        msg = await client.wait_for(event="message")

        if msg.content == "1":
            await context.message.channel.send(f'URL for {data.videos[0].title}: {data.videos[0].url}')

        elif msg.content == "2":
            await context.message.channel.send(f'URL for {data.videos[1].title}: {data.videos[1].url}')

        elif msg.content == "3":
            await context.message.channel.send(f'URL for {data.videos[2].title}: {data.videos[2].url}')

        elif msg.content == "4":
            await context.message.channel.send(f'URL for {data.videos[3].title}: {data.videos[3].url}')

        elif msg.content == "5":
            await context.message.channel.send(f'URL for {data.videos[4].title}: {data.videos[4].url}')

        else:
            await context.message.channel.send("Invalid number! Search again.")
    else:
        await context.message.channel.send(f'You need to be in a NSFW channel')


@search.error
async def search_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.message.channel.send("Invalid input")


@client.event
async def on_ready():
    general_channel = client.get_channel(778697177915588610)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="?help for commands"))
    #await general_channel.send("Pesheng weng weng")
    print("rdy")

@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.message.channel.send("Invalid Command")

client.run(os.getenv('botToken'))