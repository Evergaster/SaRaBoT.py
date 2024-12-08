import discord
from discord import app_commands
import sara
from discord.ext import commands
import datetime
from discord.ui import View
import firebase_admin
from firebase_admin import db
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("FIRABASETOKEN")


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

class ContextMenu(commands.Cog):
    def __init__(self, client):
        self.client = client


@app_commands.context_menu(name="userinfo")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
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

    button1 = discord.ui.Button(
        label="Información Básica",
        style=discord.ButtonStyle.primary
    )
    async def button1_callback(interaction: discord.Interaction):
        if interaction.user != interaction.user:
            await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
            return
        await interaction.response.edit_message(embed=embed1, view=view)
    button1.callback = button1_callback

    button2 = discord.ui.Button(
        label="Más Información",
        style=discord.ButtonStyle.secondary
    )
    async def button2_callback(interaction: discord.Interaction):
        if interaction.user != interaction.user:
            await interaction.response.send_message("No tienes permiso para usar este botón.", ephemeral=True)
            return
        await interaction.response.edit_message(embed=embed2, view=view)
    button2.callback = button2_callback

    button3 = discord.ui.Button(
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


@app_commands.context_menu(name="getpoesias")
async def getpoesias(interaction: discord.Interaction, member: discord.Member):
            
            args = member.name
            poesias = db.reference("/data/poesias").get()
            client = interaction.client

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
                        fetched_users[author_id] = await client.fetch_user(int(author_id))
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
                await interaction.response.send_message(embed=embedPoe)
            else:
                await interaction.response.send_message(f"No se encontraron poesías para {search_query}.")
            return

context_menu_commands = [userinfo, getpoesias]
async def setup(bot):
    await bot.add_cog(ContextMenu(bot))

    for command in context_menu_commands:
        bot.tree.add_command(command)

