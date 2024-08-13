import disnake
from disnake.ext import commands
from database.sql import add_to_db

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="leave", description="Отключить бота из голосового канала")
    async def leave(self, ctx):
        add_to_db(ctx.guild.id, "off", "off", None)

        voice_channel = ctx.guild.voice_client
        channel = ctx.author.voice

        if voice_channel:
            if channel:
                await voice_channel.disconnect()
                embed = disnake.Embed(
                    description=f'`Бот покинул канал`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = disnake.Embed(
                    description=f'`Вы должны находиться в канале чтобы отключить бота`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(
                description=f'`Бот не подключен к голосовому каналу`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Leave(bot))