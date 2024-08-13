import disnake
from disnake.ext import commands
from database.sql import add_to_db, select_from_db

class Always(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        add_to_db(member.guild.id, "off", "off", None)

        if member.bot:
            return

        voice_channel = before.channel or after.channel
        if not voice_channel:
            return

        users_in_channel = len(voice_channel.members)
        if users_in_channel == 1:

            if users_in_channel == 2:
                return
            
            guild = member.guild

            always = select_from_db(guild.id, "always")

            if always == "on": pass
            elif always == "off":
                try:
                    voice_client = guild.voice_client
                    await voice_client.disconnect()
                except:
                    pass


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
    bot.add_cog(Always(bot))
