import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Msg(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = os.getenv('PREFIX').lower()
        self.embed = discord.Embed(
            title="Comando no encontrado",
            color=discord.Color.red()
        )
        self.embed.set_footer(text="SaRa client")

        self.embedMention = discord.Embed(
            title="Gracias por mencionarme",
            description=">>> Mi prefijo es 's!', pero si te sientes más cómodo puedes usar los slash commands '/' para interactuar conmigo\nPara ver mis comandos puedes usar 's!help' o  '/help'\nSi quieres apoyarme puedes hacerlo en [GitHub Sponsor](https://github.com/sponsors/Evergaster)",
            color=discord.Color.red()
        )

        self.last_sent = None  # Inicializar last_sent
    
    

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        if self.client.user in message.mentions:
            await message.channel.send(embed=self.embedMention)

        # Convertir el mensaje a minúsculas y verificar el prefijo
        if not message.content.lower().startswith(self.prefix):
            return

        # Comando válido, obtener el contexto
        ctx = await self.client.get_context(message)
        if ctx.command is None:
            self.embed.description = f"> El comando **{self.prefix}{ctx.invoked_with}** no se ha podido encontrar"
            await ctx.send(embed=self.embed)
        else:
            await self.send_reminder(ctx.channel)

    async def send_reminder(self, channel):
        current_time = discord.utils.utcnow()

        # tiempo 3600 segundos osea 1 hora
        if self.last_sent is None or (current_time - self.last_sent).total_seconds() > 3600:
            await channel.send("Recuerda que puedes apoyar el proyecto en [GitHub Sponsor](https://github.com/sponsors/Evergaster)")
            self.last_sent = current_time

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Manejar otros errores de comandos si es necesario
        pass

async def setup(bot):
    await bot.add_cog(Msg(bot))
    print("Base de SaRa cargando")