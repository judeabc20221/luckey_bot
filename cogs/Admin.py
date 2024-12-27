import discord

from datetime import date
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from Global import Global
from Backup import Backup
from Database import Database

from dotenv import load_dotenv, set_key
import os

class Admin( commands.Cog ):
    def __init__( self, bot: commands.Bot ):
        self.bot = bot
        self.chance = Global.chance
        self.emoji = Global.emoji

    def check_if_it_is_owner( ctx: discord.Interaction ):
        if ctx.user.id == 430695428812439562:
            return True
        else:
            return False

    @app_commands.command( name = "check_one_player_data", description = "查看一個人的抽卡紀錄" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( player = "玩家" )
    async def check_one_player_data( self, ctx: discord.Interaction, player: discord.Member ):
        user_id = player.id
        if await Database.get_player( user_id ) is None:
            await ctx.response.send_message( "他還未抽卡過", ephemeral = True )
            return

        embed = discord.Embed( title = "抽卡紀錄", color = discord.Color.dark_green() )
        url = ""
        if ctx.user.avatar:
            url = player.avatar.url
        embed.set_author( name = player.name, icon_url = url )
        history = await Database.get_gamble_history( user_id )
        for i in range( len( self.chance ) ):
            embed.add_field( name = self.emoji[i], value = history[i], inline = True )

        embed.add_field( name = "總抽卡次數", value = await Database.get_gamble_times( user_id ), inline = False )
        embed.add_field( name = "剩餘點數", value = await Database.get_coins( user_id ), inline = True )

        today = date.today()
        if await Database.get_signed_time( user_id ) is None or await Database.get_signed_time( user_id ) != today:
            embed.add_field( name = "今日是否簽到", value = "否", inline = True )
        else:
            embed.add_field( name = "今日是否簽到", value = "是", inline = True )
        await ctx.response.send_message( embed = embed )



    @app_commands.command( name = "set_up_role", description = "設定抽卡身分組" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( role = "身分組" )
    async def set_up_role( self, ctx: discord.Interaction, role: discord.Role ):
        Global.gamble_role = role.id
        load_dotenv()
        set_key(".env", "role", str( role.id ) )
        await ctx.response.send_message( "身分組設定完成", ephemeral = True )

    @app_commands.command( name = "set_up_channel", description = "設定抽卡頻道" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( channel = "頻道" )
    async def set_up_channel( self, ctx: discord.Interaction, channel: discord.TextChannel ):
        Global.gamble_channel = channel.id
        load_dotenv()
        set_key(".env", "channel", str( channel.id ) )
        await ctx.response.send_message( "頻道設定完成", ephemeral = True )

    @app_commands.command( name = "reload", description = "重新讀取指令" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( command = "檔案名稱" )
    async def reload( self, ctx: discord.Interaction, command: str ):
        ext = command
        await self.bot.reload_extension(f'cogs.{ext}')
        await ctx.response.send_message( f'{ext} reloaded successfully.', ephemeral = True )

    @app_commands.command( name = "add_coins", description = "手動新增點數" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( player = "玩家", coins = "新增多少點數" )
    async def add_coins( self, ctx: discord.Interaction, player: discord.Member, coins: int ):
        if await Database.get_player( player.id ):
            await Database.update_coins( player.id, coins )
            await ctx.response.send_message( f"已為{player.mention}新增{coins}點，目前他總共有{await Database.get_coins( player.id )}點", ephemeral = False )
        else:
            await ctx.response.send_message( "未找到玩家", ephemeral = True )

    @app_commands.command( name = "database", description = "修改資料庫" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( query = "指令", parameter = "參數" )
    async def database( self, ctx: discord.Interaction, query: str, parameter: str ):
        par = parameter.split( "," )
        params = [param.strip() for param in par]

        for i in range( len( params ) ):
            if params[i].isdigit():
                params[i] = int( params[i] )

        result = await Database.execute_update( query, params )
        if result == "True":
            await ctx.response.send_message( "指令執行成功", ephemeral = True )
        else:
            await ctx.response.send_message( f"執行失敗:\n{result}", ephemeral = True )

    @app_commands.command( name = "update_history", description = "修改歷史紀錄" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.describe( history = "歷史紀錄", player_id = "id" )
    async def update_history( self, ctx: discord.Interaction, history: str, player_id: str ) :
        par = history.split( "," )
        params = [param.strip() for param in par]
        for i in range( len( params ) ):
            if params[i].isdigit():
                params[i] = int( params[i] )

        player_id = int( player_id )

        result = await Database.manual_update_history( params, player_id )
        if result == "True":
            await ctx.response.send_message( "指令執行成功", ephemeral = True )
        else:
            await ctx.response.send_message( f"執行失敗:\n{result}", ephemeral = True )

    @commands.command()
    async def shutdown( self, ctx: commands.Context ):
        if ctx.author.id != 430695428812439562:
            return
        await self.bot.close()

    @commands.command()
    async def post( self, ctx: commands.Context ):
        if ctx.author.id != 430695428812439562:
            return

        channel = self.bot.get_channel( Global.gamble_channel )
        if channel is not None:
            message = ctx.message.content[6:]
            embed = discord.Embed( title = "公告", color = discord.Color.dark_green(), description = message )
            embed.set_thumbnail( url = "https://imgur.com/NZPuXqX.png" )
            await channel.send( embed = embed )

    @check_one_player_data.error
    @set_up_role.error
    @set_up_channel.error
    @reload.error
    @add_coins.error
    async def error( self, ctx: discord.Interaction, error: Exception ):
        print( error )
        await ctx.response.send_message( "不要亂用指令:rage:", ephemeral = True )


async def setup( bot ):
    await bot.add_cog( Admin( bot ) )
    print( "Admin commands load success" )