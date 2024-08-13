import disnake
from disnake.ext import commands
from database.sql import add_to_db

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pause", description="Поставить радио на паузу")
    async def pause(self, ctx):
        add_to_db(ctx.guild.id, "off", "off", None)

        player = ctx.guild.voice_client

        if not player:
            embed = disnake.Embed(
                description=f'`Бот не воспроизводит музыку в данный момент`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        if player.is_paused():
            embed = disnake.Embed(
                description=f'`Воспроизведение уже приостановлено`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        player.pause()
        embed = disnake.Embed(
            description=f'`Воспроизведение поставлено на паузу`',
            color=0x8cfff0
        )
        await ctx.send(embed=embed, ephemeral=True)
            
def setup(bot):
    bot.add_cog(Pause(bot))