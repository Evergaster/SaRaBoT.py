import discord
from discord.ext import commands
from discord.ui import Select, View, Button
import datetime
import psutil
from discord import app_commands, Interaction
#para ejecutar codigo
import io
import contextlib
import traceback
import textwrap
import re
import asyncio

def formatDate(template, date=None):
    specs = ["YYYY", "MM", "DD", "HH", "mm", "ss"]
    
    if not date:
        date = datetime.datetime.now() + datetime.timedelta(minutes=datetime.datetime.utcnow().utcoffset().total_seconds() // 60)
    else:
        date = datetime.datetime.fromisoformat(str(date))
        
    date_parts = [str(date.year), str(date.month).zfill(2), str(date.day).zfill(2),
                  str(date.hour).zfill(2), str(date.minute).zfill(2), str(date.second).zfill(2)]
    
    for i, spec in enumerate(specs):
        template = template.replace(spec, date_parts[i])
    return template

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = {
            "embed1": discord.Embed(
                title="Lista de Comandos",
                description="Elige una categoría para ver más información.\nalgunos comandos aun no estan completo",
                color=discord.Color.blue()
            ).add_field(
                name="nuevas funciones <:emoji_45:919380066507567134> ",
                value="te gusta escribir?, bueno sube tus textos pequeños de menos 256 caracteres para compartirlo con los demas <:emoji_45:919380066507567134> usa los comandos **s!poetext** para ver como funciona o **/poems**"
            ).add_field(
                name="todos las catogrias",
                value=" **nsfw** comandos cochinos :: <:amor:910400150806102056> \n **rol**   comandos para rol :: <:feliz:910400345149149244> \n **menu**  menu principal  :: <:confunsion:910400063371636736> \n **anime** anime e información  :: <:beso:910400208607793152> \n **moderacion** comandos de moderacion  :: <:alex_marin:910400398672662548>",
                inline=False
            ).add_field(
                name="pofin",
                value="<:e0p_lucifer_furry_smug:1056717187131383818> puedes usar los slash command solo pon ``/``"
            ).add_field(
                name="soporte",
                value="si quieres apoyarme puede donar atravez de github\n[github Sponsor](https://github.com/sponsors/EverGasterXd) | [invitacion](https://discord.gg/WnEkPJgtnt) | [pagina web](https://saraowo.github.io/)"
            ).set_image(
                url="https://media.discordapp.net/attachments/935251389330903110/1055575295295496274/Black_Magenta_Gaming_Dynamic_Gaming_Logos_Discord_Profile_Banner_1.gif"
            ),
            "embed2": discord.Embed(
                title="para hacer rol con la gente",
                color=discord.Color.red()
            ).add_field(
                name="comandos sin mencion",
                value="""```
\u200Bs!work    \u200Bs!yandere \u200Bs!stare
\u200Bs!wink    \u200Bs!think   \u200Bs!travel
\u200Bs!teehee  \u200Bs!like    \u200Bs!angry 
\u200Bs!laugh   \u200Bs!dance   \u200Bs!cry 
\u200Bs!bored   \u200Bs!blush   \u200Bs!run 
\u200Bs!sleep```""",
                inline=False
            ).add_field(
                name="comandos con mencion",
                value="""```
\u200Bs!baka    \u200Bs!kiss    \u200Bs!kill
\u200Bs!spank   \u200Bs!punch   \u200Bs!poke```""",
                inline=False
            ).set_image(
                url="https://media.discordapp.net/attachments/935251389330903110/1055577421719552100/rolplay.gif"
            ),
            "embed3": discord.Embed(
                title="para pasar el rato",
                color=discord.Color.red()
            ).add_field(
                name="Comandos para tener nekos",
                value="""```
\u200Bs!girl        \u200Bs!jumbo       \u200Bs!botinfo        
\u200Bs!neko        \u200Bs!foxgirl     \u200Bs!serverinfo
\u200Bs!avatar      \u200Bs!userinfo    \u200Bs!servericon```""",
                inline=False
            ).set_image(
                url="https://media.discordapp.net/attachments/935251389330903110/1055585859094720623/Black_Magenta_Gaming_Dynamic_Gaming_Logos_Discord_Profile_Banner_2_1.gif"
            ),
            "embed4": discord.Embed(
                title="Para tus puercadas",
                color=discord.Color.red()
            ).add_field(
                name="Comandos sin mención",
                value="""```
\u200Bs!pussy   \u200Bs!boobs   \u200Bs!yuri
\u200Bs!ahegao  \u200Bs!lwfoxgirl\u200Bs!hentai 
\u200Bs!uniform \u200Bs!rule34  \u200Bs!yande.re
```""",
                inline=False
            ).add_field(
                name="Comandos con mención",
                value="""```
\u200Bs!anal    \u200Bs!boobjob \u200Bs!cum
\u200Bs!fuck    \u200Bs!feetjob \u200Bs!happyend
\u200Bs!spankh  \u200Bs!suck```""",
                inline=False
            ).set_image(
                url="https://media.discordapp.net/attachments/935251389330903110/1055585495456960533/Black_Magenta_Gaming_Dynamic_Gaming_Logos_Discord_Profile_Banner_3.gif"
            )
        }
        self.sent_message = None  # Almacena el mensaje enviado para editarlo más tarde

    
    @commands.command()
    async def help(self, ctx):
        """
        Muestra el menú con opciones
        """
        select = discord.ui.Select(
            placeholder="Selecciona una opción",
            options=[
                discord.SelectOption(label="Menu", value="embed1", description="Menu Principal", emoji="<:confunsion:910400063371636736>"),
                discord.SelectOption(label="Rolplay", value="embed2", description="Comandos de rolplay", emoji="<:feliz:910400345149149244>"),
                discord.SelectOption(label="Anime", value="embed3", description="Comandos de anime y información", emoji="<:beso:910400208607793152>"),
                discord.SelectOption(label="NSFW", value="embed4", description="Comandos NSFW", emoji="<:amor:910400150806102056>"),
            ],
            custom_id="select_option"
        )

        async def select_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("No eres el usuario que llamó el comando", ephemeral=True)
                return

            selected_value = select.values[0]

            if selected_value == 'embed4' and not interaction.channel.is_nsfw():
                await interaction.response.defer()
                await interaction.followup.send("Este canal no es NSFW. No puedes seleccionar esta opción aquí.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=self.embeds[selected_value])

        select.callback = select_callback
        view = discord.ui.View(timeout=60)
        view.add_item(select)
        await ctx.send(embed=self.embeds["embed1"], view=view)

            # !avatar command

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None,):
        """
        Muestra el avatar de un usuario.
        """
        if member is None:
            member = ctx.author
        
        # Crea un embed con el avatar del usuario
        embed = discord.Embed(
            title=f"Avatar de {member}",
            color=discord.Color.red(),
        ).set_image(url=member.avatar.url)

        view = View()
        # Crea un botón para ver el avatar en tamaño completo
        button = Button(
            style=discord.ButtonStyle.url,
            label="Ver avatar en tamaño completo",
            url=member.avatar.url
        )
        view.add_item(button)
        # Envía el embed y el botón al canal
        
        return await ctx.channel.send(embed=embed, view=view)
        
    #!severinfo command
    @commands.command()
    async def severinfo(self, ctx):
        url = ctx.guild.banner.url if ctx.guild.banner else None

        icon_url = ctx.guild.icon.url if ctx.guild.icon else None
        owner_name = ctx.guild.owner.name if ctx.guild.owner else "Desconocido"


        
        embed = discord.Embed(
            title="sever info",
        ).add_field(
            name="👑 owner",
            value=f"{owner_name}",
            inline=False
        ).add_field(
            name="🎈 id",
            value=f"{ctx.guild.id}",
            inline=False
        ).add_field(
            name="🔮 emojis",
            value = f"{len(ctx.guild.emojis)}",
            inline=False

        ).add_field(
            name="📅 Fecha de creacion del Servidor",
            value=f"{formatDate('YYYY/MM/DD,a las HH:mm:ss', ctx.guild.created_at)}"
        ).add_field(
            name="🎨 roles",
            value=(f"{len(ctx.guild.roles)}"),
            inline=False
        ).add_field(
            name="nombre del servidor",
            value=f"{ctx.guild.name}",
            inline=False
        ).add_field(
            name="icono del sever",
            value = f"[descargar icono]({icon_url})",
            inline=False

        ).add_field(
            name="nivel de seguridad",
            value=f"{ctx.guild.verification_level}",
            inline=False
        ).set_thumbnail(
            url=icon_url
        )
        return await ctx.send(embed = embed)
    
    #!botinfo command

    @commands.command()
    async def botinfo(self, ctx):

        clientStatus = f"""
        Servers :: {len(self.client.guilds)}
        Prefix  :: s!
        Users   :: {sum(guild.member_count for guild in self.client.guilds)}
        Channels:: {sum(1 for _ in self.client.get_all_channels())}
        WS Ping :: {round(self.client.latency * 1000)} ms
        """

        memInfo = psutil.virtual_memory()
        severStats = f"""
        OS         :: Ubuntu 24.04
        Cores      :: {psutil.cpu_count()}
        CPU Usage  :: {psutil.cpu_percent()}%
        RAM Usage  :: {memInfo.used // (1024 ** 2)} MB
        RAM Total  :: {memInfo.total // (1024 ** 2)} MB
        """

        owner = await self.client.fetch_user(360095173474254849)
        cacao = await self.client.fetch_user(801603753631285308)
        yukus1 = await self.client.fetch_user(366738712538644480)
        
        traditional_commands = len(self.client.commands)
        slash_commands = len(self.client.tree.get_commands())
        total_commands = traditional_commands + slash_commands
        embed = discord.Embed(
            title="Bot Statistics",
            color=0xFF0000
        ).add_field(
            name="commands",
            value=f"```{total_commands}``` comandos"
        ).add_field(
            name="ayudantes", 
            value=f"```{yukus1}\n{cacao}```", 
            inline=False
        ).add_field(
            name="Developer", 
            value=f"```{owner}```", 
            inline=False
        ).add_field(
            name="Cliente", 
            value=f"```asciidoc\n{clientStatus}```", inline=False
            ).add_field(
                name="Server", 
                value=f"```asciidoc\n{severStats}```", 
                inline=False
        )
    

        await ctx.send(embed=embed)

    #!severicon
    @commands.command()
    async def severicon(self, ctx):
        url = ctx.guild.icon.url if ctx.guild.icon else None
        embed = discord.Embed(
            title="aqui esta el icono del servidor",
            color=discord.Color.red(),
        ).set_image(
            url=url
        )
        view = View()
        button = Button(
            style=discord.ButtonStyle.url,
            label="Ver icono en tamaño completo",
            url=url
        )
        view.add_item(button)
        return await ctx.send(embed=embed, view=view)
    
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed1 = discord.Embed(
            description="Información del usuario",
            color=discord.Color.red()
        ).add_field(name="**:ticket: Nombre**:", value=f"**{member.name}**", inline=False
        ).add_field(name="avatar:", value=f"[avatar link]({member.avatar.url})", inline=False
        ).add_field(name="id", value=f"{member.id}", inline=False
        ).add_field(name="cuenta creada", value=formatDate("**DD/MM/YYYY, a las HH:mm:ss**", member.created_at), inline=False
        ).set_thumbnail(
            url=member.avatar.url
        )

        embed2 = discord.Embed(
            description="Más información del usuario",
            color=discord.Color.red()
        ).add_field(name="**:pushpin: Apodo del usuario**:", value=f"**{member.nick if member.nick is not None else 'No tiene apodo'}**", inline=False
        ).add_field(name="**:rocket: ¿Boostea?**:", value=f"**{'estoy boosteado' if member.premium_since else 'no estoy boosteado'}**", inline=False
        ).add_field(name="**Fecha de ingreso**:", value=formatDate("**DD/MM/YYYY, a las HH:mm:ss**", member.joined_at), inline=False
        ).set_thumbnail(
            url=member.avatar.url
        )

        embed3 = discord.Embed(
            description="Roles del usuario",
            color=discord.Color.red()
        ).add_field(name="**:military_medal: Roles:**", value=f"{', '.join([r.name for r in member.roles if r.name != '@everyone'])}", inline=False
        ).set_thumbnail(
            url=member.avatar.url
        )

        view = View()

        button1 = Button(
            label="Información Básica",
            style=discord.ButtonStyle.primary
        )
        async def button1_callback(interaction: Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed1, view=view)
        button1.callback = button1_callback

        button2 = Button(
            label="Más Información",
            style=discord.ButtonStyle.secondary
        )
        async def button2_callback(interaction: Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed2, view=view)
        button2.callback = button2_callback

        button3 = Button(
            label="Roles",
            style=discord.ButtonStyle.success
        )
        async def button3_callback(interaction: Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed3, view=view)
        button3.callback = button3_callback

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)

        await ctx.send(embed=embed1, view=view)

    @commands.command()
    async def code(self, ctx, *, code: str):
        """Ejecuta código Python de manera segura"""
        # Expresión regular para detectar palabras clave peligrosas
        if re.search(r"\b(import|exec|eval|open|__|os|sys|subprocess)\b", code):
            await ctx.send("Error: tu código contiene palabras clave no permitidas.", delete_after=3)
            return

        code = code.strip('` ')
        safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
                "map": map,
                "filter": filter,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "all": all,
                "any": any,
                "enumerate": enumerate,
                "sorted": sorted,
                "zip": zip,
                "help": help,
            }
        }

        safe_locals = {
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
        }

        stdout = io.StringIO()

        # Formatear el código para que se pueda ejecutar correctamente
        formatted_code = f"async def _exec_code():\n{textwrap.indent(code, '    ')}"

        try:
            exec(formatted_code, safe_globals, safe_locals)

            with contextlib.redirect_stdout(stdout):
                await asyncio.wait_for(safe_locals['_exec_code'](), timeout=5)  # Limitar a 5 segundos

            result = stdout.getvalue()
        except Exception as e:
            error_message = str(e)
            # Eliminar información sensible del error
            error_message = re.sub(r'File ".*?[/\\]', 'File "', error_message)
            result = f"Error:\n{error_message}"

        await ctx.send(f"```\n{result[:1990]}```")  # Limitar a 1990 caracteres para Discord


    @commands.command()
    async def emoji(self, ctx, emoji: discord.Emoji = None):
        """Muestra una versión más grande de un emoji personalizado."""

        if emoji is None:
            await ctx.send("Por favor, proporciona un emoji personalizado.", delete_after=3)
            return
        
        embed = discord.Embed(
            title=f"Emoji: {emoji.name}",
            color=discord.Color.blurple()
        ).set_image(url=emoji.url)

        view = View()
        button = Button(
            style=discord.ButtonStyle.url,
            label="Ver emoji en tamaño completo",
            url=emoji.url
        )
        view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Info(bot))
    print("info command complete")