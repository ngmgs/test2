# botのライブラリをimport
import discord
from mastodon import Mastodon, StreamListener

# threading.Threadをimoprt
from threading import Thread

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    

# discord botの起動
job = Thread(target=discord_client.run, args=(DISCORD_BOT_TOKEN,))
job.start()

# mastodon bot の起動
job = Thread(target=mstdn.stream_user, args=(MstdnStreamListener(),))
job.start()
