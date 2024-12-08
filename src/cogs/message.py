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
            title="gracias por mencionarme",
            description=">>> mi prefijo es 's!', pero si te sientes mas comodo puedes usar los slash commands '/' para interactuar conmigo\npara ver mis comandos puedes usar 's!help' o  '/help'\n si quieres apoyarme puedes hacerlo en [github Sponsor](https://github.com/sponsors/Evergaster)",
            color=discord.Color.red()
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        if self.client.user in message.mentions:
            await message.channel.send(embed=self.embedMention)

        if not message.content.lower().startswith(self.prefix):
            return

        ctx = await self.client.get_context(message)
        if ctx.command is None:
            self.embed.description = f"> El comando **{self.prefix}{ctx.invoked_with}** no se ha podido encontrar"
            await ctx.send(embed=self.embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle other command errors if necessary
        pass


async def setup(bot):
    await bot.add_cog(Msg(bot))
    print("Base de SaRa cargando")