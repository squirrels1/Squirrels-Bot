import discord
import typing
from discord.ext import commands
import asyncio 


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

      
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: typing.Union[discord.User, discord.Member], *, reason="No reason provided"):
        if ctx.author == member:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not ban yourself.")
            return await ctx.send(embed = embed)
        if isinstance(member, discord.Member):
          if ctx.author.top_role.position <= member.top_role.position:
              embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not ban a member who has a higher role than you.")
              return await ctx.send(embed = embed)
        ban = discord.Embed(title=f"<a:tick:912173533151514655> Banned {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        # await ctx.message.delete()
        try:
          await ctx.guild.ban(member, reason = reason)
          await ctx.send(embed=ban)
          try:
            await member.send(embed=ban)
          except (discord.HTTPException, discord.Forbidden):
            if isinstance(member, discord.Member):            
              embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Could not send a dm to this member.")
              return await ctx.send(embed = embed)
        except:
          embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Could not ban this member.")
          await ctx.send(embed=embed)

                      
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author == member:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not kick yourself.")
            return await ctx.send(embed = embed)
        if ctx.author.top_role.position <= member.top_role.position:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not kick a member who has a higher role than you.")
            return await ctx.send(embed = embed)
        kick = discord.Embed(title=f"<a:tick:912173533151514655> Kicked {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        try:
          await ctx.guild.kick(member, reason = reason)
          await ctx.send(embed=kick)
          try:
            await member.send(embed=kick)
          except (discord.HTTPException, discord.Forbidden):
            if isinstance(member, discord.Member):            
              embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Could not send a dm to this member.")
              return await ctx.send(embed = embed)
        except:
          embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Could not kick this member.")
          await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author == member:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not softban yourself.")
            return await ctx.send(embed = embed)
        if (ctx.author.top_role.position <= member.top_role.position) and member == discord.Member:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "You can not softban a member who has a higher role than you.")
            return await ctx.send(embed = embed)
        softban = discord.Embed(title=f"<a:tick:912173533151514655> Soft-Banned {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        try:
            await member.send(embed=softban)
        except (discord.HTTPException, discord.Forbidden):
          embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Could not send a dm to this member.")
          return await ctx.send(embed = embed)
        await asyncio.sleep(0.2)
        await member.softban(reason=reason)
        await ctx.send(embed=softban)
        await asyncio.sleep(1)
        await member.unban(reason="Softban unban")

                      
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.User):
        if not member:
            embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "Please pass the ID of the user who you want to unban.")
            return await ctx.send(embed = embed)
        if isinstance(member, discord.User):
            try:
                await ctx.guild.unban(member, reason=f"Responsible Moderator: {ctx.author}")
              
                embed = discord.Embed(title="<a:tick:912173533151514655> Success", description = "Unbanned this user.")
                return await ctx.send(embed = embed)
            except discord.NotFound:
              embed = discord.Embed(title="<a:tickfalse:912178613258969098> Error", description = "I can not find this user in the banned user list.")
              return await ctx.send(embed = embed)
        bans = tuple(ban_entry.member for ban_entry in await ctx.guild.bans())
        ban_members = tuple(str(ban_entry.member) for ban_entry in await ctx.guild.bans())
        if member in ban_members:
            member = bans[ban_members.index(member)]
            await ctx.guild.unban(member, reason="Responsible moderator: "+ str(ctx.author))
        else:
                embed = discord.Embed(title="<a:tick:912173533151514655> Success", description = "I can not find this user in the banned user list.")
                return await ctx.send(embed = embed)
        await ctx.send(f"<a:tick:912173533151514655> Successfully unbanned {member.mention}!")

                      
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description=f':lock: `{channel}` is now locked.')
        await ctx.send(embed=embed)

                      
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed=discord.Embed(description=f':unlock: `{channel}` is now unlocked.')
        await ctx.send(embed=embed)

                      
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, limit=5, member: discord.User=None):
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
                embed = discord.Embed(title="<a:tick:912173533151514655> Success", description = "Please pass an integer.")
                return await ctx.send(embed = embed)
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)


async def setup(bot):
  await bot.add_cog(ModerationCog(bot))