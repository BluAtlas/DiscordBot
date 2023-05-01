# SwabluBot

Swablu is a discord bot written with the Discord-py Library. It assigns all new users a default role, a random role out of a set of default roles (typically used to assign random colors to users), and changes the user's nickname to a 𝕗𝕒𝕟𝕔𝕪 𝕥𝕖𝕩𝕥 version. Swablu also scrapes r/gamedeals for free games and posts them as embeds in an assigned channel.

## Setup

Install python. You will need a Discord server, a Discord Bot, and a Reddit Bot.

Replace information as described in each file:

```txt
./myRedditBot/redditBot.py
./myservers/server.py
./mytokens/discordToken.py
```

Run the bot with `./run.sh` on linux or `run.bat` on windows.

## Credits

The [nauct](https://github.com/nasyxx/nautc) library is used to convert text into 𝕗𝕒𝕟𝕔𝕪 𝕥𝕖𝕩𝕥.
