import disnake
from disnake.ext import commands

class Tribune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def tribune(self, ctx: disnake.AppCmdInter, before, after):   
        user = await ctx.guild.fetch_member(ctx.id) # Получение данных о ползователе                                    #type:ignore
        app = await ctx.guild.fetch_member(self.bot.user.id) # Получение данных о боте                                       #type:ignore
        # ========================================================================= Провека взаимодействия с приложением
        if user.id == app.id:
            # try:
                # =================================================================== Приложение есть в голосовом канале
            UserVC = user.voice.channel                                                                             #type:ignore
            if UserVC:
                if (app.voice.suppress == True or app.voice.mute == False):                                         #type:ignore
                    # =================================================================================== Переменные
                    Perm = app.voice.channel.permissions_for(app.guild)                                  #type:ignore
                    VoiceBot = disnake.utils.get(UserVC.members, id = self.bot.user.id)
                    # ================================================== Проверка прав подключатся в голосовой канал
                    if Perm.connect:
                        # =============================================================== Бот не выступает в турбине
                        if app.voice.suppress == True:                                                              #type:ignore
                            # ===================================================== Провека прав выступать в турбине
                            if Perm.speak: 
                                await VoiceBot.edit(suppress = False)                                               #type:ignore
                        # ========================================================================== Бот не заглушен
                        if (app.voice.deaf == False or app.voice.self_deaf == False):                               #type:ignore
                            # ==================================================== Провека прав заглушать участников
                            if Perm.deafen_members:
                                await VoiceBot.edit(deafen = True)                                                  #type:ignore
                            # =================================================== Бот отключит звук у себя в клиенте
                            await app.guild.change_voice_state(channel = UserVC, self_deaf = True)
            # except:
            #     pass

def setup(bot):
    bot.add_cog(Tribune(bot))
