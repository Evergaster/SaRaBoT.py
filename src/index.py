import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import traceback
import sys

load_dotenv()
token = os.getenv('TOKEN')
prefix = os.getenv('PREFIX')

initial_extensions = (
    "cogs.message",
    "cogs.info",
    "cogs.nsfw",
    "cogs.sfw",
    "cogs.rolplay",
    "cogs.slashCommand",
    "cogs.rolplaynsfw",
    "cogs.run",
    "cogs.dataBase",
    "cogs.contexmenu"
)

allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
intents = discord.Intents.default()
intents.message_content = True
aplication_id = '1055935899118088193'

class SaRaBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=prefix,
            help_command=None,
            max_messages=None,
            intents=intents,
            allowed_mentions=allowed_mentions,
            aplication_id=aplication_id,
        )

    async def setup_hook(self) -> None:

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()

if __name__ == "__main__":
    bot = SaRaBot()
    bot.run(token)