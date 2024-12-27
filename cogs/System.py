import discord
import pytz

from datetime import time, datetime
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import Choice

from Global import Global
from Backup import Backup
from Player import Player

class System( commands.Cog ):
    @commands.Cog.listener()
    # 被中斷 備份所有伺服器資料
    async def on_shutdown( self ):
        # Backup.backup()
        None

    @commands.Cog.listener()
    async def on_disconnect( self ):
        # Backup.backup()
        None

async def setup( bot ):
    await bot.add_cog( System( bot ) )
    print( "System listener load success" )