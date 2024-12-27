import discord
import asyncio
import json
import os


from typing import Optional
from discord.ext import commands
from discord.app_commands import Choice
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot( command_prefix="=", intents=intents )
async def load():
    load_dotenv()
    # 將指令輸入進去
    for filename in os.listdir( "./cogs" ):
        if filename.endswith( "py" ):
            await bot.load_extension( f'cogs.{filename[:-3]}' )

asyncio.run( load() )
bot.run("MTMwNDQ5NDg3NjI2NzY0NzAxNw.Gg2VIv.5_GBsyu8vCZtK2CmnOAiZ-VrqnNPeker6lP28M")