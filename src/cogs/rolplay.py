import discord
import sara
from discord.ext import commands

def funcion(text, funcion, modulo, member: discord.Member = None, ctx = None):
    moduloSara = getattr(sara, modulo, None)
    if moduloSara:
        funcion_reaccion = getattr(moduloSara, funcion, None)


    if member is None:
        url = funcion_reaccion()
        embed = discord.Embed(
            title=f"{ctx.author} {text}",
            color=discord.Color.red()).set_image(
                url=url
            )
        return embed
    else:
        url = funcion_reaccion()
        embed = discord.Embed(
            title=f"{ctx.author} {text} {member.name}",
            color=discord.Color.red()).set_image(
                url=url
            )
    return embed

        
class rolplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def baka(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('le dijo baka a','baka', 'rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        embed = funcion('beso a','kiss','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    @commands.command()
    async def spank(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('le dio una nalgada a','spank','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('le dio un golpe a','punch','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def kill(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('mato a','kill','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('le dio un toque a','poke','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def sleep(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('se durmio','sleep','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def stare(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply("debes mencionar a un usuario", delete_after=3)
        
        embed = funcion('le esta mirando fijamente a','stare','rolplay', member, ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    ####################################reaciones####################################
    
    @commands.command()
    async def blush(self, ctx):
        embed = funcion('se sonrojo', 'blush', 'sfw', ctx=ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def wink(self, ctx):
        embed = funcion('guiño', 'wink', 'sfw', ctx=ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)
    
    @commands.command()
    async def travel(self, ctx):
        embed = funcion('viaje', 'travel', 'sfw', ctx=ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    @commands.command()
    async def bored(self, ctx):
        embed = funcion('aburrido', 'bored', 'sfw', ctx=ctx)
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo encontrar una imagen en esta categoría", delete_after=3)

    
async def setup(bot):
    await bot.add_cog(rolplay(bot))
    print("rolplay cog loaded")
