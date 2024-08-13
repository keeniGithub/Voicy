import disnake
from disnake.ext import commands
from database.sql import add_to_db

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="resume", description="Продолжить воспроизведения")
    async def resume(self, ctx):
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
                description=f'`Воспроизведение не приостановлено`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        player.resume()
        embed = disnake.Embed(
            description=f'`Воспроизведение возабновлено`',
            color=0x8cfff0
        )
        await ctx.send(embed=embed, ephemeral=True)

            
def setup(bot):
    bot.add_cog(Resume(bot))