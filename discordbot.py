import discord
import traceback
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time


bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
           

@bot.event
async def on_ready():
    guild = bot.guilds[0]
    norolemember = [i for i in guild.members]
    norolemember2 = [i for i in guild.members if len(i.roles) == 1]
    print("on_ready")
    print(discord.__version__)
    print(norolemember)
    for item in norolemember:
        print(item)       
   
    print("on_ready")
    print(discord.__version__)
    print(norolemember2)
    for item in norolemember2:
        print(item)     
        
        
@bot.command()
async def test(ctx):
    guild = bot.guilds[0]
    norolemember = [i for i in guild.members]
    norolemember2 = [i for i in guild.members if len(i.roles) == 1]

    for item in norolemember:
        await ctx.send(item)
    
    await ctx.send(discord.__version__)
    
    for item in norolemember2:
        await ctx.send(item)          
        await item.kick()         
        
@bot.command()
async def tes(ctx):
    guild = bot.guilds[0]
    norolemember = [i for i in guild.members]
    norolemember2 = [i for i in guild.members if len(i.roles) == 2]

    for item in norolemember:
        await ctx.send(item)
    
    await ctx.send(discord.__version__)
    
    for item in norolemember2:
        await ctx.send(item)    
      
       
@bot.command()    
async def norole(ctx): #guildオブジェクトを渡してください
    guild = bot.guilds[0]
    role = discord.utils.get(guild.roles, name = "kagi")
    norolemember = [i for i in guild.members]
    for i in norolemember:
        try:
            await ctx.send(i)
            await i.remove_roles(role, atomic=True)    
        except discord.Forbidden:
            print("権限が足りません")


@bot.event
async def on_message(message):
    words=['https']
    words2=['remove']       
    member = message.author    
    role = discord.utils.get(message.guild.roles, name = "kagi")
    for word in words:
        if word in message.content:
            print(member)   
            print(role)
            await member.add_roles(role, atomic=True)
            
    for word in words2:
        if word in message.content:
            print(member)   
            print(role)
            await member.remove_roles(role, atomic=True)   

    await bot.process_commands(message)


channel_sent = None
@tasks.loop(
    time=time(
        hour=4, minute=1,
        tzinfo=timezone(
            timedelta(hours=9)
        )
    )
)
async def send_message_every_10sec():         
    guild = bot.guilds[0]
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST).strftime('%A/%H:%M')
    await channel_sent.send(now)    
    if now == 'Saturday/04:00':
        await channel_sent.send(now + "全員のkagi権限削除")        
        role = discord.utils.get(guild.roles, name = "kagi")
        norolemember = [i for i in guild.members]
        for i in norolemember:
            try:
                await i.remove_roles(role, atomic=True)    
            except discord.Forbidden:
                print("権限が足りません")
           
        await channel_sent.send(now + "鍵部屋をプライベート解除")                      
        channel_sent2 = bot.get_channel(1012928069402636390)
        role2 = discord.utils.get(guild.roles, name = "@everyone")
        await channel_sent2.set_permissions(role2, read_messages=True)
           
    if now == 'Tuesday/04:00': 
        await channel_sent.send(now + "鍵部屋をプライベート化")
        channel_sent2 = bot.get_channel(1012928069402636390)
        role2 = discord.utils.get(guild.roles, name = "@everyone")
        await channel_sent2.set_permissions(role2, read_messages=False)

           
@bot.event
async def on_ready():
    global channel_sent 
    channel_sent = bot.get_channel(1012237139729199136)
    send_message_every_10sec.start() #定期実行するメソッドの後ろに.start()をつける


@bot.command()    
async def everyone(ctx): 
    guild = bot.guilds[0]
    channel_sent2 = bot.get_channel(1012928069402636390)
    role = discord.utils.get(guild.roles, name = "@everyone")
    await channel_sent2.set_permissions(role, read_messages=False)








@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    

@bot.command()
async def ping(ctx):
    await ctx.send(discord.__version__)
    
    
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member, reason):
   await member.kick(reason=reason)
   embed=discord.Embed(title="KICK", color=0xff0000)
   embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
   embed.add_field(name="理由", value=f"{reason}", inline=False)
   await ctx.send(embed=embed)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
