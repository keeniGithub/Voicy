import disnake 
from disnake.ext import commands, tasks
from disnake import Activity, ActivityType
import os
import config
from database.sql import *
import platform

intents = disnake.Intents.default()
intents.voice_states = True

TOKEN = config.TOKEN

bot = commands.Bot(command_prefix=None, intents=intents, reload=True)

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

for filename in os.listdir(config.cogs_path):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready() -> None:
    print(f"Бот {bot.user} успешно запущен в версии {config.ver}")
    await bot.change_presence(status=disnake.Status.idle,activity=Activity(name=config.Activity,  type=ActivityType.listening))

@bot.event
async def on_button_click(interaction: disnake.MessageInteraction):
    guild = interaction.guild

    if interaction.component.custom_id == "always_status":
        always = select_from_db(guild.id, "always")

        if always == "on":
            update_in_db(guild.id, "always", "off")

            embed = disnake.Embed(
                description=f'Статус 24/7 был выключен ⛔',
                color=0x8cfff0
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif always == "off":
            update_in_db(guild.id, "always", "on")

            embed = disnake.Embed(
                description=f'Статус 24/7 был включен ✅',
                color=0x8cfff0
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

# if platform.system() != "Windows": TOKEN = config.TOKEN
bot.run(TOKEN)