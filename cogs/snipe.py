import discord
from discord.ext import commands

DELETED_MESSAGE = "https://cdn.discordapp.com/attachments/846597178918436885/846841722994163722/messagedelete.png"

class snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = []

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message):
            self.snipes.append(message)
      
       
    @commands.command()
    async def snipe(self, ctx, *, member: discord.Member = None):

        def get_snipe(author_id=None):
            msgs = [m for m in self.snipes if m.channel.id == ctx.channel.id]
            if author_id:
                msgs = [m for m in msgs if m.author_id == author_id]

            if msgs:
                return msgs[-1]

        if member is None:
            msg = get_snipe()
        else:
            msg = get_snipe(member.id)

        if not msg:
            return await ctx.send(f"There is nothing to snipe.")

        author = msg.author.id
        message_id = msg.id
        content = msg.content
        timestamp = msg.created_at.utcnow()

        author = self.bot.get_user(author)
        if not author:
            author = await self.bot.fetch_user(author)

        if str(content).startswith("```"):
            content = f"**__Message Content__**\n {str(content)}"
        else:
            content = f"**__Message Content__**\n ```fix\n{str(content)}```"

        embed = discord.Embed(
            description=f"**Author:**  {author.mention} \n> ↳ **ID:** `{author.id}`\n\n"
            f"**Channel:** {ctx.channel.mention} \n> ↳ **ID:** `{ctx.channel.id}`\n\n"
            f"**Server:** `{ctx.guild.name}` \n> ↳ **ID:** `{ctx.guild.id}`\n\n"
            f"{content}",
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(
            name="Deleted Message Retrieved",
            icon_url=DELETED_MESSAGE,
        )
        embed.set_footer(text=f"Message ID: {message_id}")
        await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(snipe(bot))