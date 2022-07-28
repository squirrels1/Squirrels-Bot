import discord
import random
import asyncio
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(FunClass(bot))
  
class FunClass(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      
    @commands.command()
    async def guess(self, ctx: commands.Context, number: int = 100):
        guesses = range(number)
        answer = random.choice(guesses)
        await ctx.reply(f"A random number has been selected from 0 - {number}")
        condition = True
        counter = 0
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while condition:
            try:
                message = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                embedtimeout = discord.Embed(title="You didnt respond on time!", description=f'The correct number was {answer}\n You guessed {counter} times')
                return await ctx.reply(embed=embedtimeout)
            else:
                if message.content.lower() in ['end', 'cancel']:
                    embedcancel = discord.Embed(title='Canceled the game', description=f'Dont worry! You will get it next time.\n The correct number was {answer}\nYou guessed {counter} times')
                    return await ctx.reply(embed=embedcancel)
                if message.content.isdigit():
                    if int(message.content) > answer:
                        message_reply = "That's incorrect! You can keep trying or type `cancel` to end the game\n**Hint:** `guess lower`"
                    elif int(message.content) < answer:
                        message_reply = "That's incorrect! You can keep trying or type `cancel` to end the game\n**Hint:** `guess higher`"
                    if int(message.content) == answer:
                        counter += 1
                        embedwin = discord.Embed(title='Correct!', description=f'You guessed the correct number!\nThe number was `{answer}`\nYou guessed in `{counter}` tries')
                        return await ctx.reply(embed=embedwin)
                    else:
                        counter += 1
                        await ctx.reply(message_reply)