import disnake
from disnake.ext import commands
from disnake import FFmpegPCMAudio
from disnake import Option
from list.radio import select_radio, radio_list
from database.sql import add_to_db, update_in_db
import config

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="join", description="Подключить бота к голосовому каналу")
    async def join(self, ctx, radio=commands.Param(name="radio", description="Выберите радио из списка", choices=radio_list())):
        try:
            add_to_db(ctx.guild.id, "off", "off", None)
            selected_radio = select_radio(radio)

            if selected_radio is None:
                embed = disnake.Embed(
                    description=f'`Такого радио пока что нету. Выберите радио из списка`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
                return
            
            channel = ctx.author.voice.channel

            if channel:
                permissions = channel.permissions_for(ctx.guild.me)

                if not permissions.connect:
                    embed = disnake.Embed(
                        description=f'`У меня нет прав на подключение к этому каналу`',
                        color=0x8cfff0
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    return
                
                if not permissions.speak:
                    embed = disnake.Embed(
                        description=f'`У меня нет прав говорить в этом канале`',
                        color=0x8cfff0
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    return
                
                if channel.user_limit <= len(channel.members) and channel.user_limit != 0:
                    embed = disnake.Embed(
                        description=f'`Канал уже полон`',
                        color=0x8cfff0
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    return
                
                channel = ctx.author.voice.channel
                bot_channel = ctx.guild.voice_client

                if bot_channel and bot_channel.channel != channel:
                    embed = disnake.Embed(
                        description=f'`Я уже подключен к другому каналу`',
                        color=0x8cfff0
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    return

                if channel and bot_channel and channel == bot_channel.channel:
                    embed = disnake.Embed(
                        description=f'`Вы уже подключенны в канале с ботом. Для того чтобы сменить радио воспользуйтесь `/change`',
                        color=0x8cfff0
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    return
                
                FFMPEG_OPTIONS = config.FFMPEG_OPTIONS
                player = await channel.connect()

                try:
                    player.play(FFmpegPCMAudio(executable=config.FFMpeg_WIN_path ,source=selected_radio, **FFMPEG_OPTIONS))
                except:
                    player.play(FFmpegPCMAudio(executable=config.FFMpeg_UBUNTU_path ,source=selected_radio, **FFMPEG_OPTIONS))
                    
                embed = disnake.Embed(
                    description=f'`Бот подключился к каналу`\n\n`Выбранное радио:` **{radio}**',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
                update_in_db(ctx.guild.id, "play_song", radio)
                
            else:
                embed = disnake.Embed(
                    description=f'`Вы должны быть подключены к голосовому каналу`',
                    color=0x8cfff0
                )
                await ctx.send(embed=embed, ephemeral=True)
        except:
            embed = disnake.Embed(
                description=f'`Не удалось подключиться к каналу`',
                color=0x8cfff0
            )

            await ctx.send(embed=embed, ephemeral=True)
            
def setup(bot):
    bot.add_cog(Join(bot))