import discord

from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from dotenv import load_dotenv

from Global import Global

class Help( commands.Cog ):
    def __init__( self, bot: commands.Bot ):
        self.bot = bot
        self.chance = Global.chance
        self.emoji = Global.emoji

    @app_commands.command( name = "help", description = "指令介紹" )
    async def help( self, ctx: discord.Interaction ):
        embed = discord.Embed( title = "抽卡機器人", description = "這是給你們這些抽卡上癮的人專用的", color = discord.Color.dark_green() )
        embed.add_field( name = "目前機率", value = "", inline = False )
        for i in range( len( self.chance ) ):
            embed.add_field( name = self.emoji[i], value = f"{round( self.chance[i] * 100, 1 ) }%", inline = False )
        
        commands = "/draw: 抽10連抽\n/history: 查看自己抽卡歷史紀錄\n/player_data: 查看自己的抽卡統計紀錄\n/sign: 每日簽到\n/check_coins: 查看剩餘點數"
        embed.add_field( name = "指令列表", value = commands, inline = False )
        await ctx.response.send_message( embed = embed )

async def setup( bot ):
    await bot.add_cog( Help( bot ) )
    print( "Help load success" )