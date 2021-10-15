'''
Author: Zach Dupureur
Date: 10/15/2021

License: Creative Commons Zero v1.0 Universal

'''

import os
import discord
from discord.ext import commands
import random
from keepalive import keep_alive

# For hosting a bot on replit. Use replit database.
# Otherwise a local dictionary or text file will do.

from replit import db



class ErrorHandling(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = LoreBot

async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
  if isinstance(error, commands.BadArgument):
    message = 'Bad argument(s) provided. Use ".awaken" for commands.'
  else:
    message = 'Something went wrong! Sorry could you try again?'
  
  await ctx.send(message)

def setup(bot: commands.Bot):
  bot.add_cog(ErrorHandling(bot))

  

discordQuotes = db

LoreBot = commands.Bot(command_prefix = '.', case_insensitive = True)


@LoreBot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(LoreBot))

@LoreBot.event
async def on_message(message):
  userMsg = message.content
  author = message.author

  if author == LoreBot.user:
    return

  if message.author.bot:
    return
  
  await LoreBot.process_commands(message)

@LoreBot.command(aliases = ['helpme'])
async def awaken(ctx):
  embed = discord.Embed(
    title = 'Commands for Lore Bot',
    description = 'I am the keeper of Lore. What is your command?'
  )

  embed.add_field(name = '.awaken', value = 'Displays this menu.', inline = False)
  embed.add_field(name = '.add {key} {quote}', value = 'Adds a quote to database.', inline = False)
  embed.add_field(name = '.remove {key}', value = 'Removes a quote from the archives with {key}.', inline = False)
  embed.add_field(name = '.lore', value = 'Shows entire list of quotes, including keys as a text file.', inline = False)
  embed.add_field(name = '.quote or .random', value = 'Returns a random quote from the archives.', inline = False)
  embed.add_field(name = '.recall {key}', value = 'Returns the quote with specified {key} from the archives.')

  await ctx.send(embed = embed)

@LoreBot.command(aliases = ['addquote'])
async def add(ctx, key, *, quote):
  if key in discordQuotes.keys():
    await ctx.send('Key already in archives. Try again, but harder!')
    return
  discordQuotes[key] = quote
  await ctx.send('Quote has been added with key {}.'.format(key))

@LoreBot.command(aliases = ['delete', 'del'])
async def remove(ctx, key):
  
  if key not in discordQuotes.keys():
    await ctx.send('Sorry this key doesn\'t exist.')
    return
  
  await ctx.send('Quote you wish to remove:')
  await ctx.send('{}'.format(db[key]))
  await ctx.send('Are you sure you wish to remove this quote? Y/N')
  msg = await LoreBot.wait_for('message', check = None)
  
  if msg.content == 'Y' or msg.content == 'y':
    del discordQuotes[key]
    await ctx.send('Quote has been deleted.')
  else:
    await ctx.send('Quote has not been deleted.')

@LoreBot.command(aliases = ['quotes', 'database'])
async def lore(ctx):
  #write to file
  with open("quotes.txt", "w") as file:
    for key in discordQuotes.keys():
      file.write('Key = {0}, Quote = {1}\n'.format(key, discordQuotes[key]))
    
  #send file to Discord in message
  with open("quotes.txt", "rb") as file:
    await ctx.send("My current knowledge:", file=discord.File(file, "quotes.txt"))
  
  os.remove("quotes.txt")

@LoreBot.command(aliases = ['knowledge'])
async def recall(ctx, key):
  if key not in discordQuotes.keys():
    await ctx.send('I cannot find that quote. Perhaps my archives are incomplete?')
    return
  else:
    await ctx.send('Quote with key {}:'.format(key))
    await ctx.send('{}'.format(discordQuotes[key]))



@LoreBot.command(aliases = ['random'])
async def quote(ctx):
  keyList = []
  for keys in discordQuotes.keys():
    keyList.append(keys)

  await ctx.send(discordQuotes[random.choice(keyList)])



 
keep_alive()
LoreBot.run(os.getenv(#BOT_TOKEN))