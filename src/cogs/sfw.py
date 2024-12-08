import discord
from discord.ext import commands
import sara

def funcion(text, funcion):
    funcion_sfw = getattr(sara.sfw, funcion, None)

    if funcion_sfw:
        url = funcion_sfw()
        embed = discord.Embed(
            title=f"{text}",
            color=discord.Color.red()).set_image(
                url=url
            )
        return embed
    else:
        return None
        
class sfw(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def foxgirl(self, ctx):
        embed = funcion('que linda', 'foxgirl')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

    @commands.command()
    async def work(self, ctx):
        embed = funcion('trabajando duro o durando en el trabajo', 'work')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def yandere(self, ctx):
        embed = funcion('ta loquita', 'yandere')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

    @commands.command()
    async def vomit(self, ctx):
        embed = funcion('vomitando', 'vomit')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

    @commands.command()
    async def think(self, ctx):
        embed = funcion('pensando', 'think')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

    @commands.command()
    async def teehee(self, ctx):
        embed = funcion('teehee', 'teehee')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def like(self, ctx):
        embed = funcion('dando like', 'like')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def laugh(self, ctx):
        embed = funcion('riendo', 'laugh')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def dance(self, ctx):
        embed = funcion('bailando', 'dance')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def cry(self, ctx):
        embed = funcion('llorando', 'cry')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def angry(self, ctx):
        embed = funcion('enojado', 'angry')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    @commands.command()
    async def run(self, ctx):
        embed = funcion('corriendo', 'run')
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
    
    #es todo por horita

async def setup(bot):
    await bot.add_cog(sfw(bot))
    print("sfw command complete")
