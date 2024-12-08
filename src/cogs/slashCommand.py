from discord.ext import commands
from discord import app_commands, Interaction
from discord.ui import View, Button
import discord
import sara
import datetime
import psutil
from rule34Python import rule34, yandereRe


import aiohttp

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

def funcion(text, funcion,modulo, member: discord.Member = None, ctx = None):

    modulo_sara = getattr(sara, modulo, None)
    if modulo_sara:
        funcion_nsfw = getattr(modulo_sara, funcion, None)

    if funcion_nsfw:
        if member is None or ctx is None:
            url = funcion_nsfw()
            embed = discord.Embed(
                title=f"{text}",
                color=discord.Color.red()).set_image(
                    url=url
                )
            return embed
        else:
                url = funcion_nsfw()
                embed = discord.Embed(
                    title=f"{ctx.user.name} {text} {member.name}",
                    color=discord.Color.red()).set_image(
                        url=url
                    )
                return embed
    else:
        return None
    
class nsfwSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ass", description="bonitos culitos", nsfw=True)
    async def ass(self, interaction= Interaction):
        embed = funcion('que rico culito', 'ass', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="masturbation", description="masturbacion, que rico", nsfw=True)
    async def masturbation(self, interaction= Interaction):
        embed = funcion('que rico', 'masturbation', 'nsfw')

        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="hentai", description="monas chinas encueradas", nsfw=True)
    async def hentai(self, interaction= Interaction):
        embed = funcion('hentai', 'hentai', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)


    @app_commands.command(name="lwfoxgirl", description="lindas monas chinas furrytas", nsfw=True)
    async def foxgirl(self, interaction= Interaction):
        embed = funcion('que linda', 'foxgirl', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
        
    @app_commands.command(name="pussy", description="bonitas vaginas de anime", nsfw=True)
    async def pussy(self, interaction= Interaction):
        embed = funcion('que bonita', 'pussy', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
        
    @app_commands.command(name="bdsm", description="bondage, sadomasoquismo, dominación y sumisión", nsfw=True)
    async def bdsm(self, interaction= Interaction):
        embed = funcion('bdsm', 'bdsm', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
        
    @app_commands.command(name="panties",description="calzones, bragas, pantaletas", nsfw=True)
    async def panties(self, interaction= Interaction):
        embed = funcion('que lindas bragas', 'panties', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)


    rule34 = app_commands.Group(name="rule34", description="busca imagenes en rule34", nsfw=True)

    @rule34.command(name="search", description="Busca imágenes por palabras clave")
    async def rule34Search(self, interaction: Interaction, args: str = None, comment: bool = False):
        search_query = args.lower() if args else None
        post = None
        comment = None
        try:
            if search_query:
                post = rule34.search(search_query, limit=3)
                comment = rule34.getCommets(limit=3)
            else:
                post = rule34.get_random_post(limit=3)
                comment = rule34.getCommets(limit=3)

            if post:
                message = post
                if comment:
                    message += "\n" + comment 
                return await interaction.response.send_message(message)
            else:
                raise Exception("No se pudo encontrar ninguna imagen")

        except Exception as e:  # Captura cualquier tipo de excepción
            print(f"Error al buscar imágenes: {e}")
            allowed_mentions = discord.AllowedMentions(replied_user=False)
            try:
                await interaction.response.send_message("No se pudo encontrar ninguna imagen", allowed_mentions=allowed_mentions, ephemeral=True)
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")

    yandere = app_commands.Group(name="yandere-re", description="busca imagenes en yandere", nsfw=True, )
    @yandere.command(name="search", description="Busca imágenes por palabras clave")
    async def search(self, interaction: Interaction, args: str = None):
        search_query = args.lower() if args else None

        try:
            if search_query:
                post = yandereRe.search(search_query, limit=3)
            else:
                post = yandereRe.get_random_post(limit=3)

            return await interaction.response.send_message(post)
 
        except Exception as e:  # Captura cualquier tipo de excepción
            print(f"Error al buscar imágenes: {e}")
            allowed_mentions = discord.AllowedMentions(replied_user=False)
            await interaction.response.send_message(content="No se pudo encontrar ninguna imagen", allowed_mentions=allowed_mentions, ephemeral=True)
    
    @yandere.command(name="artist", description="Busca información sobre un artista")
    async def artist(self, interaction: Interaction, args: str = None, page: int = None):
        artist_query = args.lower() if args else None
        page = page if page else 1

        try:
            if artist_query:
                post = yandereRe.getArtists(artist_query)
            else:
                post = yandereRe.getArtists(page=page)

            embed = discord.Embed(
                title="artista de yandere.re",
                color=discord.Color.red(),
            ).add_field(inline=False, name="Artista", value=post.name
            ).add_field(inline=False, name="ID", value=post.id
            ).add_field(inline=False, name="URL", value='\n'.join(post.urls.split()) if post.urls else 'no tiene links puestos')
            return await interaction.response.send_message(embed=embed) 
        except Exception as e:
            print(f"Error al buscar artista: {e}")

    @app_commands.command(name="boobs", description="mira tetas", nsfw=True)
    async def boobs(self, interaction= Interaction):
        embed = funcion('tetas', 'boobs', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
        
    @app_commands.command(name="ahegao", description="monas chinas con caras de placer", nsfw=True)
    async def ahegao(self, interaction=Interaction):
        embed = funcion('ahegao', 'ahegao', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="uniform", description="monas chinas con uniformes", nsfw=True)
    async def uniform(self, interaction= Interaction):
        embed = funcion('uniforme', 'uniform', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="cum", description="lechita", nsfw=True)
    async def cum(self, interaction= Interaction):
        embed = funcion('lechita', 'cum', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="yuri", description="monas chinas lesbianas", nsfw=True)
    async def yuri(self, interaction= Interaction):
        embed = funcion('yuri', 'yuri', 'nsfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

################################rolplay Mencion nsfw#################################################################################
class rolplayNsfwSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="anal", description="sexito anal", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def anal(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)

        embed = funcion('le metio el pene en el culo a', 'anal', 'rolplayNsfw', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="blowjob", description="gogogogo", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def blowjob(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('se le hizo un trabajito a', 'blowjob', 'rolplayNsfw', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="happyend", description="un rica corrida", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def happyend(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)

        embed = funcion('se vino dentro de', 'happyend', 'rolplayNsfw',member,interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

        
    @app_commands.command(name="feetjob", description="hazle una paja con los pies", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def feetjob(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le hizo una paja con los pies', 'feetjob', 'rolplayNsfw', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
            
        
    @app_commands.command(name="fuck", description="coge a un usuario", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def fuck(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('se cogio a', 'fuck', 'rolplayNsfw', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
            
    @app_commands.command(name="suck", description="chupada de pito", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario") 
    async def suck(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)

        embed = funcion('se chupo de pito a', 'suck', 'rolplayNsfw', member, interaction)

        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    
    @app_commands.command(name="spankh", description="azotar a un usuario", nsfw=True, extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def spankh(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le dio una nalgada a', 'spank', 'rolplayNsfw', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

################################rolplay Mencion sfw#################################################################################
class rolplaySlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="baka", description="llama baka a un usuario", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def baka(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le dijo baka a', 'baka', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="kiss", description="besa a un usuario", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def kiss(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('beso a', 'kiss', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="angry", description="muestra tu enojo")
    async def angry(self, interaction: Interaction):
        embed = funcion('enojado', 'angry', 'rolplay')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="bored", description="muestra tu aburrimiento")
    async def bored(self, interaction: Interaction):
        embed = funcion('aburrido', 'bored', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="blush", description="muestra tu vergüenza")
    async def blush(self, interaction: Interaction):
        embed = funcion('sonrojado', 'blush', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="cry", description="muestra tus lágrimas")
    async def cry(self, interaction: Interaction):
        embed = funcion('llorando', 'cry', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="dance", description="baila")
    async def dance(self, interaction: Interaction):
        embed = funcion('bailando', 'dance', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="kill", description="muelto", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def kill(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('mato a', 'kill', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="laugh", description="ríete")
    async def laugh(self, interaction: Interaction):
        embed = funcion('riendo', 'laugh', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="like", description="me gusta")
    async def like(self, interaction: Interaction):
        embed = funcion('me gusta', 'like', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="poke", description="toca a un usuario", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def poke(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le toco', 'poke', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="punch", description="golpea a alguien", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def punch(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le dio un golpe a', 'punch', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="run", description="corre")
    async def run(self, interaction: Interaction):
        embed = funcion('corriendo', 'run', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="sleep", description="mimido")
    async def sleep(self, interaction: Interaction):
        embed = funcion('durmiendo', 'sleep', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="sfwspank", description="nalgada", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def sfwSpank(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le dio una nalgada a', 'spank', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="stare", description="mira fijamente a alguien", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def stare(self, interaction: Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("No puedes mencionarte a ti mismo.", ephemeral=True)
        
        embed = funcion('le esta mirando fijamente a', 'stare', 'rolplay', member, interaction)
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="think", description="piensa")
    async def think(self, interaction: Interaction):
        embed = funcion('pensando', 'think', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="teehee", description="teehee")
    async def teehee(self, interaction: Interaction):
        embed = funcion('teehee', 'teehee', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="travel", description="viaja")
    async def travel(self, interaction: Interaction):
        embed = funcion('viajando', 'travel', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)

    @app_commands.command(name="vomit", description="vomita")
    async def vomit(self, interaction: Interaction):
        embed = funcion('vomitando', 'vomit', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="wink", description="guiña un ojo")
    async def wink(self, interaction: Interaction):
        embed = funcion('guiño', 'wink', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="work", description="trabaja")
    async def work(self, interaction: Interaction):
        embed = funcion('trabajando', 'work', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="yandere", description="muestra tu lado yandere")
    async def yandere(self, interaction: Interaction):
        embed = funcion('yandere', 'yandere', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="neko", description="muestra tu lado neko")
    async def neko(self, interaction: Interaction):
        embed = funcion('neko', 'neko', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
    @app_commands.command(name="foxgirl", description="muestra tu lado furry")
    async def foxgirl(self, interaction: Interaction):
        embed = funcion('foxgirl', 'foxgirl', 'sfw')
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No se pudo encontrar una imagen en esta categoría", ephemeral=True)
    
#########################################comandos info#################################################################################
class commandsSlash(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot
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

    @app_commands.command(name="serverinfo", description="Muestra la información del servidor")
    async def severinfo(self, interaction= Interaction):

        icon_url = interaction.guild.icon.url if interaction.guild.icon else None
        owner_name = interaction.guild.owner.name if interaction.guild.owner else "Desconocido"
     
        embed = discord.Embed(
            title="sever info",
        ).add_field(
            name="👑 owner",
            value=f"{owner_name}",
            inline=False
        ).add_field(
            name="🎈 id",
            value=f"{interaction.guild.id}",
            inline=False
        ).add_field(
            name="🔮 emojis",
            value = f"{len(interaction.guild.emojis)}"

        ).add_field(
            name="📅 Fecha de creacion del Servidor",
            value=f"{formatDate('YYYY/MM/DD,a las HH:mm:ss', interaction.guild.created_at)}",
            inline=False
        ).add_field(
            name="🎨 roles",
            value=(f"{len(interaction.guild.roles)}"),
            inline=False
        ).add_field(
            name="nombre del servidor",
            value=f"{interaction.guild.name}",
            inline=False
        ).add_field(
            name="icono del sever",
            value = f"[descargar icono]({icon_url})",
            inline=False


        ).add_field(
            name="nivel de seguridad",
            value=f"{interaction.guild.verification_level}",
            inline=False
        ).set_thumbnail(
            url=icon_url
        )
        return await interaction.response.send_message(embed = embed)
    
    @app_commands.command(name="botinfo", description="Muestra la información del bot")
    async def botinfo(self, interaction: discord.Interaction):

        clientStatus = f"""
        Servers :: {len(self.bot.guilds)}
        Prefix  :: s!
        Users   :: {sum(guild.member_count for guild in self.bot.guilds)}
        Channels:: {sum(1 for _ in self.bot.get_all_channels())}
        WS Ping :: {round(self.bot.latency * 1000)} ms
        """

        memInfo = psutil.virtual_memory()
        severStats = f"""
        OS         :: 
        Cores      :: {psutil.cpu_count()}
        CPU Usage  :: {psutil.cpu_percent()}%
        RAM Usage  :: {memInfo.used // (1024 ** 2)} MB
        RAM Total  :: {memInfo.total // (1024 ** 2)} MB
        """

        owner = await self.bot.fetch_user(360095173474254849)
        cacao = await self.bot.fetch_user(801603753631285308)
        yukus1 = await self.bot.fetch_user(366738712538644480)

        embed = discord.Embed(
            title="Bot Statistics",
            color=0xFF0000
        ).add_field(
            name="Helpers",
            value=f"{cacao.mention}\n{yukus1.mention}",
            inline=False
        ).add_field(
            name="Developer",
            value=f"{owner.mention}",
            inline=False
        ).add_field(
            name="Client",
            value=clientStatus,
            inline=False
        ).add_field(
            name="Server",
            value=severStats,
            inline=False
        ).set_footer(
            text=f"{interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar_url
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="severicon", description="regresa el icono del servidor")
    async def severicon(self, interaction: Interaction):
        url = interaction.guild.icon.url if interaction.guild.icon else None
        embed = discord.Embed(
            title="icono del servidor",
            color=0xFF0000
        ).set_image(
            url=url
        )
        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="descargar icono",
            url=url
        )
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="userinfo", description="Muestra la información de un usuario", extras={"member": "menciona a un usuario"})
    @app_commands.describe(member="menciona a un usuario")
    async def userinfo(self, interaction: Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
            
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
        
        embed2 = discord.Embed(            description="Más información del usuario",
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
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user != interaction.user:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed1, view=view)
        button1.callback = button1_callback

        button2 = Button(
            label="Más Información",
            style=discord.ButtonStyle.secondary
        )
        async def button2_callback(interaction: discord.Interaction):
            if interaction.user != interaction.user:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed2, view=view)
        button2.callback = button2_callback

        button3 = Button(
            label="Roles",
            style=discord.ButtonStyle.success
        )
        async def button3_callback(interaction: discord.Interaction):
            if interaction.user != interaction.user:
                await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
                return
            await interaction.response.edit_message(embed=embed3, view=view)
        button3.callback = button3_callback

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)

        await interaction.response.send_message(embed=embed1, view=view, ephemeral=True)

    @app_commands.command(name="code", description="Ejecuta código básico de Python")
    @app_commands.describe(file="Sube un archivo con tu código Python")
    async def code(self, interaction: Interaction, file: discord.Attachment):
        if not file.filename.endswith(('.py', '.txt')):
            await interaction.response.send_message("Por favor, sube un archivo .py o .txt")
            return

        code = (await file.read()).decode('utf-8')

        # Sanitizar la entrada para evitar ejecución de código peligroso
        if re.search(r"\b(import|exec|eval|open|__|os|sys|subprocess)\b", code):
            await interaction.response.send_message("Error: tu código contiene palabras clave no permitidas.", ephemeral=True)
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
            'interaction': interaction,
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

        await interaction.response.send_message(f"```\n{result[:1990]}```")



    @app_commands.command(name="help", description="Muestra la ayuda del bot")
    async def help(self, interaction: discord.Interaction):
        select = discord.ui.Select(
            placeholder="seleciona una opcion",
            options=[
                discord.SelectOption(label="Menu", value="embed1", description="Menu Principal", emoji="<:confunsion:910400063371636736>"),
                discord.SelectOption(label="Rolplay", value="embed2", description="Comandos de rolplay", emoji="<:feliz:910400345149149244>"),
                discord.SelectOption(label="anime", value="embed3", description="Comandos de anime y informacion", emoji="<:beso:910400208607793152>"),
                discord.SelectOption(label="nsfw", value="embed4", description="Comandos nsfw", emoji="<:amor:910400150806102056>"),
            ],
            custom_id="select_option"
        )

        async def select_callback(select_interaction: discord.Interaction):
            if select_interaction.user.id != interaction.user.id:
                await select_interaction.response.defer()
                await select_interaction.followup.send("No eres el usuario que llamó el comando", ephemeral=True)
                return
            
            selected_value = select.values[0]

            if selected_value == 'embed4' and not select_interaction.channel.is_nsfw():
                await select_interaction.response.defer()
                await select_interaction.followup.send("Este canal no es NSFW. No puedes seleccionar esta opción aquí.", ephemeral=True)
                return
            
            await select_interaction.response.edit_message(embed=self.embeds[selected_value])
        
        select.callback = select_callback
        view = View(timeout=60)
        view.add_item(select)
        await interaction.response.send_message(embed=self.embeds["embed1"], view=view)

    @app_commands.command(name="avatar", description="Muestra el avatar de un usuario")
    @app_commands.describe(member="menciona a un usuario")
    async def avatar(self, interaction: Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        embed = discord.Embed(
            title=f"Avatar de {member.name}",
            color=discord.Color.red()
        ).set_image(
            url=member.avatar.url
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="jumbo", description="Muestra el emoji personalizado en formato de foto")
    @app_commands.describe(emoji="Inserta el emoji personalizado")
    async def emoji(self, interaction: discord.Interaction, emoji: str):
        # Patrón para encontrar el ID del emoji personalizado
        emoji_pattern = r'<:.*?:(\d+)>'
        match = re.match(emoji_pattern, emoji)
        
        if match:
            emoji_id = int(match.group(1))
            try:
                custom_emoji = await interaction.guild.fetch_emoji(emoji_id)
                
                embed = discord.Embed(
                    title=f"Emoji: {custom_emoji.name}",
                    color=discord.Color.red()
                ).set_image(url=custom_emoji.url)
                
                view = View()

                button = Button(
                    label="Descargar",
                    style=discord.ButtonStyle.link,
                    url=custom_emoji.url
                )
                view.add_item(button)

                await interaction.response.send_message(embed=embed, view=view)
            except discord.NotFound:
                await interaction.response.send_message(content="No se encontró el emoji personalizado.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Por favor, inserta un emoji personalizado válido.", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print("question loaded")
        fmt = await self.bot.tree.sync()
        print(f"Synced {len(fmt)} commands")

async def setup(bot):
    await bot.add_cog(nsfwSlash(bot))
    await bot.add_cog(rolplayNsfwSlash(bot))
    await bot.add_cog(commandsSlash(bot))
    await bot.add_cog(rolplaySlash(bot))
    
