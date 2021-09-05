import discord
import os
from discord import Message
from discord.ext import tasks, commands
import requests
import json
from riotwatcher import LolWatcher
from sqlite3 import connect
from datetime import date, datetime
import ast

key = 'YOUR RIOT API KEY'
watcher = LolWatcher(key)
Database = connect("YOUR PATH TO YOUR DATABASE")
Cursor = Database.cursor()


class database:
    def field(command, *values):
        Cursor.execute(command, tuple(values))
        fetch = Cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        return

    def one_record(command, *values):
        Cursor.execute(command, tuple(values))
        return Cursor.fetchone()

    def records(command, *values):
        Cursor.execute(command, tuple(values))
        return Cursor.fetchall()

    def column(command, *values):
        Cursor.execute(command, tuple(values))
        return [item[0] for item in Cursor.fetchall()]

    def execute(command, *values):
        Cursor.execute(command, tuple(values))
        return

    async def commit():
        Database.commit()
        return

    def disconnect():
        Database.close()
        return


def tierFormat(tier):
    if tier == "IRON":
        tier = "Iron"
    elif tier == "BRONZE":
        tier = "Bronze"
    elif tier == "SILVER":
        tier = "Silver"
    elif tier == "GOLD":
        tier = "Gold"
    elif tier == "PLATINUM":
        tier = "Platinum"
    elif tier == "DIAMOND":
        tier = "Diamond"

    return tier


def printStats(summonerName):
    summoner = watcher.summoner.by_name('na1', summonerName)
    stats = watcher.league.by_summoner('na1', summoner['id'])
    if not stats:
        return 0
    elif stats[0]['queueType'] == 'RANKED_SOLO_5x5' and len(stats) == 1:
        tier = stats[0]['tier']
        rank = stats[0]['rank']
        lp = stats[0]['leaguePoints']
        wins = int(stats[0]['wins'])
        losses = int(stats[0]['losses'])
        winrate = 100*(wins/(wins+losses))
        return str(1), tier, rank, str(lp), str(round(winrate, 2))

    elif stats[0]['queueType'] == 'RANKED_FLEX_SR' and len(stats) == 1:
        tier = stats[0]['tier']
        rank = stats[0]['rank']
        lp = stats[0]['leaguePoints']
        wins = int(stats[0]['wins'])
        losses = int(stats[0]['losses'])
        winrate = 100*(wins/(wins+losses))
        return str(2), tier, rank, str(lp), str(round(winrate, 2))

    elif stats[0]['queueType'] == 'RANKED_SOLO_5x5':
        tier = stats[0]['tier']
        rank = stats[0]['rank']
        lp = stats[0]['leaguePoints']
        wins = int(stats[0]['wins'])
        losses = int(stats[0]['losses'])
        winrate = 100*(wins/(wins+losses))
        ftier = stats[1]['tier']
        frank = stats[1]['rank']
        flp = stats[1]['leaguePoints']
        fwins = int(stats[1]['wins'])
        flosses = int(stats[1]['losses'])
        fwinrate = 100*(fwins/(fwins+flosses))

    else:
        ftier = stats[0]['tier']
        frank = stats[0]['rank']
        flp = stats[0]['leaguePoints']
        fwins = int(stats[0]['wins'])
        flosses = int(stats[0]['losses'])
        fwinrate = 100*(fwins/(fwins+flosses))
        tier = stats[1]['tier']
        rank = stats[1]['rank']
        lp = stats[1]['leaguePoints']
        wins = int(stats[1]['wins'])
        losses = int(stats[1]['losses'])
        winrate = 100*(wins/(wins+losses))

    ftier = tierFormat(ftier)
    tier = tierFormat(tier)

    return tier, rank, str(lp), str(round(winrate, 2)), ftier, frank, str(flp), str(round(fwinrate, 2))


def livechecker(summonerName):
    summoner = watcher.summoner.by_name('na1', summonerName)

    try:
        stats = watcher.spectator.by_summoner('na1', summoner['id'])
        print(stats)
        return 0, stats['gameId']
    except:
        return 1, 1


def spectator(summonerName):
    summoner = watcher.summoner.by_name('na1', summonerName)
    try:
        stats = watcher.spectator.by_summoner('na1', summoner['id'])
        print(stats)
        return 0
    except:
        print("Player not active")
        return 1


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    addloop.start()


@tasks.loop(seconds=10)
async def addloop():
    channel = client.get_channel(YOUR CHANNEL ID)
    tup = database.records("SELECT * FROM users")
    row = [item[0] for item in tup]
    for i in row:
        temp = livechecker(i)
        if temp[0] == 0:
            try:
                database.execute(
                    "INSERT INTO gameid (id,userid) VALUES (?,?)", temp[1], i)

                await channel.send(i + " is in game")

            except:
                print("game already printed")

        else:
            print(i + " Dead")
    Database.commit()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('$tunkgon'):

        await message.channel.send('Hi This is Tunkgon Bot!')

    if message.content.startswith('$summoner'):
        summoner = msg.split("$summoner ", 1)[1]
        stats = printStats(summoner)
        if stats == 0:
            await message.channel.send("Player is Unranked")
        elif stats[0] == '1':
            await message.channel.send("**Ranked Solo/Duo**\nRank: " + stats[1] + " " + stats[2] + " " + stats[3] + "\n" + "Winrate: " + stats[4])
        elif stats[0] == '2':
            await message.channel.send("**Ranked Solo/Duo**\nRank: " + stats[1] + " " + stats[2] + " " + stats[3] + "\n" + "Winrate: " + stats[4])
        else:
            await message.channel.send("**Solo/Duo**\nRank: " + stats[0] + " " + stats[1] + " " + stats[2] + "\n" + "Winrate: " + stats[3] + '\n' + "**Flex Rank** \n" + "Rank: " + stats[4] + " " + stats[5] + " " + stats[6] + "\n" + "Winrate: " + stats[7])

    if message.content.startswith('$live'):
        summoner = msg.split("$live ", 1)[1]
        info = spectator(summoner)
        if info == 0:
            await message.channel.send("Player is in game")
        if info == 1:
            await message.channel.send("Player is currently not in game")

    if message.content.startswith('$add'):
        summoner = msg.split("$add ", 1)[1]
        try:
            database.execute(
                "INSERT INTO users (summonerName) VALUES (?)", summoner)
            Database.commit()
        except:
            await message.channel.send("Player is already in the list")

    if message.content.startswith('$remove'):
        summoner = msg.split("$remove ", 1)[1]
        database.execute("DELETE FROM users WHERE summonerName = ?", summoner)

    if message.content.startswith('$list'):
        list = database.records("SELECT * FROM users")
        await message.channel.send(list)


client.run('YOUR DISCORD KEY')
