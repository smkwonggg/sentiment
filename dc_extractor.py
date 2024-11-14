import discord
import re
from discord.ext import commands

# Set up intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True  # Enable messages intent
intents.message_content = True  # Enable message content intent (required for reading message content)

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# User IDs
marco = 694840655448637490
pan = 665883311553642516
kwong = 265352522036805632

# Regular expression to extract the sentiment score
sentiment_pattern = re.compile(r'\(([-+]?\d*\.?\d+)\)')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Analyzing Sentiments"))  # Set presence
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    
    count = 0
    while ((message.author.id == marco or pan or kwong) or (count >= 1)):
        await message.channel.send('早晨，我係你老豆 (i am online)')
        count += 1

    # Check if the message contains a sentiment score
    match = sentiment_pattern.search(message.content)

    if match and (message.author.id == marco):
        sentiment_score = float(match.group(1))  # Extract the sentiment score as a float
        text = message.content[:match.start()].strip()  # Get the message text
        formatted_message = (text, sentiment_score)
        print(formatted_message)

    # Check if the message content is "pan"
    if message.content.lower() == 'pan':
        await message.channel.send('pan is gay')

    # Process commands if you have any
    await bot.process_commands(message)

# Run the bot with your token
bot.run('MTMwNjI1ODA2NjUxMzE5OTE1NQ.GtbGJD.4rdzlZpUITbzaho6UN5rnTFvK1Z9HyatLyYPiA')

