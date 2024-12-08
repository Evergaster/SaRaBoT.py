import discord
import sara
from discord.ext import commands

import traceback
from rule34Python import yandereRe

def funcion(text, funcion, member: discord.Member = None, ctx = None):

    funcion_nsfw = getattr(sara.rolplayNsfw, funcion, None)

    if funcion_nsfw:
        if member is None:
            return ctx.reply("debes mencionar a un usuario", delete_after=3)
        else:
            url = funcion_nsfw()
            embed = discord.Embed(
                title=f"{ctx.author} {text} {member.name}",
                color=discord.Color.red()).set_image(
                    url=url
                )
        return embed
    else:
        return None
        

class rolplayNsfw(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @commands.command()
    @commands.is_nsfw()
    async def anal(self, ctx, member: discord.Member = None):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            
            embed = funcion('le metio el pene en el culo a', 'anal', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    
    @commands.command()
    @commands.is_nsfw()
    async def blowjob(self, ctx, member: discord.Member = None,):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            
            embed = funcion('le hizo una mamada a', 'blowjob',member,ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

            
    @commands.command()
    @commands.is_nsfw()
    async def feetjob(self, ctx, member: discord.Member = None):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            
            embed = funcion('le hizo una paja con los pies','feetjob', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)


    @commands.command()
    @commands.is_nsfw()
    async def happyend(self, ctx, member: discord.Member):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            
            embed = funcion('se vino en', 'happyend', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    
    @commands.command()
    @commands.is_nsfw()
    async def suck(self, ctx, member: discord.Member):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            
            embed = funcion('le chupo el pene a', 'suck', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    
    @commands.command()
    @commands.is_nsfw()
    async def spankh(self, ctx, member: discord.Member):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            embed = funcion('le dio una nalgada a', 'spank', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    
    @commands.command()
    @commands.is_nsfw()
    async def fuck(self, ctx, member: discord.Member):
            if member is ctx.author:
                return await ctx.send("No puedes darte eso a ti mismo.")
            embed = funcion('se cogio a', 'fuck', member, ctx)
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)


##################pruebas############################
    @commands.group(name="yande.re", invoke_without_command=True)
    @commands.is_nsfw()
    async def yande_re(self, ctx):
        """Grupo de comandos Yande.re"""
        embed = discord.Embed(
            color=discord.Color.red(),
            title="sub comandos de yande.re",
            description="s!yande.re search <palabra> \n s!yande.re artist <nombre>"
        )
        await ctx.send(embed=embed)

    @yande_re.command(name="search")
    @commands.is_nsfw()
    async def search(self, ctx, *, args: str = None):
        """Busca imágenes por palabras clave"""
        try:
            search_query = args.lower() if args else None
            
            if search_query:
                post = yandereRe.search(search_query, limit=3)
            else:
                post = yandereRe.get_random_post(limit=3)
            
            if not post:
                return await ctx.send("No se encontraron imágenes.")
            
            await ctx.send(post)
        
        except Exception as e:
            print(f"Error al buscar imágenes: {e}")
            traceback.print_exc()
            await ctx.send("No se pudo encontrar ninguna imagen")

    @yande_re.command(name="artist")
    @commands.is_nsfw()
    async def artist(self, ctx, *, args: str = None):
        """Busca información sobre un artista"""
        try:
            page = 1
            if args and args.split()[-1].isdigit():
                page = int(args.split()[-1])
                args = ' '.join(args.split()[:-1]) if len(args.split()) > 1 else None

            artist_query = args.lower() if args else None
            
            if artist_query:
                post = yandereRe.getArtists(artist_query)
            else:
                post = yandereRe.getArtists(page=page)
            
            if not post:
                return await ctx.send("No se encontró información del artista.")
            
            embed = discord.Embed(
                title="Artista de Yandere.re",
                color=discord.Color.red()
            )
            embed.add_field(name="Artista", value=post.name, inline=False)
            embed.add_field(name="ID", value=post.id, inline=False)
            
            urls = post.urls.split() if post.urls else []
            embed.add_field(
                name="URLs", 
                value='\n'.join(urls) if urls else 'No tiene links configurados', 
                inline=False
            )
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            print(f"Error al buscar artista: {e}")
            traceback.print_exc()
            await ctx.send("No se pudo encontrar la información del artista")


async def setup(bot):
    await bot.add_cog(rolplayNsfw(bot))
    print("rolplayNsfw command complete")