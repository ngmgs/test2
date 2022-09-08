import discord
import traceback
import re
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
is_text = {}

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
async def norole(ctx):  # guildオブジェクトを渡してください
    guild = bot.guilds[0]
    role = discord.utils.get(guild.roles, name="kagi")
    norolemember = [i for i in guild.members]
    for i in norolemember:
        try:
            await ctx.send(i)
            await i.remove_roles(role, atomic=True)
        except discord.Forbidden:
            print("権限が足りません")

@bot.command()
async def everyone(ctx):
    guild = bot.guilds[0]
    channel_sent2 = bot.get_channel(1012928069402636390)
    role = discord.utils.get(guild.roles, name="@everyone")
    await channel_sent2.set_permissions(role, read_messages=False)

@bot.command()
async def ping(ctx):
    await ctx.send(discord.__version__)

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, reason):
    await member.kick(reason=reason)
    embed = discord.Embed(title="KICK", color=0xff0000)
    embed.add_field(name="メンバー", value=f"{member.mention}", inline=False)
    embed.add_field(name="理由", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    await _check_url(message)

async def _check_url(message: discord.Message):
    role = discord.utils.get(message.guild.roles, name="kagi")
    member = message.author
    pattern = pattern = re.compile(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")


    if message.author.bot:
        return
    # メッセージからURLを抽出
    url_list = re.findall(pattern, message.content)
    # もしメッセージにURLが含まれていたら
    if url_list:
        print("#" * 50)
        print("1時間以内に同じURLを送信したら削除する")
        # もし辞書にURLが登録されていたら(含まれていなかったらNoneが返る)
        if is_text.get(url_list[0], None) is not None:
            # 送信されていた時間を取り出す
            _sent_date = is_text[url_list[0]]
            print("辞書に登録されている発言時間は" + str(_sent_date))
            # もし差分が3600秒以上(1h)なら
            if (datetime.now() - _sent_date).seconds >= 3600:
                # 辞書のURLが持つ発言時間を更新して終了
                print("辞書のURL(" + url_list[0] + ")が持つ発言時間を更新")
                is_text[url_list[0]] = datetime.now()
            else:
                # 1h以内に投稿されていた場合削除
                print(url_list[0])
                print("そのURL(" + url_list[0] + ")が入ったメッセージが1時間以内に投稿されています。削除します。")
                alert_msg = await message.channel.send("そのURLが入ったメッセージが1時間以内に投稿されています。削除します。")
                await message.delete(delay=1)
                await alert_msg.delete(delay=3)
                return
        else:
            # 辞書にURLが登録されていなかったのでURLと発言時間を登録する
            print("辞書にURLと発言時間を登録")
            is_text[url_list[0]] = datetime.now()
            print(is_text)
    else:
        print("メッセージにURLはない")
        
    # 発言したメンバーに役職kagiを付与
    await member.add_roles(role, atomic=True)

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


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
    if now == 'Saturday/04:01':
        await channel_sent.send(now + "全員のkagi権限削除")
        role = discord.utils.get(guild.roles, name="kagi")
        norolemember = [i for i in guild.members]
        for i in norolemember:
            try:
                await i.remove_roles(role, atomic=True)
            except discord.Forbidden:
                print("権限が足りません")

        await channel_sent.send(now + "鍵部屋をプライベート解除")
        channel_sent2 = bot.get_channel(1012928069402636390)
        role2 = discord.utils.get(guild.roles, name="@everyone")
        await channel_sent2.set_permissions(role2, read_messages=True)

    if now == 'Tuesday/04:01':
        await channel_sent.send(now + "鍵部屋をプライベート化")
        channel_sent2 = bot.get_channel(1012928069402636390)
        role2 = discord.utils.get(guild.roles, name="@everyone")
        await channel_sent2.set_permissions(role2, read_messages=False)

@bot.event
async def on_ready():
    guild = bot.guilds[0]
    norolemember = [i for i in guild.members]  # 全てのメンバー
    norolemember2 = [i for i in guild.members if len(i.roles) == 1]  # 役職が一つ（everyoneのみ）のメンバー
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

    global channel_sent
    channel_sent = bot.get_channel(1012237139729199136)
    send_message_every_10sec.start()  # 定期実行するメソッドの後ろに.start()をつける

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
