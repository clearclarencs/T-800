# Discord qt monitor
import discord, json, requests
from discord.ext import commands

client=commands.Bot(command_prefix="/")

keywords = []
channels = []
with open("settings.json", "r") as r:
    settings = json.loads(r.read())

def refresh():
    global keywords, channels
    with open("channels.txt", "r") as r:
        channels = r.read().splitlines()
    with open("keywords.txt", "r") as r:
        keywords = r.read().splitlines()


def go(ctx):
    if settings["bot"] == "cybersole":
        headers = {"Cookie":settings["botCookie"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        requests.get("https://cybersole.io/dashboard/tasks?quicktask="+ctx.embeds[0].url, headers=headers)
        print("Sent "+ctx.embeds[0].url)
    else:
        print(settings["bot"]+" bot not supported")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(details="T-800 Monitoring..."))

@client.event
async def on_message(ctx):
    global keywords, channels
    refresh()
    if not str(ctx.channel.id) in channels:
        return
    for keyword in keywords:
        keywordList = keyword.split(",")
        good = True
        for kw in keywordList:
            if not kw.lower() in str(ctx.embeds[0].title).lower():
                good = False
                break
        if good:
            go(ctx)








client.run(settings["discordToken"], bot=False)