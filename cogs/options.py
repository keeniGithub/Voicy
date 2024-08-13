import disnake
from disnake.ext import commands
from database.sql import add_to_db, select_from_db

class Options(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="options", description="Открыть найстройки бота на сервере")
    @commands.has_permissions(administrator=True)
    async def options(self, ctx):
        guild = ctx.guild

        add_to_db(ctx.guild.id, "off", "off", None)

        always = select_from_db(guild.id, "always")
        
        if always == "on": always = f"Включенно ✅"
        elif always == "off": always = f"Выключенно ⛔"

        embed = disnake.Embed(
            title=f'**{guild.name}**',
            color=0x8cfff0
        )

        embed.add_field(name="ID Сервера", value=f"{guild.id}", inline=False)
        embed.add_field(name="24/7", value=f"{always}", inline=False)

        button_row = disnake.ui.ActionRow(
        disnake.ui.Button(style=disnake.ButtonStyle.primary, label="24/7", custom_id="always_status"),
        disnake.ui.Button(style=disnake.ButtonStyle.url, label="Voicy Community", url="https://discord.com/invite/4ed6dbJZvZ")
        )

        await ctx.send(embed=embed, ephemeral=True, components=button_row)
    
def setup(bot):
    bot.add_cog(Options(bot))