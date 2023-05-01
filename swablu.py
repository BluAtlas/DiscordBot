# Swablu discord bot
# November 2019 - December 2022
# By Dillon Anderson
# Primary bot used for private servers


import random
import discord
from discord.ext import tasks
from datetime import datetime
from nautc import convert
import asyncpraw
from pathlib import Path

from mytokens import discordToken
from myservers import server
from myRedditBot import redditBot


botfile = discordToken
serverfile = server

#   #Logging to file 'discord.log'
#   logger = logging.getLogger('discord')
#   logger.setLevel(logging.DEBUG)
#   handler = logging.FileHandler(filename=log.txt, encoding='utf-8', mode='w')
#   handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#   logger.addHandler(handler)


TOKEN = botfile.getToken()

intents = discord.Intents.all()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    printt('Logged on as {0}!\n'.format(client.user))
    Path("./oldtime.tmp").touch()
    sendFreeGameNotification.start()

# Runs on server join, converts own nickname to fancytext, Prints message


@client.event
async def on_guild_join(guild):
    printt("Joined guild: [{0}]" .format(guild))
    botself = await guild.fetch_member(botfile.getID())
    await botself.edit(nick=normalToFancy(botself.name))


@client.event
# Runs commands - $hello, $nick
async def on_message(message: discord.message.Message):
    if message.author == client.user:
        return
    # $hello: Responds to $hello with Hello!
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        printt("Said hello to [{0.author}]\n".format(message))

    # $nick: 1 arg, change the nickname of commander to fancytext(arg1)
    if message.content.startswith('$nick'):
        cutcontent = message.content[6:len(message.content)]
        if cutcontent != '':
            fancyname = normalToFancy(cutcontent)
            await message.author.edit(nick=fancyname)
            printt("N: Changed [{0.author}]'s nickname to fancytext('{1}')\n".format(
                message, cutcontent))
        else:
            fancyname = normalToFancy(message.author.display_name)
            await message.author.edit(nick=fancyname)
            printt("N: Changed [{0.author}]'s nickname to {1}\n".format(
                message, fancyname))

    if message.content.startswith('$refresh'):
        if message.author.guild.get_role(serverfile.getAdminRole()) not in message.author.roles:
            printt("refreshed attempted by [{0}] but lacks permissions to do so".format(
                message.author))
            return
        else:
            printt("Refresh started by [{0}]\n".format(message.author))

        for member in message.author.guild.members:
            fancyname = normalToFancy(member.display_name)

            serverroles = serverfile.getRoles()

            newrole = member.guild.get_role(serverfile.getDefaultRole())
            newroles = [newrole]

            newrole = member.guild.get_role(
                serverroles[random.randrange(0, len(serverroles))])
            newroles.append(newrole)

            try:
                await member.edit(nick=fancyname)
                printt(
                    "R: Changed [{0}]'s nickname to {1}" .format(member, fancyname))
                await member.edit(roles=[])
                await member.edit(roles=newroles)
                printt('R: Deleted all roles, Added role [{0}] and default role to member [{1}]\n' .format(
                    newrole, member))
            except:
                printt("R: Failed to edit member [{0}], user is admin.\n".format(
                    member))
        printt("Refresh run by [{0}] Completed\n".format(message.author))


# Runs on member join, Prints message, gives new member fancytext nickname and prints success message
# Assigns new member a default role and random role from serverfile

@client.event
async def on_member_join(member: discord.Member):
    printt('J: {0.name} has joined the server!\n' .format(member))

    fancyname = normalToFancy(member.display_name)
    await member.edit(nick=fancyname)
    printt(
        "J: Changed [{0}]'s nickname to {1}\n" .format(member, fancyname))

    serverroles = serverfile.getRoles()
    newroles = member.roles

    newrole = member.guild.get_role(serverfile.getDefaultRole())
    newroles.append(newrole)

    newrole = member.guild.get_role(
        serverroles[random.randrange(0, len(serverroles))])
    newroles.append(newrole)
    await member.edit(roles=newroles)
    printt('J: Added role [{0}] and default role to member [{1}]' .format(
        newrole, member))


@client.event
async def on_member_update(mbefore, mafter):
    if mbefore.display_name != mafter.display_name:
        printt("U: Attempted name change of [{0}]".format(mbefore))
        fancyname = normalToFancy(mafter.display_name)
        await mafter.edit(nick=fancyname)
        printt("U: Nickname of [{0}] changed to {1}".format(
            mbefore, fancyname))

# converts string to double-struck unicode


def normalToFancy(name):
    try:
        newname = ""
        for txt in convert(name):
            if txt[0] == "Double Struck":
                newname = txt[1]
        return newname
    except:
        # if new method fails, fallback to old
        printt(
            "normalToFancy failed on [{0}], using old function instead".format(name))
        return normalToFancyy(name)


# Utility Function, takes a string of regular characters, returns fancytext characters
def normalToFancyy(name):
    normaltext = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    fancytext = '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘'

    flag = False
    fancyname = ''
    for i in name:
        for j in range(len(normaltext)):
            if i == normaltext[j]:
                fancyname += fancytext[j]
                flag = True
                break
        if not flag:
            fancyname += i
        flag = False
    return fancyname


# Check r/gamedeals and post free games


@tasks.loop(seconds=60*10)
async def sendFreeGameNotification():
    try:  # try and except in case of crash so the task will continue to loop even when errors occur
        # printt("Scrubbing reddit...")

        oldTime = readOldtime()

        # get the channel the bot will post too
        botChannel = client.get_channel(server.getChannelId())

        # setup asyncpraw reddit instance
        subreddit_name = "gamedeals"
        reddit = asyncpraw.Reddit(client_id=redditBot.getClientID(),
                                  client_secret=redditBot.getClientSecret(),
                                  user_agent=redditBot.getUserAgent())
        try:  # second try clause to avoid unclosed reddit session

            subreddit = await reddit.subreddit(subreddit_name)

            # get list of recent posts and sort oldest to newest
            posts = []
            async for post in subreddit.new(limit=10):
                posts.append(post)
            posts.reverse()

            # If this is the first scrub, set oldTime to the newest post and don't send anything
            if oldTime == 0.0:
                oldTime = posts[-1].created
                writeOldtime(str(oldTime))

            # loop over posts, send any new free deals to the channel
            for post in posts:
                if ("100%" in post.title.lower()) and post.created > oldTime:

                    embed = discord.Embed(title="Direct Link to Store Page",
                                          url=post.url)
                    embed.set_author(name=post.title[:257],
                                     url="https://www.reddit.com"+post.permalink)
                    embed.set_footer(text=post.url)

                    printt("Sending Post: " + post.title)
                    await botChannel.send(embed=embed)

                    oldTime = post.created
                    writeOldtime(str(oldTime) + "\n")
            # close reddit, truncate and close file
            await reddit.close()
        except Exception as e:
            printt("Scrubbing Reddit Failed:", end="")
            print(e)
            await reddit.close()
    except Exception as e:
        printt("Scrubbing Reddit Failed:", end="")
        print(e)


def writeOldtime(string):
    f = open("oldtime.tmp", "w")
    f.write(string)
    f.close()


def readOldtime():
    f = open("oldtime.tmp", "r")
    lines = f.readlines()
    f.close()

    if len(lines) > 0:
        return float(lines[-1])
    return 0.0


def printt(string, end="\n"):
    print("\033[90m"+datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
          "\033[0m" + " " +
          string, end=end)


client.run(TOKEN)
