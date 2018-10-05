import os
import random
import discord
from .utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class OpenRP:
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'data/openrp/openrp.json'
        self.openrps = dataIO.load_json(self.filename)

    async def save_openrp(self):
        dataIO.save_json(self.filename, self.openrps)

    @commands.command(pass_context=True, no_pm=True, name='openrp')
    async def _openrp(self, context, openrpee: discord.Member):
        """Randomly chooses an openRP."""
        server = context.message.server
        author = context.message.author
        if server.id in self.openrps:
            x = list(self.openrps[server.id].keys())
            if openrpee.id == author.id:
                message = 'I won\'t let you openRP yourself!'
            elif openrpee.id == self.bot.user.id:
                message = 'I refuse to openRP myself!'
            else:
                message = self.openrps[server.id][random.choice(x)]['text'].format(openrpee=openrpee.display_name, openrper=author.display_name)
        else:
            message = 'I don\'t know how to openRP yet. Use `{}addopenrp` to add openRPs.'.format(context.prefix)
        await self.bot.say(message)

    @commands.command(pass_context=True, name='removeopenrp')
    @checks.mod_or_permissions(administrator=True)
    async def _removeopenrp(self, context, name):
        """Remove a openRP"""
        server = context.message.server
        if server.id not in self.openrps or name.lower() not in self.openrps[server.id]:
            message = 'I do not know `{}`'.format(name)
        else:
            del self.openrps[server.id][name.lower()]
            await self.save_openrps()
            message = 'openRP removed.'
        await self.bot.say(message)

    @commands.command(pass_context=True, name='addopenrp')
    @checks.mod_or_permissions(administrator=True)
    async def _addopenrp(self, context, name, *openrp_text):
        """Variables:
        {openrper} adds the name of the openRPer
        {openrpee} adds the name of the openRPee
        """
        server = context.message.server
        if server.id not in self.openrps:
            self.openrps[server.id] = {}
        if name.lower() not in self.openrps[server.id]:
            try:
                int(name)
            except:
                self.openrps[server.id][name.lower()] = {}
                self.openrps[server.id][name.lower()]['text'] = ' '.join(openrp_text)
                await self.save_openrps()
                message = 'openRP added.'
            else:
                message = 'Name cannot be a number alone, it must contain characters.'
        else:
            message = 'This openRP is already in here! perform `{}removeopenrp <name>` to remove it.'.format(context.prefix)
        await self.bot.say(message)


def check_folder():
    if not os.path.exists('data/openrp'):
        print('Creating data/openrp folder...')
        os.makedirs('data/openrp')


def check_file():
    data = {}
    f = 'data/openrp/openrp.json'
    if not dataIO.is_valid_json(f):
        print('Creating default openrp.json...')
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    n = openrp(bot)
    bot.add_cog(n)
