import discord
import json
import random

from datetime import date, datetime
from asyncio import Lock
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from Player import Player
from Global import Global
from Database import Database

class Gamble( commands.Cog ):
    def __init__( self, bot: commands.Bot ):
        self.bot = bot
        # 機率
        self.chance = Global.chance
        # 輸出的emoji
        self.emoji = Global.emoji
        # 用戶 ID 對應的鎖
        self.locks = {}

    def once_draw( self ):
        num = random.random()
        # 機率用累加的
        chance_count = 0.0
        for i in range( len( self.chance ) ):
            chance_count += self.chance[i]
            if num < chance_count:
                return i

        # 真的跑到這裡的話 你是歐皇...
        return len( self.chance ) - 1

    async def get_ten_draw( self, player_id: int ):
        await Database.update_gamble_times( player_id, 10 )
        data = []
        for i in range( 10 ):
            # 記錄一次抽卡結果
            data.append( self.once_draw() )

        return data

    async def get_user_lock(self, user_id):
        """取得對應用戶的鎖，如果不存在則創建"""
        if user_id not in self.locks:
            self.locks[user_id] = Lock()
        return self.locks[user_id]

    # 每日簽到
    @app_commands.command( name = "sign", description = "每日簽到" )
    async def sign( self, ctx: discord.Interaction ):
        user_id = ctx.user.id
        last_signed_time = await Database.get_signed_time( user_id )
        if await Database.get_player( user_id ) is None:
            await Database.add_player( user_id, ctx.user.name )

        today = date.today()

        if last_signed_time is None or last_signed_time < today:
            await Database.update_sign_time( user_id )
            await Database.update_coins( user_id, 100 )
            await ctx.response.send_message( f"已簽到完成，目前硬幣持有數：{await Database.get_coins( user_id )}", ephemeral = True )
        else:
            await ctx.response.send_message( "你今天已簽到過", ephemeral = True )


    # 差看目前點數
    @app_commands.command( name = "check_coins", description = "查看目前還有多少點數" )
    async def check_coins( self, ctx: discord.Interaction ):
        await ctx.response.send_message( f"你還剩{ await Database.get_coins( ctx.user.id ) }點", ephemeral = True )

    # 抽卡
    @app_commands.command( name = "draw", description = "來看看你的運氣吧" )
    async def draw( self, ctx: discord.Interaction ):
        user_id = ctx.user.id
        user_name = ctx.user.name

        # 獲取用戶的鎖，避免競態條件
        user_lock = await self.get_user_lock( user_id )
        async with user_lock:
            coins = await Database.get_coins( user_id )

            if coins < 10:
                await ctx.response.send_message( f"剩餘點數不足10點，你目前只有{coins}點", ephemeral = True )
                return
            await Database.update_coins( user_id, -10 )
            # 紀錄本次抽卡結果
            data = await self.get_ten_draw( user_id )
            await Database.update_gamble_history( user_id, data )
            output = ""
            for i in data:
                output += self.emoji[ i ]

            embed = discord.Embed( color = discord.Color.dark_green() )
            url = ""
            if ctx.user.avatar:
                url = ctx.user.avatar.url
            embed.set_author( name = user_name, icon_url = url )
            embed.add_field( name = "抽卡結果", value = output, inline = False )

            await ctx.response.send_message( embed = embed )

    @app_commands.command( name = "player_data", description = "查看個人抽卡統計紀錄" )
    async def player_data( self, ctx: discord.Interaction ):
        user_id = ctx.user.id
        user = await Database.get_player( user_id )
        if user is None:
            await ctx.response.send_message( "你還未抽卡過", ephemeral = True )
            return

        if await Database.get_gamble_times( user_id ) == 0:
            await ctx.response.send_message( "你還未抽卡過", ephemeral = True )

        embed = discord.Embed( title = "抽卡紀錄", color = discord.Color.dark_green() )
        url = ""
        if ctx.user.avatar:
            url = ctx.user.avatar.url
        embed.set_author( name = ctx.user.name, icon_url = url )

        history = await Database.get_gamble_history( user_id )

        if history:
            for i in range( len( self.chance ) ):
                embed.add_field( name = self.emoji[i], value = history[i], inline = True )
        else:
            for i in range( len( self.chance ) ):
                embed.add_field( name = self.emoji[i], value = 0, inline = True )

        embed.add_field( name = "總抽卡次數", value = await Database.get_gamble_times( user_id ), inline = False )
        embed.add_field( name = "剩餘點數", value = await Database.get_coins( user_id ), inline = True )

        today = date.today()
        if await Database.get_signed_time( user_id ) is None or await Database.get_signed_time( user_id ) != today:
            embed.add_field( name = "今日是否簽到", value = "否", inline = True )
        else:
            embed.add_field( name = "今日是否簽到", value = "是", inline = True )
        await ctx.response.send_message( embed = embed )

    @draw.error
    @player_data.error
    async def error( self, ctx: discord.Interaction, error: Exception ):
        if isinstance( error, discord.app_commands.errors.MissingRole ):
            print( error )
            await ctx.response.send_message( "沒有身分組執行這個指令", ephemeral = True )
        else:
            await ctx.response.send_message(f"發生錯誤: {error}", ephemeral = True )


async def setup( bot ):
    await bot.add_cog( Gamble( bot ) )
    print( "Gamble commands load success" )