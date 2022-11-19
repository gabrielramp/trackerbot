# Imports
import discord
from discord.ext import commands
import random
from datetime import datetime
import json

# Token available on discord dev portal
TOKEN = "MTA0MjE2NDc2MDU4MzYwMjIyNw.GsjZGx.-526uBZKq0Amk89YprZZWGVfwlyPhgrSyCj88s"

# Declaring intents
intents = discord.Intents(message_content = True, members = True, messages=True, guilds=True, voice_states = True)
client = commands.Bot(command_prefix='trackbot ', intents=intents)

# Bot functions
@client.command()
async def lotto(ctx):
    print("checking user")
    if (ctx.author.id == 135343913996255232):
        print("sending dm")
        user = await client.fetch_user(668282566540918810)
        await user.send("it's 5")
    else:
        print("user check failed")
        
@client.command(name="who's")
async def goodboy(ctx, *arg):
    print("checking user")
    if (ctx.author.id == 135343913996255232):
        print("sending dm")
        await ctx.send("i am")

@client.command()
async def bark(ctx, *arg):
    if ctx.author.id == 135343913996255232:
        await ctx.send("bark")
    else:
        print("that's not wormy")
        return

# Prints an embedded list of all recorded timestamps.
@client.command()
async def listfreq(ctx):
    with open("disconnecttable.json", "r") as distable:
        # Then loading the file into disconnecttable
        loadedtable = json.load(distable)
        embed = discord.Embed.from_dict(loadedtable)
    await ctx.send("Members last seen:")
    await ctx.send(embed=embed)
    
# Updates the JSON file with user's last timestamp, and creates a new timestamp if the user has not been recorded yet.
# Called when a user's voice state changes within the server
@client.event
async def on_voice_state_update(member, before, after):
    beforechannel = before.channel # Fetch previous channel user was in
    channel = after.channel # Fetch voice channel
    
    # If the user's state changed to disconnect
    if (after.channel==None):
        # Log disconnect timestamp
        timestamp = datetime.now().strftime("%m/%d/%Y %I:%M %p")
        await savedisconnect(member, timestamp)
        return
    
    curMembers = []
    for member in channel.members:
        curMembers.append(str(member).split('#')[0])
    print(str(member).split('#')[0], 'voicestate', channel)
    
    print(curMembers)

# Called to save a disconnect into table from on_voice_state_update
async def savedisconnect(member, newtimestamp):
    # debug
    print("Saving disconnect", member, newtimestamp)
    
    # Creating new entry for appending
    dictentry = {
        "name": str(member),
        "value": str(newtimestamp)
    }
    
    # Opening table as dictionary
    with open("disconnecttable.json", "r") as distable:
        # Then loading the file into disconnecttable
        loadedtable = json.load(distable)
    
    # Then opening the file to write
    with open("disconnecttable.json", "w") as distable:
        # If the member already exists on the table, update their timestamp
        flag = 0
        for each in loadedtable['fields']:
            if each['name'] == str(member):
                each['value'] = str(newtimestamp)
                flag = 1
        if flag == 0:
            loadedtable["fields"].append(dictentry)

        # Then dump the new dictionary into the json
        json.dump(loadedtable, distable, indent = 4, separators=(',', ': '))


# Announcing online
@client.event
async def on_ready():
        print("Trackbot online as {0.user}".format(client))

# run
client.run(TOKEN)