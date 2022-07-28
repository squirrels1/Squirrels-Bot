import discord
import typing
from discord.ext import commands

class Counter(discord.ui.View):   
    def __init__(self, total, first, second, embed):
      super().__init__()
      self.total = total
      self.first = first
      self.second = second
      self.responded = []
      self.embed = embed
      self.check = False
      
    @discord.ui.button(label='0', style=discord.ButtonStyle.red, emoji = "1️⃣")
    async def poll1(self, interaction: discord.Interaction, button: discord.ui.Button):
      number = int(button.label) if button.label else 0
      if number + 1 >= self.total:
        button.style = discord.ButtonStyle.green
        for item in self.children:
          item.disabled = True
        await self.message.edit(view=self)
        if self.check == False:
          self.embed.description += f"\n\n**`{self.first}` Has won**"
          self.embed.color = discord.Color.green()
          await interaction.message.edit(embed=self.embed)
          await interaction.message.reply(f"**`{self.first}` has won**")
          self.check = True
      button.label = str(number + 1)
      if interaction.user not in self.responded:
        await interaction.response.edit_message(view=self)
        self.responded.append(interaction.user)
        await interaction.followup.send(f'✅ You have voted for {self.first}.', ephemeral=True)
      else:
        await interaction.response.send_message('❌ You can only vote once in this poll.', ephemeral=True)

    @discord.ui.button(label='0', style=discord.ButtonStyle.red, emoji = "2️⃣")
    async def poll2(self, interaction: discord.Interaction, button: discord.ui.Button):
      number = int(button.label) if button.label else 0
      if number + 1 >= self.total:
        button.style = discord.ButtonStyle.green
        for item in self.children:
          item.disabled = True
        if self.check == False:
          self.embed.description += f"\n\n**`{self.second}` has won**"
          self.embed.color = discord.Color.green()
          await interaction.message.edit(embed=self.embed)
          await interaction.message.reply(f"**`{self.second}` has won**")
          self.check = True
      button.label = str(number + 1)
      if interaction.user not in self.responded:
        await interaction.response.edit_message(view=self)
        self.responded.append(interaction.user)
        await interaction.followup.send(f'✅ You have voted for {self.second}', ephemeral=True)
      else:
        await interaction.response.send_message('❌ You can only vote once in this poll.', ephemeral=True)

      
class TestCog(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      
    @commands.command()
    async def poll(self, ctx: commands.Context, count: int, *, option):
      a = option.split(',')
      embed = discord.Embed(title = a[0], description = f"`{count}` vote(s) to win.\n\n:one: {a[1]}\n:two: {a[2]}", timestamp=discord.utils.utcnow(), color = discord.Color.green())
      await ctx.send(embed = embed, view=Counter(count, a[1], a[2], embed))


async def setup(bot):
  await bot.add_cog(TestCog(bot))