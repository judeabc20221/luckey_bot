import discord

from discord import app_commands
from discord.ext import commands

class Custom( commands.Cog ):
    def __init__( self, bot: commands.Bot ):
        self.bot = bot

    def check_if_it_is_owner( ctx: discord.Interaction ):
        if ctx.user.id == 430695428812439562:
            return True
        else:
            return False

    @app_commands.command( name = "status", description = "更改狀態" )
    @app_commands.check( check_if_it_is_owner )
    @app_commands.choices(
        option=[
            app_commands.Choice( name="正在玩", value="playing" ),
            app_commands.Choice( name="正在直播", value="streaming" ),
            app_commands.Choice( name="正在聽", value="listening" ),
            app_commands.Choice( name="正在看", value="watching" )
        ]
    )
    @app_commands.describe( option = "狀態選項", status_str = "狀態文字" )
    async def status( self, interaction: discord.Interaction, option: app_commands.Choice[str], status_str: str ):
        if option.value == "playing":
            await self.bot.change_presence( activity = discord.Game( name = status_str ) )
        elif option.value == "streaming":
            await self.bot.change_presence( activity = discord.Streaming( name = status_str ) )
        elif option.value == "listening":
            await self.bot.change_presence( activity = discord.Activity( type = discord.ActivityType.listening, name = status_str ) )
        elif option.value == "watching":
            await self.bot.change_presence( activity = discord.Activity( type = discord.ActivityType.watching, name = status_str ) )
        else:
            return await interaction.response.send_message( "未修改成功", ephemeral = True )

        return await interaction.response.send_message( "已修改狀態", ephemeral = True )


async def setup( bot ):
    await bot.add_cog( Custom( bot ) )
    print( "Gamble commands load success" )