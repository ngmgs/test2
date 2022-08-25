import discord
from discord.ext import commands

bot=commands.Bot(command_prefix='!')


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


bot.run('DISCORD_BOT_TOKEN')
