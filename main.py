import os
import discord
import aiohttp
from colorama import Fore
from pkgutil import iter_modules
from discord.ext import commands, tasks

class MyBot(commands.Bot):
    def __init__(self):
      super().__init__(
          command_prefix = '-',
          intents=discord.Intents.all(),
          activity=discord.Activity(type=discord.ActivityType.listening,name="-help"),
          owner_ids=[706242014056022027]
      )
      self.initial_extensions = [m.name for m in iter_modules(['cogs'], prefix='cogs.')]; self.initial_extensions.append("jishaku")

    async def setup_hook(self):
      self.background_task.start()
      self.session = aiohttp.ClientSession()
      for ext in self.initial_extensions:
        try:
          await self.load_extension(ext)
          print(f"{Fore.GREEN} {ext} loaded {Fore.RESET}")
        except:
          print(f"{Fore.RED} {ext} not loaded {Fore.RESET}")
        
    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')
  
    async def close(self):
      await super().close()
      await self.session.close()

    async def on_ready(self):
      print(Fore.MAGENTA + "========[ " + bot.user.name + " is Online! ]========" + Fore.RESET)
      print(Fore.RED + "========[ Discord Version: " + discord.__version__ + " ]=======")

bot = MyBot()
my_secret = os.environ['TOKEN']
bot.run(my_secret)
