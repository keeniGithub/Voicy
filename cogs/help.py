import disnake
from disnake.ext import commands
from database.sql import add_to_db
import config

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Информация о боте")
    async def help(self, ctx): 
        add_to_db(ctx.guild.id, "off", "off", None)

        version = config.ver

        embed = disnake.Embed(
            title='Информация',
            description=f'''
**Основное**

> Серверов: **{len(self.bot.guilds)}** 
> Версия: **{version}**

**Команды**

> `/join` - Подключить бота к голосовому каналу
> `/change` - Сменить радио
> `/nowplay` - Узнать что сейчас играет
> `/leave` - Отключить бота из голосового канала
> `/pause` - Поставить воспроизведения на паузу
> `/resume` - Продолжить воспроизведения
> `/options` - Настройки бота
> `/help` - Вы сейчас тут находитесь

**Партнеры**

> [Radio KetaRu](https://live.ketaru.com/) - Радиостанция, Discord бот, веб приложения и многое другое

**Ссылки**

> [Сайт](https://voicy.site/)
> [Документация](https://voicy.site/documentations)
> [Добавить на сервер](https://discord.com/oauth2/authorize?client_id=1105500733333315644&permissions=3409920&integration_type=0&scope=bot)
> [Донат](https://www.donationalerts.com/r/voicycommunity)

**Мониторинги**

> [TopGG](https://top.gg/bot/1105500733333315644)
> [DiscordBotList](https://discord.ly/voicy)
> [BotiCord](https://boticord.top/bot/1105500733333315644)
''',
            color=0x8cfff0
        )

        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Help(bot))