import typing
import random
import asyncio
import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(aliases=['si'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        thread_channels = len(ctx.guild.threads)
        # stages = len(ctx.guild.stages)
        embed = discord.Embed(title=f"{ctx.guild.name} Info")
        embed.add_field(name=f"General  Info", value = f"<:id:915110710516793384> ID: `{ctx.guild.id}`\n<:owner:907296832642764822> Owner: `{ctx.guild.owner}`\n<:join:915110675800555542> Created: {discord.utils.format_dt(ctx.guild.created_at, 'F')} ({discord.utils.format_dt(ctx.guild.created_at, 'R')})\n<:afadsfs:909537820790620230> Role amount: {len(ctx.guild.roles)}", inline = False)
        total = ctx.guild.member_count
        new_list = [(0 if str(x.status) == 'online' else 1 if str(x.status) == 'idle' else 2 if str(x.status) == 'dnd' else 3) for x in ctx.guild.members]
        online, idle, dnd, offline = [new_list.count(x) for x in range(4)]
        another_list = [(0 if x.bot else 1) for x in ctx.guild.members]
        bots, humans = [another_list.count(x) for x in range(2)]
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
            animated = ['png', 'jpg', 'jpeg', 'webp']
            if ctx.guild.icon.is_animated():
                animated.append('gif')
                icon = " | ".join([f"[{x.upper()}]({ctx.guild.icon.replace(format=x, size=1024).url})" for x in animated])
            else:
                icon = " | ".join([f"[{x.upper()}]({ctx.guild.icon.replace(format=x, size=1024).url})" for x in animated])
            
            embed.add_field(name="<:afadsfs:909537820790620230> Server Icon",
                            value=(f"\n╰ {icon}"),inline=False)
        embed.add_field(name="<:afadsfs:909537820790620230> Channels:", value=f"<:chan:915110447454224415> Channels: {text_channels}\n<:thread:915112100777574420> Threads: {thread_channels}\n<:vsc:915111893725765703> Voice: {voice_channels}\n <:channels:915110435273973770> Categories: {categories}\n <:stage:915112474682990654> Stages: stages", inline = False)
        embed.add_field(name="<:members:907302642542325771> Member Info", value=f"╰ Total Members: {total}\n:bust_in_silhouette: Total Humans: {humans}\n:robot: Total Bots: {bots}\n<:online:907296805040062465> Online: {online}\n<:offline:915110878691598366> Offline: {offline}\n<:idle:915110894596399124> Idle: {idle}\n<:dnd:915110652958363668> DND: {dnd}", inline=False)
        last_boost = max(ctx.guild.members, key=lambda m: m.premium_since or ctx.guild.created_at)
        if last_boost.premium_since is not None:
            boost = f"\n{last_boost}" \
                    f"\n╰ {discord.utils.format_dt(last_boost.premium_since, style='R')}"
        else:
            boost = "\n╰ No active boosters"
        embed.add_field(name="<:booster:907296708269064212> Boosts:", value = f"Level: {ctx.guild.premium_tier}\n╰ Amount: {ctx.guild.premium_subscription_count}\n<:booster:907296708269064212> **Last booster:** {boost}")
        embed.add_field(name=f"<:emojis:915110958832160779> Emojis:", value=f"Static: {len([e for e in ctx.guild.emojis if not e.animated])}/{ctx.guild.emoji_limit}\nAnimated: {len([e for e in ctx.guild.emojis if e.animated])}/{ctx.guild.emoji_limit}", inline=False)
      
        await ctx.send(embed=embed)
    @commands.command(aliases=['whois', 'ui'])
    async def userinfo(self, ctx, member: typing.Optional[discord.Member]):
        member = member or ctx.author
        fetched_user = await self.bot.fetch_user(member.id)
        embed = discord.Embed(title='Showing info for {}'.format(fetched_user.name), color=member.color)   
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="ℹ️ General Information",
                        value=f"\n╰ **ID:** `{member.id}`"
                              f"\n╰ **Username:** `{fetched_user.name}`"
                              f"\n╰ **Discriminator:** `#{fetched_user.discriminator}`"
                              f"\n╰ **Nickname:** {member.nick}"
                              f"\n╰ **Mention:** {member.mention}")

        embed.add_field(name="<:members:907302642542325771> User Info",
                        value=f"\n╰ **Created:** {discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})"
                        ,inline=False)
        joined = sorted(ctx.guild.members, key=lambda mem: mem.joined_at)
        pos = joined.index(member)
        more = joined[pos-5 if pos >= 5 else 0:pos+5]
        join_pos = '\n'.join([(f"{pos+1}. > {x} ({x.joined_at.strftime('%m/%d/%Y')})" if x == member else f"{joined.index(x)+1}.   {x} ({x.joined_at.strftime('%m/%d/%Y')})") for x in more])
        if member.premium_since:
            embed.add_field(name="<:booster:907296708269064212> Boosting since:",
                            value=f"╰ **Date:** {discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"
                            ,inline=False)
        animated = ['png', 'jpg', 'jpeg', 'webp']
        if fetched_user.display_avatar.is_animated():
            animated.append('gif')
            avatar = " | ".join([f"[{x.upper()}]({fetched_user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        
        else:
            avatar = " | ".join([f"[{x.upper()}]({fetched_user.display_avatar.replace(format=x, size=1024).url})" for x in animated])

        animated = ['png', 'jpg', 'jpeg', 'webp']
        if fetched_user.banner:
            if fetched_user.banner.is_animated():
                banner = " | ".join([f"[{x.upper()}]({fetched_user.banner.replace(format=x, size=1024).url})" for x in animated])
            else:
                banner = " | ".join([f"[{x.upper()}]({fetched_user.banner.replace(format=x, size=1024).url})" for x in animated])
        if member.avatar:
            embed.add_field(name="<:afadsfs:909537820790620230> Avatar",
                            value=(
                                f"\n╰ {avatar}"
                            ),inline=False)

        if fetched_user.banner:
            embed.add_field(name="<:afadsfs:909537820790620230> Banner",
                            value=(
                                f"\n╰ {banner}"
                            ),inline=True) 
        embed.add_field(name="<:join:915110675800555542> Join Info",
                value=(
                    f"\n╰ **Joined:** {discord.utils.format_dt(member.joined_at, style='f')} ({discord.utils.format_dt(member.joined_at, style='R')})"
                    f"\n╰ **Join Position:**"
                    f"\n```python"
                    f"\n{join_pos}"
                    f"\n```"
                ),inline=False)  
        roles = [r.mention for r in member.roles if r != ctx.guild.default_role]
        if roles:
            if len(roles) < 10 and len(roles) > 1:
                embed.add_field(name="<:role:915122941165981747> Top Role",
                                value=member.top_role.mention, inline=False)
                
                embed.add_field(name="<:role:915122941165981747> Roles",
                                value=" ".join(roles[::-1]), inline=False)
            else:
                embed.add_field(name="<:role:915122941165981747> Top Role",
                                value=member.top_role.mention, inline=False)  
        await ctx.send(embed=embed)

    async def say_permissions(self, ctx, member, channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed(colour=member.colour)
        avatar = member.display_avatar.with_static_format('png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='<a:tick:912173533151514655> Allowed', value='\n'.join(allowed))
        e.add_field(name='<a:tickfalse:912178613258969098> Denied ', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command(aliases=['perms'])
    @commands.guild_only()
    async def permissions(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        if member is None:
            member = ctx.author

        await self.say_permissions(ctx, member, channel)

    @commands.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx: commands.Context, member: typing.Union[discord.Member, discord.User] = None):
        """Displays a user's avatar"""
        user = member or ctx.author
        embed = discord.Embed(title='Showing avatar for {}'.format(user.name))
        embed.set_image(url=user.display_avatar.replace(size=1024).url)
        animated = ['png', 'jpg', 'jpeg', 'webp']
        if user.display_avatar.is_animated():
            animated.append('gif')
            embed.description = " | ".join([f"[{x.upper()}]({user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        else:
            embed.description = " | ".join([f"[{x.upper()}]({user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        await ctx.send(embed=embed)

    @commands.command()
    async def slots(self, ctx: commands.Context):
        counter = 0
        string_list = ["【 <a:slotsroll:915158443697000469> 】", "【 <a:slotsroll:915158443697000469> 】", "【 <a:slotsroll:915158443697000469> 】"]
        embed = discord.Embed(title="Rolling the slot machine", description='|'.join(string_list))
        message = await ctx.send(embed=embed)
        slot_options = "\N{Watermelon} \N{Gem Stone} 3\N{variation selector-16}\N{combining enclosing keycap} \U0001f352 \U0001f4b5 \U0001fa99".split()
        print(slot_options)
        option_list = random.choices(slot_options, k=3)
        print(option_list)
        for item in option_list:
          await asyncio.sleep(1.5)
          string_list[counter] = f"【 {option_list[counter]} 】"
          embed.description = ' | '.join(string_list)
          await message.edit(embed=embed)
          counter += 1

async def setup(bot):
    await bot.add_cog(Utility(bot))