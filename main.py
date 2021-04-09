# Discord qt monitor
import discord, json, requests, time
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



def go(ctx):
    if settings["bot"] == "cybersoleqt":
        headers = {"Cookie":settings["botCookie"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        requests.get("https://cybersole.io/dashboard/tasks?quicktask="+ctx.embeds[0].url, headers=headers)
    if settings["bot"] == "cybersoleqt":
        headers = {"Cookie":settings["botCookie"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        requests.get("https://cybersole.io/dashboard/tasks?linkchange="+ctx.embeds[0].url, headers=headers)
    else:
        print(settings["bot"]+" bot not supported")
    print("Sent "+ctx.embeds[0].url)

@client.event
async def on_message(ctx):
    global keywords, channels, domains
    refresh()
    if not str(ctx.channel.id) in channels:
        return
    for keyword in keywords:
        keywordList = keyword.split(",")
        goodKw = True
        goodDom = False
        for kw in keywordList:
            if not kw.lower() in str(ctx.embeds[0].title).lower():
                goodKw = False
                break
        for domain in domains:
            if domain in str(ctx.embeds[0].url).lower():
                goodDom = True
                break
        if goodKw and goodDom:
            go(ctx)
            time.sleep(settings["cooldown"])
            return








client.run(settings["discordToken"], bot=False)