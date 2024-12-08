import discord
import sara
from discord.ext import commands
from rule34Python import rule34


def funcion(text, funcion):
    funcion_nsfw = getattr(sara.nsfw, funcion, None)

    if funcion_nsfw:
        url = funcion_nsfw()
        embed = discord.Embed(
            title=f"{text}",
            color=discord.Color.red()).set_image(
                url=url
            )
        return embed
    else:
        return None
        

class nsfw(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.is_nsfw()
    async def ass(self, ctx):
            embed = funcion('que buen trasero', 'ass')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
            

    @commands.command()
    @commands.is_nsfw()
    async def masturbation(self, ctx):

            embed = funcion('que rico','masturbation')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

    
    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx):

            embed = funcion('hentai', 'hentai')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)


    @commands.command()
    @commands.is_nsfw()
    async def feet(self, ctx):

            embed = funcion('mmm patas', 'feet')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

        
    @commands.command()
    @commands.is_nsfw()
    async def lwfoxgirl(self, ctx):
            embed = funcion('una chica zorro', 'foxgirl')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

        
    @commands.command()
    @commands.is_nsfw()
    async def pussy(self, ctx):
            embed = funcion('rico', 'pussy')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

        
    @commands.command()
    @commands.is_nsfw()
    async def bdsm(self, ctx):

            embed = funcion('bdsm', 'bdsm')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

        
    @commands.command()
    @commands.is_nsfw()
    async def yuri(self, ctx):
            embed = funcion('lo que te gusta', 'yuri')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

            
    @commands.command()
    @commands.is_nsfw()
    async def maid(self, ctx):
            embed = funcion('una sirvienta', 'maid')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)

        
    @commands.command()
    @commands.is_nsfw()
    async def rule34(self, ctx):
        # Divide el contenido del mensaje por espacios
        palabras = ctx.message.content.split()

        # Verifica si se proporcionó una segunda palabra después de "s!rule34"
        if len(palabras) > 1:
            search_query = '+'.join(palabras[1:]) .lower()  # Toma la segunda palabra
        else:
            search_query = None

        try:
            
            post = rule34.search(search_query, limit=3)

            return await ctx.send(post)
 
        except Exception as e:  # Captura cualquier tipo de excepción
            print(f"Error al buscar imágenes: {e}")
            allowed_mentions = discord.AllowedMentions(replied_user=False)
            await ctx.send(content="No se pudo encontrar ninguna imagen", allowed_mentions=allowed_mentions, ephemeral=True, delete_after=3)

    @commands.command()
    @commands.is_nsfw()
    async def ahegao(self, ctx):
            embed = funcion('ahegao', 'ahegao')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)


    @commands.command()
    @commands.is_nsfw()
    async def boobs(self, ctx):
            embed = funcion('tetas', 'boobs')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)


    @commands.command()
    @commands.is_nsfw()
    async def uniform(self, ctx):
        if ctx.channel.is_nsfw():
            embed = funcion('uniforme', 'uniform')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", ephemeral=True, delete_after=3)
        else:
            return await ctx.send("Este comando solo puede ser usado en canales NSFW", delete_after=3)
    
    @commands.command()
    @commands.is_nsfw()
    async def cum(self, ctx):
        if ctx.channel.is_nsfw():
            embed = funcion('cum', 'cum')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
        else:
            return await ctx.send("Este comando solo puede ser usado en canales NSFW", delete_after=3)
    
    @commands.command()
    @commands.is_nsfw()
    async def panties(self, ctx):
        if ctx.channel.is_nsfw():
            embed = funcion('panties', 'panties')
            if embed:
                await ctx.send(embed=embed)
            else:
                await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
        else:
            return await ctx.send("Este comando solo puede ser usado en canales NSFW", delete_after=3)


async def setup(bot):
    await bot.add_cog(nsfw(bot))
    print("nsfw command complete")