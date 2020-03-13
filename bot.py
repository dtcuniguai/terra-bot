import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BTOKEN')
prefix = os.getenv('BPREFIX')

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print('-------------------Terrar-Bot-----------------------')
    print(f'Bot Token  :  {token}')
    print(f'Bot Prefix :  {prefix}')
    print('----------------------------------------------------')
    print('>>Terra Bot is online !!!!!')


@bot.command()
async def network(ctx, arg):
    print(arg)
    await ctx.send(f'{bot.latency*1000}(ms)')

@bot.command()
async def item(ctx, arg):
    info = 'you are lookong for this item \n'
    info += 'hellow workd\n'
    info += arg
    await ctx.send(info)

bot.run(token)