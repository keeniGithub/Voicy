import disnake
from disnake.ext import commands
from list.radio import radio_list
from database.sql import add_to_db

class List(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="list", description="Список всех доступных радио")
    async def list(self, ctx): 
        add_to_db(ctx.guild.id, "off", "off", None)

        embed = disnake.Embed(
            title='Все доступные радио:',
            description=f'`{radio_list()}`',
            color=0x8cfff0
        )

        await ctx.send(embed=embed, ephemeral=True)
            
def setup(bot):
    bot.add_cog(List(bot))