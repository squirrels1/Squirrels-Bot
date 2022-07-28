import discord, asyncio
from discord.ext import commands

class Shush(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.off = []
    self.check = "<a:tick:912173533151514655>"
    self.fail = "<a:tickfalse:912178613258969098>"

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def shush(self, ctx, user: discord.User):
    try:
      if user.id not in self.off:
        if user.id != 706242014056022027 and user.id != 996855623394279466:
          self.off.append(user.id)
          await ctx.reply(f"{self.check} - `{user.id}` appended to the silenced list.")
          
        else:
          if user.id != 996855623394279466:
            await ctx.reply(f"{self.fail} - You cant shush the master.\n\n<@706242014056022027> Mute this fool (<@{ctx.author.id}>)")
            
          else:
            await ctx.reply(f"{self.fail} - You cant shush me.")
          
      else:
        await ctx.reply(f"{self.fail} - `{user.id}` is already in the silenced list.")
        
    except:
      await ctx.reply(f"{self.fail} - There was an error performing this command.")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def unshush(self, ctx, user: discord.User):
    try:
      if user.id in self.off:
        if user.id != ctx.author.id:
          self.off.remove(user.id)
          await ctx.reply(f"{self.check} - `{user.id}` removed from the silenced list.")
          
        else:
          await ctx.reply(f"{self.fail} - You can't unshush yourself.")
          
      else:
        await ctx.reply(f"{self.fail} - This user is not in the silenced list.")
        
    except:
      await ctx.reply(f"{self.fail} - There was an error performing this command.")

  @commands.command()
  async def shushedlist(self, ctx):
    a = ""
    for item in self.off:
      a += f"{item} | <@{item}>\n"
      
    if self.off == []:
      await ctx.reply("There are no shushed users at the moment.")
      
    else:
      await ctx.reply(a)
    
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def resetall(self, ctx):
    count = 0
    if ctx.author.id in self.off:
      await ctx.reply(f"{self.fail} - <@{ctx.author.id}> You can't use this command while you are in the shushed list.")
      
    else:
      for item in self.off:
        self.off.remove(item)
        count += 1
        
      await ctx.reply(f"{self.check} - Removed `{count}` user(s) from the silenced list.")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def squirrels(self, ctx):
    count = 0
    for item in self.off:
      if item == 706242014056022027:
        self.off.remove(item)
        count += 1
        
    await ctx.reply("Anything for you master :)")
    await asyncio.sleep(1)
    await ctx.reply(f"{self.check} - Removed you from the silenced list.")
  
  @commands.Cog.listener('on_message')
  async def on_message(self, message: discord.Message):
    if message.author.id in self.off:
      try:
        print(message.author.name + " - " + message.content)
        await message.delete()
        
      except:
        pass
    
async def setup(bot):
    await bot.add_cog(Shush(bot))