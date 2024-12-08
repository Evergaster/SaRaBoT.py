
from firebase_admin import db
from dotenv import load_dotenv
import os
from discord.ext import commands
import discord
import random
from discord import app_commands, Interaction, ui
import aiohttp

load_dotenv()
apikey = os.getenv("FIRABASETOKEN")

class dataBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poetext(self, ctx, *, args=None):
        if not args:
            embed = discord.Embed(
                title='Poesía Sara',
                description='<:cobijita:918106713054384138> bienvenido a  y escribe tus historias o peoesias personales con los siguientes comando:',
            ).add_field(
                name='s!poetext <texto>',
                value='sube tus textos para que los demas de una opinion (máximo 256 caracteres)',
                inline=False
            ).add_field(
                name='s!poetext random',
                value='Para ver una poesía aleatoria',
                inline=False
            ).add_field(
                name='s!poetext <nameuser>',
                value='Para ver todas las poesías de un usuario (puedes usar directamente al dar click derecho en el usuario "getpoesias")',
                inline=False
            ).set_image(
                url="https://cdn.discordapp.com/attachments/1221521316239245433/1261752914121326623/9d023e35dcf94e252ddda4b3c5c1d0e6.jpg?ex=66941a78&is=6692c8f8&hm=68c9ef4bdd3800cfd8d90114f72c75fb3a541b6bb9b4066e87c813ec04e197b4&"
            )
            await ctx.send(embed=embed)
            return

        search_query = args.lower().strip()
        
        poesias = db.reference("/data/poesias").get()

        if search_query == "random":
            await self.send_random_poetry(ctx, poesias)
            return

        if poesias:
            search_query = search_query.lower()
            found_poems = []
            total_likes = 0
            total_dislikes = 0
            user = None
            fetched_users = {}

            for poem_id, data in poesias.items():
                author_id = data['author']
                if author_id not in fetched_users:
                    try:
                        fetched_users[author_id] = await self.bot.fetch_user(int(author_id))
                    except Exception:
                        fetched_users[author_id] = None

                fetched_user = fetched_users[author_id]
                if fetched_user and fetched_user.name.lower() == search_query:
                    found_poems.append(data['texto'])
                    total_likes += data.get('likes', 0)
                    total_dislikes += data.get('dislikes', 0)
                    user = fetched_user

            if found_poems:
                poems_text = "\n\n".join(found_poems)
                embedPoe = discord.Embed(
                    title=f" Poesías de {user.name}",
                    description=poems_text,
                    color=discord.Color.random()
                ).add_field(
                    name="Total Likes",
                    value=str(total_likes),
                    inline=True
                ).add_field(
                    name="Total Dislikes",
                    value=str(total_dislikes),
                    inline=True
                )
                if user and user.avatar:
                    embedPoe.set_thumbnail(url=user.avatar.url)
                await ctx.send(embed=embedPoe)
            else:
                await ctx.send(f"No se encontraron poesías para {search_query}.", delete_after=3)
            return

        formatoPoesia = {
            'author': str(ctx.author.id),
            'texto': search_query,
            'likes': 0,
            'dislikes': 0
        }
        new_poetry_ref = db.reference("/data/poesias").push()
        new_poetry_ref.set(formatoPoesia)
        
        await ctx.send("Tu poesía ha sido subida a la base de datos.", delete_after=3)

    async def send_random_poetry(self, ctx, poesias):
        if poesias:
            random_post_id, random_poetry = random.choice(list(poesias.items()))
            username = await self.bot.fetch_user(int(random_poetry['author']))
            likes = random_poetry.get('likes', 0)
            dislikes = random_poetry.get('dislikes', 0)
            embedRandom = discord.Embed(
                title=f"Poesía aleatoria, de {username}",
                description=random_poetry['texto'],
                color=discord.Color.random()
            ).set_thumbnail(url=username.avatar.url).add_field(name="Likes", value=str(likes)).add_field(name="Dislikes", value=str(dislikes))

            view = discord.ui.View()
            button = discord.ui.Button(
                emoji="<:like_RK:1263225611753881610>",
                style=discord.ButtonStyle.green,
                label="Likear",
                custom_id="like_button"
            )
            button2 = discord.ui.Button(
                emoji="<:report53:1263225613888524490>",
                style=discord.ButtonStyle.danger,
                label="reportar",
                custom_id="report_button"
            )
            button3 = discord.ui.Button(
                emoji="<:pol_dislike:1263225612911247461>",
                style=discord.ButtonStyle.gray,
                label="Dislike",
                custom_id="dislike_button"
            )
            button4 = discord.ui.Button(
                emoji="<:Comment:1263225610336206988>",
                style=discord.ButtonStyle.primary,
                label="Comentar",
                custom_id="comment_button"
            )

            button.callback = lambda interaction: self.like_callback(interaction, username, random_poetry, random_post_id, likes)
            button2.callback = lambda interaction: self.report_callback(interaction, username, random_poetry)
            button3.callback = lambda interaction: self.dislike_callback(interaction, username, random_poetry, random_post_id, dislikes)
            button4.callback = lambda interaction: self.comment_callback(interaction, username, random_poetry)
            
            view.add_item(button)
            view.add_item(button3)
            view.add_item(button2)
            view.add_item(button4)

            await ctx.send(embed=embedRandom, view=view)
        else:
            await ctx.send("No hay poesías disponibles.", delete_after=3)

    async def like_callback(self, interaction, username, random_poetry, random_post_id, likes):
        if interaction.user == username:
            await interaction.response.send_message("No puedes dar like a tu propia poesía.", ephemeral=True)
            return

        if interaction.data['custom_id'] == "like_button":
            new_likes = likes + 1
            db.reference(f'data/poesias/{random_post_id}').update({'likes': new_likes})
            await interaction.response.send_message(f"Has dado like a la poesía. Ahora tiene {new_likes} likes.", ephemeral=True)

    async def dislike_callback(self, interaction, username, random_poetry, random_post_id, dislikes):
        if interaction.user == username:
            await interaction.response.send_message("No puedes dar dislike a tu propia poesía.", ephemeral=True)
            return

        if interaction.data['custom_id'] == "dislike_button":
            new_dislikes = dislikes + 1
            db.reference(f'data/poesias/{random_post_id}').update({'dislikes': new_dislikes})
            await interaction.response.send_message(f"Has dado dislike a la poesía. Ahora tiene {new_dislikes} dislikes.", ephemeral=True)

    async def report_callback(self, interaction, username, random_poetry):
        if interaction.user == username:
            await interaction.response.send_message("No puedes reportar tu propia poesía.", ephemeral=True)
            return

        if interaction.data['custom_id'] == "report_button":
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(os.getenv("REPORTESURL"), session=session)
                embedReport = discord.Embed(
                    title="Reporte de poesía",
                    description=f"id: {random_poetry['author']}\nUsuario: {username}\nPoesía: {random_poetry['texto']}",
                    color=discord.Color.red()
                )
                await webhook.send(embed=embedReport, username='reportes', avatar_url='https://cdn.donmai.us/sample/e5/b5/__beelzebub_helltaker_drawn_by_wootsang__sample-e5b54721482abc1e157d317631197d22.jpg')
            await interaction.response.send_message("El reporte se envió correctamente.", ephemeral=True)

    async def comment_callback(self, interaction, username, random_poetry):
        if interaction.user == username:
            await interaction.response.send_message("No puedes comentar tu propia poesía.", ephemeral=True)
            return
        
        if interaction.data['custom_id'] == "comment_button":
            modal = discord.ui.Modal(title="Pon tu comentario")
            modal.add_item(discord.ui.TextInput(
                label="Escribe tu comentario sobre la poesía", 
                style=discord.TextStyle.short, 
                placeholder="Escribe aquí tu comentario", 
                required=True, 
                max_length=200
            ))
        
            async def modal_callback(modal_interaction: discord.Interaction):
                answer = modal.children[0].value
                embed = discord.Embed(
                    title="Comentario",
                    description=f"Comentario enviado por {modal_interaction.user.mention}\n{answer}",
                    color=discord.Color.random()
                ).add_field(
                    name="Poesía",
                    value=random_poetry['texto']
                )
                try:
                    await username.send(embed=embed)
                    await modal_interaction.response.send_message("Comentario enviado correctamente.", ephemeral=True)
                except discord.errors.Forbidden:
                    await modal_interaction.response.send_message("No se pudo enviar el DM. El usuario puede tener los DMs cerrados.", ephemeral=True)
                except Exception as e:
                    await modal_interaction.response.send_message(f"Error al enviar el comentario: {str(e)}", ephemeral=True)

            modal.on_submit = modal_callback
            await interaction.response.send_modal(modal)

    @app_commands.command(name='poems', description='Interact with poetry commands')
    @app_commands.describe(option='The command option', args='Additional arguments')
    async def poems(self, inter: Interaction, option: str, args: str = None):
        poesias = db.reference("/data/poesias").get()

        if option == "random":
            await self.send_random_poetry_slash(inter, poesias)
            return

        if option == "user" and args:
            search_query = args.lower()
            found_poems = []
            total_likes = 0
            total_dislikes = 0
            user = None
            fetched_users = {}

            for poem_id, data in poesias.items():
                author_id = data['author']
                if author_id not in fetched_users:
                    try:
                        fetched_users[author_id] = await self.bot.fetch_user(int(author_id))
                    except Exception:
                        fetched_users[author_id] = None

                fetched_user = fetched_users[author_id]
                if fetched_user and fetched_user.name.lower() == search_query:
                    found_poems.append(data['texto'])
                    total_likes += data.get('likes', 0)
                    total_dislikes += data.get('dislikes', 0)
                    user = fetched_user

            if found_poems:
                poems_text = "\n\n".join(found_poems)
                embedPoe = discord.Embed(
                    title=f"Poesías de {user.name}",
                    description=poems_text,
                    color=discord.Color.random()
                ).add_field(
                    name="Total Likes",
                    value=str(total_likes),
                    inline=True
                ).add_field(
                    name="Total Dislikes",
                    value=str(total_dislikes),
                    inline=True
                )
                if user and user.avatar:
                    embedPoe.set_thumbnail(url=user.avatar.url)
                await inter.response.send_message(embed=embedPoe)
            else:
                await inter.response.send_message(f"No se encontraron poesías para {search_query}.")
            return

        if option == "subir" and args:
            search_query = args.lower().strip()

            if len(search_query.split()) <= 2 or len(search_query) > 256:
                await inter.response.send_message("Por favor, ingrese una poesía con más de dos palabras y menos de 256 caracteres.")
                return

            formato_poesia = {
                'author': str(inter.user.id),
                'texto': search_query,
                'likes': 0,
                'dislikes': 0
            }
            new_poetry_ref = db.reference("/data/poesias").push()
            new_poetry_ref.set(formato_poesia)
            await inter.response.send_message("Tu poesía ha sido subida a la base de datos.")
            return

        await inter.response.send_message("Opción inválida o faltan argumentos. Por favor, use el comando correctamente.")

    @poems.autocomplete('option')
    async def poems_autocomplete(self, inter: discord.Interaction, current: str):
        choices = ['random', 'user', 'subir']
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

    async def send_random_poetry_slash(self, Inter, poesias):
        if poesias:
            random_post_id, random_poetry = random.choice(list(poesias.items()))
            username = await self.bot.fetch_user(int(random_poetry['author']))
            likes = random_poetry.get('likes', 0)
            dislikes = random_poetry.get('dislikes', 0)
            embedRandom = discord.Embed(
                title=f"Poesía aleatoria, de {username}",
                description=random_poetry['texto'],
                color=discord.Color.random()
            ).set_thumbnail(url=username.avatar.url).add_field(name="Likes", value=str(likes)).add_field(name="Dislikes", value=str(dislikes))

            view = discord.ui.View()
            button = discord.ui.Button(
                emoji="<:like_RK:1263225611753881610>",
                style=discord.ButtonStyle.green,
                label="Likear",
                custom_id="like_button"
            )
            button2 = discord.ui.Button(
                emoji="<:report53:1263225613888524490>",
                style=discord.ButtonStyle.danger,
                label="reportar",
                custom_id="report_button"
            )
            button3 = discord.ui.Button(
                emoji="<:pol_dislike:1263225612911247461>",
                style=discord.ButtonStyle.gray,
                label="Dislike",
                custom_id="dislike_button"
            )
            button4 = discord.ui.Button(
                emoji="<:Comment:1263225610336206988>",
                style=discord.ButtonStyle.primary,
                label="Comentar",
                custom_id="comment_button"

            )
            

            button.callback = lambda interaction: self.like_callback(interaction, username, random_poetry, random_post_id, likes)
            button2.callback = lambda interaction: self.report_callback(interaction, username, random_poetry)
            button3.callback = lambda interaction: self.dislike_callback(interaction, username, random_poetry, random_post_id, dislikes)
            button4.callback = lambda interaction: self.comment_callback(interaction, username, random_poetry)
            
            
            view.add_item(button)
            view.add_item(button3)
            view.add_item(button2)
            view.add_item(button4)

            await Inter.response.send_message(embed=embedRandom, view=view)
        else:
            await Inter.response.send_message("No hay poesías disponibles.")
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"poemas slash conectado")

async def setup(bot):
    await bot.add_cog(dataBase(bot))
    print("dataBase command complete")