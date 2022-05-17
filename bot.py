#importing discord package
import discord
import random
import asyncio
import os
from discord.ext import commands

#client set prefix to call bot
client = commands.Bot(command_prefix = '.')

# setting activity on ready
@client.event
async  def on_ready():
    await client.change_presence(activity=discord.Game('leci w kulki'))
    print("Bot is up!") #check if bot is online in terminal

# info command explaining each command
@client.command()
async  def info(ctx):
    myEmbed = discord.Embed(title='Dostępne komendy: ',
                            color=16705372)
    myEmbed.add_field(name="help", value='Wyswietla komendy', inline=False)
    myEmbed.add_field(name="info", value="Wyswietla info o bocie", inline=False)
    myEmbed.add_field(name="losowanie", value="Losuje druzyny", inline=False)
    myEmbed.add_field(name="konkurs (time)", value="Losuje jednego z osob bioracych udzial", inline=False)
    myEmbed.add_field(name="clear (amount)", value="Czysci wiadmosci", inline=False)
    myEmbed.set_footer(text ="Putek to najwiekszy szef")
    await ctx.send(embed=myEmbed)

# helps clear chat with amount of deleted messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# it begins spread people in two teams
@client.command()
async def losowanie(ctx):
    myEmbed = discord.Embed(title='Welcome to team draft: ',
                            description="You've got 60 seconds to join by pressing emoji -> ✅",
                            color=16705372)
    players = []
    team_1 = []
    team_2 = []

    message = await ctx.send(embed = myEmbed)
    await message.add_reaction('✅')
    await asyncio.sleep(60)

    message = await ctx.fetch_message(message.id)

    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user != client.user:
                    players.append(user.mention)

    if len(players) > 1:
        if len(players) % 2 != 0:
            await ctx.send('Time is up, amount of player are not even.')
        else:
            await ctx.send("Let's start draft")

            old_players = players

            while players != []:
                selected_player = random.choice(players)
                team_1.append(selected_player)
                players.remove(selected_player)

                selected_player = random.choice(players)
                team_2.append(selected_player)
                players.remove(selected_player)

            lastEmbed = discord.Embed(title='Welcome to team draft: ',
                                    description=f'{old_players.count(old_players)} is amount of the people that joined draft)',
                                    color=16705372)
            lastEmbed.add_field(name="Team 1", value='\n'.join(team_1), inline=True)
            lastEmbed.add_field(name="Team 2", value='\n'.join(team_2), inline=True)
            await ctx.send(embed=lastEmbed)
    else:
        await ctx.send('Time is up, one is not enough.')

@client.command()
async def konkurs(ctx, amount=60):
    myEmbed = discord.Embed(title='Welcome in the lotery: ',
                            description=f"You've got {amount} seconds to join lottery by pressing this emoji -> ✅",
                            color=16705372)
    players = []

    message = await ctx.send(embed = myEmbed)
    await message.add_reaction('✅')
    await asyncio.sleep(amount)

    message = await ctx.fetch_message(message.id)

    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user != client.user:
                    players.append(user.mention)

    winner = random.choice(players)

    lastEmbed = discord.Embed(title='Lottery : ',
                                    description=f'Person who in is:{winner}',
                                    color=16705372)
    await ctx.send(embed=lastEmbed)


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')








    





# run the client
client.run()
