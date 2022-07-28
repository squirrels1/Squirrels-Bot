import io
import asyncio
import typing
import discord
import datetime
import os
import textwrap
import traceback
from discord.ext import commands
from contextlib import redirect_stdout

class DeveloperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
  
    @commands.command(help="Reloads all extensions", aliases=['relall', 'rall'], usage="[silent|channel]")
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def reloadall(self, ctx, argument: typing.Optional[str]):
        self.bot.last_rall = datetime.datetime.utcnow()
        cogs_list = ""
        to_send = ""
        err = False
        first_reload_failed_extensions = []
        if argument == 'silent' or argument == 's':
            silent = True
        else:
            silent = False
        if argument == 'channel' or argument == 'c':
            channel = True
        else:
            channel = False

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cogs_list = f"{cogs_list} \n<a:ading:910197216835158076> {filename[:-3]}"

        embed = discord.Embed(color=discord.Color.green(), description=cogs_list)
        message = await ctx.send(embed=embed)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    self.bot.reload_extension("cogs.{}".format(filename[:-3]))
                    to_send = f"{to_send} \n<a:tick:912173533151514655> Loaded - `{filename[:-3]}`"
                except Exception:
                    first_reload_failed_extensions.append(filename)

        for filename in first_reload_failed_extensions:
            try:
                self.bot.reload_extension("cogs.{}".format(filename[:-3]))
                to_send = f"{to_send} \n<a:tick:912173533151514655> Loaded `{filename[:-3]}`"

            except discord.ext.commands.ExtensionNotLoaded:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> Not loaded - `{filename[:-3]}`"
            except discord.ext.commands.ExtensionNotFound:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098>  Not found - `{filename[:-3]}`"
            except discord.ext.commands.NoEntryPointError:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> No setup func - `{filename[:-3]}`"
            except discord.ext.commands.ExtensionFailed as e:
                traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> Execution error - `{filename[:-3]}`"
                embed_error = f"\n<a:tickfalse:912178613258969098> Execution error - Traceback `{filename[:-3]}`" \
                              f"\n```py\n{traceback_string}\n```"
                if not silent:
                    target = ctx if channel else ctx.author
                    if len(embed_error) > 2000:
                        await target.send(file=io.StringIO(embed_error))
                    else:
                        await target.send(embed_error)

                err = True

        await asyncio.sleep(0.4)
        if err:
            if not silent:
                if not channel:
                    to_send = f"{to_send} \n\n📬 {ctx.author.mention}, I sent you all the tracebacks."
                else:
                    to_send = f"{to_send} \n\n📬 Sent all tracebacks here."
            if silent:
                to_send = f"{to_send} \n\n📭 silent, no tracebacks sent."
            embed = discord.Embed( title='Reloaded some extensions', description=to_send, color=discord.Color.green())
            await message.edit(embed=embed)
        else:
            embed = discord.Embed(title='Reloaded all extensions', description=to_send, color=discord.Color.green())
            await message.edit(embed=embed)
            channel = self.bot.get_channel(912234535758991380)
            await channel.send(embed=embed)    

async def setup(bot):
    await bot.add_cog(DeveloperCog(bot))