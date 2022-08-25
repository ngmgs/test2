from discord.ext import commands
from os import getenv
import traceback
import discord

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)

    
@bot.command(pass_context=True)
async def kickem(ctx):
    server=ctx.message.server
    for member in tuple(server.members):
        if len(member.roles)==1:
            await bot.kick(member)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
