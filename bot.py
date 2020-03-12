import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix=os.getenv('BPREFIX'))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('>> Bot is online')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(687240776828190730)
    await channel.send("hihi")

@bot.command()
async def network(ctx):
    await ctx.send(f'{bot.latency*1000}(ms)')

print(os.getenv('BTOKEN'))
bot.run(os.getenv('BTOKEN'))