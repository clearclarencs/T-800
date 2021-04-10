# Discord qt monitor
import discord, json, requests, time, os, keyboard
from discord.ext import commands

client=commands.Bot(command_prefix="/")

keywords = []
channels = []
domains = []
with open("settings.json", "r") as r:
    settings = json.loads(r.read())

def refresh():
    global keywords, channels, domains
    with open("channels.txt", "r") as r:
        channels = r.read().splitlines()
    with open("keywords.txt", "r") as r:
        keywords = r.read().splitlines()
    with open("domains.txt", "r") as r:
        domains = r.read().splitlines()

def sent(link):
    print("Sent "+link)
    requests.post(settings["webhook"], json={"content":"Sent "+link}, headers={"Content-Type": "application/json"})

def go(ctx):
    try:
        link = ctx.embeds[0].url
        if len(str(link)) < 15:
            raise KeyError
    except:
        try:
            link = ctx.embeds[0].description.split("](")[1].split(")")[0]
            if len(str(link)) < 10:
                raise
        except:
            print("Error parsing link "+ctx.embeds[0].description)
    if settings["bot"] == "cybersoleqt":
        headers = {"Cookie":settings["botCookie"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        requests.get("https://cybersole.io/dashboard/tasks?quicktask="+link, headers=headers)
        sent(link)
    if settings["bot"] == "cybersoleqt":
        headers = {"Cookie":settings["botCookie"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        requests.get("https://cybersole.io/dashboard/tasks?linkchange="+link, headers=headers)
        sent(link)
    elif settings["bot"] == "cheggaio":
        command = 'echo | set /p nul=' + str(link).strip() + '| clip'
        os.system(command)
        keyboard.send('F9')
        sent(link)
    else:
        print(settings["bot"]+" bot not supported")

@client.event
async def on_message(ctx):
    global keywords, channels, domains
    refresh()
    if not str(ctx.channel.id) in channels:
        return
    embedMost = str(str(ctx.embeds[0].title).lower()+str(ctx.embeds[0].description).lower()+str(ctx.embeds[0].url).lower())
    for keyword in keywords:
        keywordList = keyword.split(",")
        goodKw = True
        goodDom = False
        for kw in keywordList:
            if not kw.lower() in embedMost:
                goodKw = False
                break
        for domain in domains:
            if domain in embedMost:
                goodDom = True
                break
        if goodKw and goodDom:
            go(ctx)
            time.sleep(settings["cooldown"])
            return








client.run(settings["discordToken"], bot=False)