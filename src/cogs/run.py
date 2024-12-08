from discord.ext import commands
import discord
import aiohttp
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, db

load_dotenv()
webhooklink = os.getenv("WEBHOOKURL")
crev = os.getenv("FIRABASELOGIN")
apikey = os.getenv("FIRABASETOKEN")

# Inicialización de Firebase
cred = credentials.Certificate(crev)
firebase_admin.initialize_app(cred, {
    'databaseURL': apikey
})

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = discord.Embed(
                title="Bot listo!",
                description="Me he vuelto a iniciar correctamente ... <:chucha:918106668439601163>",
                color=discord.Color.green()
            )
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print(f'Serving {len(self.bot.guilds)} guilds')
        print('------')
        print(f'Shards: {self.bot.shard_count}')
        print(f'Latency: {self.bot.latency * 1000:.2f} ms')
        
        await self.bot.change_presence(activity=discord.Game(name="/help || top.gg"), status=discord.Status.dnd)

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhooklink, session=session)
            
            self.embed.add_field(name="Datos del bot", value=f"\n------\nServidores: {len(self.bot.guilds)}\nUsuarios: {sum(guild.member_count for guild in self.bot.guilds)} \n------\nshards: {self.bot.shard_count}\nLatency: {self.bot.latency * 1000:.2f} ms", inline=False)
            self.check_firebase_connection()
            await webhook.send(embed=self.embed, username='beelzebub', avatar_url='https://cdn.donmai.us/sample/e5/b5/__beelzebub_helltaker_drawn_by_wootsang__sample-e5b54721482abc1e157d317631197d22.jpg')

    def check_firebase_connection(self):
        try:
            # Intentar acceder a la base de datos
            ref = db.reference('/')
            ref.get()
            print("Conexión a Firebase exitosa.")
            self.embed.add_field(name="firebase",value="Conexión a Firebase <:firebase:1268601863482380309> exitosa.", inline=False)
        except Exception as e:
            print(f"Error al conectar con Firebase: {e}")

async def setup(bot):
   await bot.add_cog(Ready(bot))
