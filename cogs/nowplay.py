import disnake
from disnake.ext import commands
from database.sql import add_to_db, select_from_db

class Now_play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="nowplay", description="Сейчас играет...")
    async def nowplay(self, ctx):
        try:
            add_to_db(ctx.guild.id, "off", "off", None)
            play_song = select_from_db(ctx.guild.id, "play_song")

            if play_song is None:
                embed = disnake.Embed(
                    description=f'`В данный момент ничего не проигрываеться`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
                return
            
            voice_channel = ctx.guild.voice_client

            if voice_channel:
                embed = disnake.Embed(
                    description=f'`Сейчас играет:` **{play_song}**',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = disnake.Embed(
                    description=f'`Бот не подключен к голосовому каналу`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)

        except:
            embed = disnake.Embed(
                description=f'`В данный момент ничего не проигрываеться`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Now_play(bot))