import discord
import os

from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from dotenv import load_dotenv

from Backup import Backup
from Global import Global
from Database import Database

class Initial( commands.Cog ):
    def __init__( self, bot: commands.Bot ):
        self.bot = bot

    async def initial( self ):
        await Database.initialize()

    def start_backup( self ):
        Global.scheduler.add_job( Backup.backup, 'interval', minutes = 5, id = 'backup' )
        Global.scheduler.start()

    @commands.Cog.listener()
    async def on_ready( self ):
        await self.initial()
        slash = await self.bot.tree.sync()
        print(f"目前登入身份 --> {self.bot.user}")
        print( f"載入{len( slash )}個斜線指令" )
        for command in slash:
            print( command.name )

async def setup( bot: commands.Bot ):
    await bot.add_cog( Initial( bot ) )
    print( "Initial load success" )