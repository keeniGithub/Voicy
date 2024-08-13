import disnake
from disnake.ext import commands
from disnake import FFmpegPCMAudio
from list.radio import select_radio, radio_list
from database.sql import add_to_db, update_in_db
import config

class Change(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="change", description="Сменить радио")
    async def change(self, ctx, radio=commands.Param(name="radio", description="Выберите радио из списка", choices=radio_list())): 
        try:
            add_to_db(ctx.guild.id, "off", "off", None)

            guild = ctx.guild
            author = ctx.author
            AppsVC = disnake.utils.get(self.bot.voice_clients, guild = guild) 
            guildVC = guild.voice_client
            
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

                bot_channel = ctx.guild.voice_client

                if bot_channel and bot_channel.channel != channel:
                    embed = disnake.Embed(
                        description=f'`Бот уже подключен к другому каналу`',
                        color=0x8cfff0
                    )

                    await ctx.send(embed=embed, ephemeral=True)
                    return

                FFMPEG_OPTIONS = config.FFMPEG_OPTIONS

                voice_channel = ctx.guild.voice_client
                await voice_channel.disconnect()

                player = await channel.connect()
                
                try:
                    player.play(FFmpegPCMAudio(executable=config.FFMpeg_WIN_path ,source=selected_radio, **FFMPEG_OPTIONS))
                except:
                    player.play(FFmpegPCMAudio(executable=config.FFMpeg_UBUNTU_path ,source=selected_radio, **FFMPEG_OPTIONS))

                embed = disnake.Embed(
                    description=f'`Радио успешно изменено на:` **{radio}**',
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
                description=f'`Не удалось сменить радио`',
                color=0x8cfff0
            )
            await ctx.send(embed=embed, ephemeral=True)
            
def setup(bot):
    bot.add_cog(Change(bot))